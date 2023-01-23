# pylint: disable=too-few-public-methods
"""Data schema.

.. seealso:: https://bit.ly/3HLRXTS
"""
import pydantic

from . import (
    constants,
)


class Pong(pydantic.BaseModel):
    """pong."""
    message: str = pydantic.Field("Pong!", example="Pong!")
    name: str = pydantic.Field(constants.NAME)
    version: list[int] = pydantic.Field(constants.VERSION)


class AddressBase(pydantic.BaseModel):
    """Address base."""
    pref: str
    city_ward: str
    house_numbers: str


class AddressCreate(AddressBase):
    """Address."""


class RomanAddressCreate(AddressBase):
    """Roman address."""


class RomanAddress(RomanAddressCreate):
    """Roman address."""
    address_id: int

    class Config:
        """Configurations to pydantic."""
        orm_mode = True


class KanaAddressCreate(AddressBase):
    """Kana address."""


class KanaAddress(KanaAddressCreate):
    """Roman address."""
    address_id: int

    class Config:
        """Configurations to pydantic."""
        orm_mode = True


class Address(AddressCreate):
    """Address."""
    address_id: int

    class Config:
        """Configurations to pydantic."""
        orm_mode = True


class ZipcodeCreate(pydantic.BaseModel):
    """Zip code creator."""
    zipcode: str


class Zipcode(ZipcodeCreate):
    """Zip code and address info."""
    id: int
    address_id: int

    class Config:
        """Configurations to pydantic."""
        orm_mode = True
