"""Functions for CRUD operations.
"""
import typing

from sqlalchemy.orm import Session

from . import constants, models, schemas


def get_zipcode(
    dbs: Session,
    zipcode: str,
) -> typing.Optional[models.Zipcode]:
    """Get *a* model instance of zip code by a zip code string.
    """
    return dbs.query(
        models.Zipcode
    ).filter(models.Zipcode.zipcode == zipcode).first()


def get_zipcodes(
    dbs: Session, skip: int = 0, limit: int = 100
) -> list[models.Zipcode]:
    """Get all of model instances of zip code.
    """
    return dbs.query(models.Zipcode).offset(skip).limit(limit).all()


def get_zipcodes_by_partial_zipcode(
        dbs: Session, partial_zipcode: str,
        skip: int = 0, limit: int = constants.LIMIT
) -> list[models.Zipcode]:
    """Get model instances of zip code by partial zip code string.
    """
    res = dbs.query(
        models.Zipcode
    ).filter(
        models.Zipcode.zipcode.startswith(partial_zipcode)
    ).offset(skip)

    return res.limit(limit).all() if limit > 0 else res.all()


def create_address(
    dbs: Session, addr: schemas.AddressCreate
) -> models.Address:
    """Create an address model instance.
    """
    db_addr = models.Address(
        pref=addr.pref, city_ward=addr.city_ward,
        house_numbers=addr.house_numbers
    )
    dbs.add(db_addr)
    dbs.commit()
    dbs.refresh(db_addr)

    return db_addr


def create_roman_address(
        dbs: Session, addr: schemas.RomanAddressCreate, address_id: int
) -> models.RomanAddress:
    """Create an address model instance from given info data.
    """
    db_addr = models.RomanAddress(
        pref=addr.pref, city_ward=addr.city_ward,
        house_numbers=addr.house_numbers,
        address_id=address_id
    )
    dbs.add(db_addr)
    dbs.commit()
    dbs.refresh(db_addr)

    return db_addr


def create_kana_address(
        dbs: Session, addr: schemas.KanaAddressCreate, address_id: int
) -> models.RomanAddress:
    """Create an address model instance from given info data.
    """
    db_addr = models.KanaAddress(
        pref=addr.pref, city_ward=addr.city_ward,
        house_numbers=addr.house_numbers,
        address_id=address_id
    )
    dbs.add(db_addr)
    dbs.commit()
    dbs.refresh(db_addr)

    return db_addr


def create_zipcode(
        dbs: Session, zipcode: schemas.ZipcodeCreate, address_id: int
) -> models.Zipcode:
    """Create an address model instance from given info data.
    """
    db_zipcode = models.Zipcode(
        zipcode=zipcode.zipcode, address_id=address_id
    )
    dbs.add(db_zipcode)
    dbs.commit()
    dbs.refresh(db_zipcode)

    return db_zipcode
