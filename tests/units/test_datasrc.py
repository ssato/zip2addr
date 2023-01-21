# Copyright (C) 2023 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import pathlib
import shutil
import time

import pytest

from zip2addr import (
    constants,
    datasrc as TT
)


CSV_FILENAMES = (
    constants.ROMAN_ZIPCODE_FILENAME,
    constants.KANA_ZIPCODE_FILENAME
)
ZIP_FILENAMES = (
    constants.ROMAN_ZIPCODE_ZIP_FILENAME,
    constants.KANA_ZIPCODE_ZIP_FILENAME
)


@pytest.fixture(name="curdir")
def get_curdir(request) -> pathlib.Path:
    """
    .. seealso::
       https://docs.pytest.org/en/6.2.x/reference.html#std-fixture-request
    """
    return pathlib.Path(request.fspath).parent


@pytest.fixture(name="my_datadir")
def get_datadir(request) -> pathlib.Path:
    return pathlib.Path(request.fspath).parent.parent.parent / "data"


@pytest.mark.parametrize(
    ("suffix", ),
    (("backup", ),
     (f"{str(time.time()).replace('.', '_')}", ),
     )
)
def test_backup_if_it_exists(suffix, tmp_path):
    filename = "test.json"
    original = tmp_path / filename
    backup = tmp_path / f"{filename}.{suffix}"

    assert not original.exists()
    TT.backup_if_it_exists(original, suffix=suffix)
    assert not backup.exists()

    original.touch()
    assert original.exists()
    TT.backup_if_it_exists(original, suffix=suffix)
    assert backup.exists()


@pytest.mark.parametrize(
    ("subdir", ),
    (("out", ),
     ("out/0/1", ),
     )
)
def test_extract_file_from_zip_file(subdir, tmp_path):
    zip_filepath = tmp_path / "test.zip"
    outdir = tmp_path / subdir
    data_s = "a,b,c,0,10,-2"
    ok_filename = "foo.csv"
    ng_filename = "it_does_not_exist.csv"

    with TT.zipfile.ZipFile(str(zip_filepath), mode='w') as zipf:
        zipf.writestr(ok_filename, data_s)

    assert zip_filepath.exists()

    TT.extract_file_from_zip_file(zip_filepath, outdir, ok_filename)
    assert (outdir / ok_filename).exists()

    with pytest.raises(OSError) as exc:
        TT.extract_file_from_zip_file(zip_filepath, outdir, ng_filename)
    assert not (outdir / ng_filename).exists()
    assert ng_filename in str(exc.value)


@pytest.mark.parametrize(
    ("row", "keys", "expected"),
    (([], TT.ROMAN_ROW_KEYS, None),
     (["0861834", "北海道", "目梨郡　羅臼町", "礼文町",
       "HOKKAIDO", "MENASHI GUN RAUSU CHO", "REBUNCHO"],
      TT.ROMAN_ROW_KEYS,
      dict(zipcode="0861834", pref="北海道", city_ward="目梨郡　羅臼町",
           house_numbers="礼文町",
           roman_pref="HOKKAIDO", roman_city_ward="MENASHI GUN RAUSU CHO",
           roman_house_numbers="REBUNCHO")),
     ([14101, "230 ", "2300033", "ｶﾅｶﾞﾜｹﾝ", "ﾖｺﾊﾏｼﾂﾙﾐｸ", "ｱｻﾋﾁｮｳ", "神奈川県",
       "横浜市鶴見区", "朝日町"],
      TT.KANA_ROW_KEYS,
      dict(_city_id_or_something=14101,
           _partial_zip_code="230 ",
           zipcode="2300033",
           kana_pref="ｶﾅｶﾞﾜｹﾝ",
           kana_city_ward="ﾖｺﾊﾏｼﾂﾙﾐｸ",
           kana_house_numbers="ｱｻﾋﾁｮｳ",
           pref="神奈川県",
           city_ward="横浜市鶴見区",
           house_numbers="朝日町")),
     ),
)
def test_parse_roman_or_kana_data(row, keys, expected):
    assert TT.parse_roman_or_kana_data(row, keys) == expected


@pytest.mark.parametrize(
    ("zip_filename", "filename", "keys"),
    ((constants.ROMAN_ZIPCODE_ZIP_FILENAME,
      constants.ROMAN_ZIPCODE_FILENAME,
      TT.ROMAN_ROW_KEYS),
     (constants.KANA_ZIPCODE_ZIP_FILENAME,
      constants.KANA_ZIPCODE_FILENAME,
      TT.KANA_ROW_KEYS),
     ),
)
def test_load_and_parse(zip_filename, filename, keys, my_datadir, tmp_path):
    TT.extract_file_from_zip_file(
        my_datadir / zip_filename, tmp_path, filename
    )
    filepath = tmp_path / filename
    assert filepath.exists()

    res = list(TT.load_and_parse(filepath, keys))
    assert res


@pytest.mark.parametrize(
    ("csv_filenames", ),
    ((constants.ZIPCODE_CSV_FILENAMES, ),
     ),
)
def test_load_from_files_have_no_data(csv_filenames, tmp_path):
    for fname in csv_filenames:
        (tmp_path / fname).touch()

    assert TT.load_from_files(tmp_path, csv_filenames) == []


@pytest.mark.parametrize(
    ("filenames", "zip_filenames"),
    ((constants.ZIPCODE_CSV_FILENAMES,
      constants.ZIPCODE_ZIP_FILENAMES),
     ),
)
def test_load_from_files(filenames, zip_filenames, my_datadir, tmp_path):
    alt_filenames = tuple(f"{n}.copy.csv" for n in filenames)

    for zname, fname, aname in zip(zip_filenames, filenames, alt_filenames):
        TT.extract_file_from_zip_file(my_datadir / zname, tmp_path, fname)
        filepath = tmp_path / fname
        assert filepath.exists()

        # alt. (tmp_path / aname).write_bytes(filepath.read_bytes())
        shutil.copyfile(str(filepath), str(tmp_path / aname))

    assert TT.load_from_files(tmp_path)
    assert TT.load_from_files(tmp_path, alt_filenames)


@pytest.mark.parametrize(
    ("outname", ),
    ((constants.JSON_FILENAME, ),
     ("foo.json", ),
     )
)
def test_load_and_save_as_json(outname, my_datadir, tmp_path):
    for zname, fname in zip(constants.ZIPCODE_ZIP_FILENAMES,
                            constants.ZIPCODE_CSV_FILENAMES):
        TT.extract_file_from_zip_file(my_datadir / zname, tmp_path, fname)
        filepath = tmp_path / fname
        assert filepath.exists()

    outdir = tmp_path / "out"
    TT.load_and_save_as_json(outdir, tmp_path, outname=outname)
    assert (outdir / outname).exists()
