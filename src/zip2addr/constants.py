"""Constants.
"""
import typing


# .. seealso:: https://www.post.japanpost.jp/zipcode/download.html
ROMAN_ZIPCODE_FILENAME: str = "KEN_ALL_ROME.csv"
KANA_ZIPCODE_FILENAME: str = "KEN_ALL.CSV"

JSON_FILEPATH: typing.Final[str] = "zipcodes.json"

# .. seealso:: https://peps.python.org/pep-0591/
DATABASE_FILENAME: typing.Final[str] = "zipcodes.db"
DATABASE_FILEPATH: typing.Final[str] = f"./{DATABASE_FILENAME}"
