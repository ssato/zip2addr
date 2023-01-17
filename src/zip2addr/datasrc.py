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
import logging
import pathlib
import time
import typing

import anyconfig

from . import constants, db, models


LOG = logging.getLogger(__name__)

ROMAN_ROW_KEYS: tuple[typing.Literal, ...] = tuple("""
zipcode
pref
city_ward
house_numbers
roman_pref
roman_city_ward
roman_house_numbers
""".split())

KANA_ROW_KEYS: tuple[typing.Literal, ...] = tuple("""
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


def parse_roman_or_kana_data(
    row: list[str], keys: tuple[typing.Literal, ...]
) -> typing.Optional[dict]:
    """Parse roman or kana zip code data row strings.
    """
    try:
        return dict(zip(keys, row))
    except (ValueError, TypeError):
        return None


def load_and_parse(
    filepath: pathlib.Path, keys: tuple[typing.Literal, ...]
) -> typing.Iterator[dict]:
    """Load zip code data in csv format.
    """
    with filepath.open(encoding='shift_jis') as csvf:
        for row in csv.reader(csvf):
            yield parse_roman_or_kana_data(row, keys)


def load_from_files(
    datadir: pathlib.Path = pathlib.Path('.'),
    roman_filename: str = constants.ROMAN_ZIPCODE_FILENAME,
    kana_filename: str = constants.KANA_ZIPCODE_FILENAME
) -> list[dict[str, str]]:
    """
    Load and parse zip code data files in csv format and return parsed data.
    """
    # zipcode: <zipcode dict>
    zipcodes: typing.OrderedDict[str, dict] = collections.OrderedDict()

    roman_filepath = datadir / roman_filename
    kana_filepath = datadir / kana_filename

    for idx, zdata in enumerate(
        load_and_parse(roman_filepath, ROMAN_ROW_KEYS)
    ):
        if zdata is None:
            LOG.warning(
                "Failed to load and parse the line #%d in the file %s",
                idx, roman_filepath
            )
            continue

        # For cases corresponding kana address data will be missing.
        zdata["kana_pref"] = ""
        zdata["kana_city_ward"] = ""
        zdata["kana_house_numbers"] = ""

        zipcodes[zdata["zipcode"]] = zdata

    for idx, zdata in enumerate(
        load_and_parse(kana_filepath, KANA_ROW_KEYS)
    ):
        if zdata is None:
            LOG.warning(
                "Failed to load and parse the line #%d in the file %s",
                idx, kana_filepath
            )
            continue

        zipcode = zdata["zipcode"]

        if zipcode in zipcodes:
            zipcodes[zipcode].update(**zdata)
        else:
            # For cases corresponding roman address data is missing.
            zdata["roman_pref"] = ""
            zdata["roman_city_ward"] = ""
            zdata["roman_house_numbers"] = ""

            zipcodes[zipcode] = zdata

    return list(zipcodes.values())


def load_and_save_as_json(
    datadir: pathlib.Path = pathlib.Path('.'),
    roman_filename: str = constants.ROMAN_ZIPCODE_FILENAME,
    kana_filename: str = constants.KANA_ZIPCODE_FILENAME,
    outpath: str = constants.JSON_FILEPATH
):
    """
    Load and parse zip code data files in csv format and dump parsed data to a
    json file.
    """
    res = load_from_files(datadir, roman_filename, kana_filename)

    opath = pathlib.Path(outpath)
    backup_if_it_exists(opath)

    anyconfig.dump(res, outpath)


def load_json_and_save_as_db(
    filepath: str = constants.JSON_FILEPATH, renew: bool = True
):
    """
    Load zip code parsed data in a json file and dump its data as a database
    file.
    """
    backup_if_it_exists(pathlib.Path(constants.DATABASE_FILENAME))

    db.init(renew=renew)
    dbs = db.get_session()

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

    dbs.commit()
    dbs.close()
