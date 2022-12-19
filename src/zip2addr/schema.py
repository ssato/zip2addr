# pylint: disable=too-few-public-methods
"""Data schema.

.. seealso:: https://bit.ly/3HLRXTS
"""
import pydantic


class Zipcode(pydantic.BaseModel):
    """Zip code and address info.
    """
    id: int
    zipcode: str

    pref: str
    city_ward: str
    house_numbers: str

    kana_pref: str
    kana_city_ward: str
    kana_house_numbers: str

    class Config:
        """Configurations to pydantic.
        """
        orm_mode = True
