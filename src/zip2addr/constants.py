"""Constants.
"""
import typing


VERSION: tuple[int, int, int] = (0, 1, 0)

# .. seealso:: https://www.post.japanpost.jp/zipcode/download.html
ROMAN_ZIPCODE_ZIP_FILENAME: typing.Final[str] = "ken_all_rome.zip"
KANA_ZIPCODE_ZIP_FILENAME: typing.Final[str] = "ken_all.zip"
ZIPCODE_ZIP_FILENAMES: tuple[str, ...] = (
    ROMAN_ZIPCODE_ZIP_FILENAME,
    KANA_ZIPCODE_ZIP_FILENAME,
)

ROMAN_ZIPCODE_FILENAME: typing.Final[str] = "KEN_ALL_ROME.csv"
KANA_ZIPCODE_FILENAME: typing.Final[str] = "KEN_ALL.CSV"
ZIPCODE_CSV_FILENAMES: tuple[str, ...] = (
    ROMAN_ZIPCODE_FILENAME,
    KANA_ZIPCODE_FILENAME,
)

JSON_FILENAME: typing.Final[str] = "zipcodes.json"

# .. seealso:: https://peps.python.org/pep-0591/
DATABASE_FILENAME: typing.Final[str] = "zipcodes.db"
DATABASE_FILEPATH: typing.Final[str] = f"./{DATABASE_FILENAME}"
