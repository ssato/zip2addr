# pylint: disable=too-few-public-methods
"""Data schema.

.. seealso:: https://bit.ly/3HLRXTS
"""
import pydantic


class AddressBase(pydantic.BaseModel):
    """Address base."""
    pref: str
    city_ward: str
    house_numbers: str


class AddressCreate(AddressBase):
    """Address."""


class Address(AddressCreate):
    """Address."""
    class Config:
        """Configurations to pydantic."""
        orm_mode = True


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
