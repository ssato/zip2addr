# Copyright (C) 2023 Satoru SATOH <satoru.satoh at gmail.com>
# SPDX-License-Identifier: MIT
"""coding: utf-8

zip code data loading stuff.

CSV data:

- sources:
  - zip codes + addrs (roman):
    https://www.post.japanpost.jp/zipcode/dl/roman-zip.html
  - zip codes + addrs (kana):
    https://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html

- formats:
  - roman data:

    - zipcode, e.g. "0600007"
    - pref, e.g. "北海道"
    - city_ward, e.g. "札幌市　中央区"
    - house_numbers, e.g. "北七条西"
    - roman_pref, e.g. "HOKKAIDO"
    - roman_city_ward, e.g. "SAPPORO SHI CHUO KU"
    - roman_house_numbers, e.g. "KITA7-JONISHI"

  - kana data:

    - <city_id_or_something>, e.g. 01101
    - <partial zip code and some white spaces>, e.g. "064  "
    - kana_pref, e.g. "ﾎｯｶｲﾄﾞｳ"
    - kana_city_ward, e.g. "ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ"
    - kana_house_numbers, e.g. "ｷﾀ21ｼﾞｮｳﾆｼ"
    - pref, e.g. "北海道"
    - city_ward, e.g. "札幌市　中央区"
    - house_numbers, e.g. "北七条西"
    - <some numbers ...>
"""
import collections
import csv
import itertools
import logging
import pathlib
import time
import typing
import zipfile

import anyconfig

from . import constants, db, models


LOG = logging.getLogger(__name__)

ROMAN_ROW_KEYS: tuple[str, ...] = tuple("""
zipcode
pref
city_ward
house_numbers
roman_pref
roman_city_ward
roman_house_numbers
""".split())

KANA_ROW_KEYS: tuple[str, ...] = tuple("""
_city_id_or_something
_partial_zip_code
zipcode
kana_pref
kana_city_ward
kana_house_numbers
pref
city_ward
house_numbers
""".split())

ROW_KEYS_SET: tuple[tuple[str, ...], ...] = (
    ROMAN_ROW_KEYS,
    KANA_ROW_KEYS
)


def backup_if_it_exists(
    filepath: pathlib.Path,
    suffix: typing.Optional[str] = None
):
    """
    Backup the file if it exists.
    """
    if filepath.exists():
        if suffix is None or not suffix:
            suffix = f"{str(time.time()).replace('.', '_')}"

        filepath.rename(f"{filepath!s}.{suffix}")


def extract_file_from_zip_file(
    zip_filepath: pathlib.Path, outdir: pathlib.Path, filename: str
):
    """
    Extract a csv file from the zip file.

    :raiess: FileNotFoundError, KeyError, zipfile.BadZipFile
    """
    with zipfile.ZipFile(zip_filepath) as zipf:
        if not outdir.exists():
            outdir.mkdir(parents=True)

        zipf.extract(filename, path=outdir)


def parse_roman_or_kana_data(
    row: list[str], keys: tuple[str, ...]
) -> typing.Optional[dict]:
    """Parse roman or kana zip code data row strings.
    """
    default = None

    if not row:
        return default

    try:
        return dict(zip(keys, row))
    except (ValueError, TypeError):
        return default


def load_and_parse(
    filepath: pathlib.Path, keys: tuple[str, ...]
) -> typing.Iterator[typing.Optional[dict]]:
    """Load zip code data in csv format.
    """
    with filepath.open(encoding='shift_jis') as csvf:
        for row in csv.reader(csvf):
            yield parse_roman_or_kana_data(row, keys)


def load_from_files(
    datadir: pathlib.Path,
    csv_filenames: tuple[str, ...] = constants.ZIPCODE_CSV_FILENAMES
) -> list[dict[str, str]]:
    """
    Load and parse zip code data files in csv format and return parsed data.
    """
    # zipcode: <zipcode dict>
    zipcodes: typing.OrderedDict[str, dict] = collections.OrderedDict()

    all_keys = set(itertools.chain(*ROW_KEYS_SET))

    for keys, filename in zip(ROW_KEYS_SET, csv_filenames):
        filepath = datadir / filename

        for idx, zdata in enumerate(load_and_parse(filepath, keys)):
            if zdata is None:
                LOG.warning(
                    "Failed to load and parse the line #%d in the file %s",
                    idx, filename
                )
                continue

            zipcode = zdata["zipcode"]

            if zipcode in zipcodes:
                zipcodes[zipcode].update(**zdata)
            else:
                # For cases corresponding another data is missing.
                for key in all_keys:
                    if key not in zdata:
                        zdata[key] = ""

                zipcodes[zipcode] = zdata

    return list(zipcodes.values())


def load_and_save_as_json(
    datadir: pathlib.Path,
    outdir: pathlib.Path,
    csv_filenames: tuple[str, ...] = constants.ZIPCODE_CSV_FILENAMES,
    outname: str = constants.JSON_FILENAME
):
    """
    Load and parse zip code data files in csv format and dump parsed data to a
    json file.
    """
    res = load_from_files(datadir, csv_filenames)

    if res:
        opath = outdir / outname

        if not outdir.exists():
            outdir.mkdir(parents=True)

        backup_if_it_exists(opath)
        anyconfig.dump(res, opath)  # type: ignore
    else:
        LOG.error("Failed to get data from %s and %s", *csv_filenames)


def load_json_and_save_as_db(
    datadir: pathlib.Path,
    outdir: pathlib.Path,
    filename: str = constants.JSON_FILENAME,
    outname: str = constants.DATABASE_FILENAME,
):
    """
    Load zip code parsed data in a json file and dump its data as a database
    file.
    """
    filepath = datadir / filename
    outpath = outdir / outname

    if not filepath.exists():
        LOG.error("Not found: %s", str(filepath))
        return

    with filepath.open(mode='rb') as bfd:
        if not bfd.read1(5):
            LOG.error("No data: %s", str(filepath))
            return

    if not outdir.exists():
        outdir.mkdir(parents=True)

    backup_if_it_exists(outpath)

    with db.get_session(outpath) as dbs:
        for zdata in anyconfig.load(filepath):
            addr = models.Address(
                pref=zdata['pref'],
                city_ward=zdata['city_ward'],
                house_numbers=zdata['house_numbers']
            )
            dbs.add(addr)
            dbs.commit()
            dbs.refresh(addr)

            kana_addr = models.KanaAddress(
                pref=zdata['kana_pref'],
                city_ward=zdata['kana_city_ward'],
                house_numbers=zdata['kana_house_numbers'],
                address_id=addr.id
            )
            dbs.add(kana_addr)
            dbs.commit()
            dbs.refresh(kana_addr)

            roman_addr = models.KanaAddress(
                pref=zdata['roman_pref'],
                city_ward=zdata['roman_city_ward'],
                house_numbers=zdata['roman_house_numbers'],
                address_id=addr.id
            )
            dbs.add(roman_addr)
            dbs.commit()
            dbs.refresh(roman_addr)

            zipcode = models.Zipcode(
                zipcode=zdata['zipcode'],
                address_id=addr.id
            )
            dbs.add(zipcode)
            dbs.commit()


def make_database_from_zip_files(
    datadir: pathlib.Path,
    outdir: pathlib.Path,
    zip_filenames: tuple[str, ...] = constants.ZIPCODE_ZIP_FILENAMES,
    csv_filenames: tuple[str, ...] = constants.ZIPCODE_CSV_FILENAMES,
    outname: str = constants.DATABASE_FILENAME,
):
    """
    Load and parse zip code data files in csv format and return parsed data.

    :raiess: FileNotFoundError, KeyError, zipfile.BadZipFile
    """
    for zname, fname in zip(zip_filenames, csv_filenames):
        extract_file_from_zip_file(datadir / zname, datadir, fname)

    load_and_save_as_json(datadir, outdir, csv_filenames=csv_filenames)
    load_json_and_save_as_db(datadir, outdir, outname=outname)
