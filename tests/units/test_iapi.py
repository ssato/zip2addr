# Copyright (C) 2023 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import shutil
import time
import zipfile

import pytest

from zip2addr import (
    constants,
    datagen as TT,
    db,
    models
)


CSV_FILENAMES = (
    constants.ROMAN_ZIPCODE_FILENAME,
    constants.KANA_ZIPCODE_FILENAME
)
ZIP_FILENAMES = (
    constants.ROMAN_ZIPCODE_ZIP_FILENAME,
    constants.KANA_ZIPCODE_ZIP_FILENAME
)


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

    with zipfile.ZipFile(str(zip_filepath), mode='w') as zipf:
        zipf.writestr(ok_filename, data_s)

    assert zip_filepath.exists()

    TT.extract_file_from_zip_file(zip_filepath, outdir, ok_filename)
    assert (outdir / ok_filename).exists()

    with pytest.raises(KeyError) as exc:
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


def test_load_and_parse_no_data(tmp_path):
    filepath = tmp_path / "test.csv"
    filepath.touch()

    assert not list(TT.load_and_parse(filepath, TT.ROMAN_ROW_KEYS))


@pytest.mark.parametrize(
    ("filename", "keys"),
    ((constants.ROMAN_ZIPCODE_FILENAME, TT.ROMAN_ROW_KEYS),
     (constants.KANA_ZIPCODE_FILENAME, TT.KANA_ROW_KEYS),
     ),
)
def test_load_and_parse(filename, keys, my_datadir):
    filepath = my_datadir / filename
    res = list(TT.load_and_parse(filepath, keys))
    assert res
    assert len(res) == len((filepath.open(encoding='shift_jis')).readlines())


def test_load_from_files_have_no_data(tmp_path):
    for fname in constants.ZIPCODE_CSV_FILENAMES:
        (tmp_path / fname).touch()

    assert not TT.load_from_files(tmp_path, constants.ZIPCODE_CSV_FILENAMES)


def test_load_from_files(my_datadir, tmp_path):
    filenames = constants.ZIPCODE_CSV_FILENAMES
    alt_filenames = tuple(f"{n}.copy.csv" for n in filenames)

    for fname, aname in zip(filenames, alt_filenames):
        # altanative.
        # (tmp_path / aname).write_bytes((my_datadir / fname).read_bytes())
        shutil.copyfile(str(my_datadir / fname), str(tmp_path / aname))

    assert TT.load_from_files(my_datadir)
    assert TT.load_from_files(my_datadir, filenames)
    assert TT.load_from_files(tmp_path, alt_filenames)


def test_load_and_save_as_json_no_data(tmp_path):
    for fname in constants.ZIPCODE_CSV_FILENAMES:
        (tmp_path / fname).touch()

    outdir = tmp_path / "out"
    TT.load_and_save_as_json(tmp_path, outdir)
    assert not outdir.exists()
    assert not (outdir / constants.JSON_FILENAME).exists()


@pytest.mark.parametrize(
    ("outname", ),
    ((constants.JSON_FILENAME, ),
     ("out.json", ),
     )
)
def test_load_and_save_as_json(outname, my_datadir, tmp_path):
    outdir = tmp_path / "out"
    TT.load_and_save_as_json(my_datadir, outdir, outname=outname)
    shutil.copyfile(str(outdir / outname), "/tmp/zipcode.json")
    assert (outdir / outname).exists()
    assert TT.anyconfig.load(outdir / outname)


def test_load_json_and_save_as_db_no_data(tmp_path):
    (tmp_path / constants.JSON_FILENAME).touch()
    TT.load_json_and_save_as_db(tmp_path, tmp_path)
    assert not (tmp_path / constants.DATABASE_FILENAME).exists()


def test_load_json_and_save_as_db(my_datadir, tmp_path):
    TT.load_json_and_save_as_db(my_datadir, tmp_path)
    outpath = tmp_path / constants.DATABASE_FILENAME
    assert outpath.exists()

    with db.get_session_ctx(outpath) as dbs_ctx:
        assert dbs_ctx.query(models.Zipcode).all()


def test_make_database_from_zip_files_errors(tmp_path):
    with pytest.raises(FileNotFoundError):
        TT.make_database_from_zip_files(tmp_path, tmp_path)

    (tmp_path / constants.ZIPCODE_ZIP_FILENAMES[0]).touch()
    with pytest.raises(zipfile.BadZipFile):
        TT.make_database_from_zip_files(tmp_path, tmp_path)

    # prepare zip files contains csv files with no data.
    for zfn, cfn in zip(constants.ZIPCODE_ZIP_FILENAMES,
                        constants.ZIPCODE_CSV_FILENAMES):
        with zipfile.ZipFile(str(tmp_path / zfn), mode='w') as zipf:
            zipf.writestr(cfn, "")

    TT.make_database_from_zip_files(tmp_path, tmp_path)
    assert not (tmp_path / constants.DATABASE_FILENAME).exists()


@pytest.mark.parametrize(
    ("outname", ),
    ((constants.DATABASE_FILENAME, ),
     ("out.db", ),
     )
)
def test_make_database_from_zip_files(outname, my_datadir, tmp_path):
    TT.make_database_from_zip_files(my_datadir, tmp_path, outname=outname)
    db_path = tmp_path / outname

    assert db_path.exists()
    with db.get_session_ctx(db_path) as dbs_ctx:
        assert dbs_ctx.query(models.Zipcode).all()
