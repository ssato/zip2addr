# pylint: disable=too-few-public-methods
"""Data schema.

.. seealso:: https://bit.ly/3HLRXTS
"""
import pydantic


class KanaAddress(pydantic.BaseModel):
    """Address info in kana characters.
    """
    pref: str
    city_ward: str
    house_numbers: str

    class Config:
        """Configurations to pydantic.

        .. seealso:: https://bit.ly/3WuRYQg
        """
        orm_mode = True


class Address(pydantic.BaseModel):
    """Address info.
    """
    pref: str
    city_ward: str
    house_numbers: str

    class Config:
        """Configurations to pydantic.
        """
        orm_mode = True


class Zipcode(pydantic.BaseModel):
    """Zip code and address info.
    """
    id: int
    zipcode: str
    addr: Address
    # kana_addr: KanaAddress

    class Config:
        """Configurations to pydantic.
        """
        orm_mode = True
