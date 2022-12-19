"""Functions for CRUD operations.
"""
from sqlalchemy.orm import Session
from . import models, schemas


def get_zipcode_by_id(db: Session, zipcode_id: int) -> models.Zipcode:
    """Get *a* model instance of zip code by its ID.
    """
    return db.query(models.Zipcode).filter(models.Zipcode.id == zipcode_id).first()


def get_zipcode(db: Session, zipcode: str) -> models.Zipcode:
    """Get *a* model instance of zip code by its zip code string.
    """
    return db.query(models.Zipcode).filter(models.Zipcode.zipcode == zipcode).first()


def get_addr_by_zipcode(db: Session, zipcode: str) -> models.Address:
    """Get *a* model instance of Address by correspondig zip code string.
    """
    return get_zipcode(zipcode).addr


def get_zipcodes(db: Session, skip: int = 0, limit: int = 100):
    """Get model instances of zip code by its zip code string.
    """
    return db.query(models.Zipcode).offset(skip).limit(limit).all()


def create_address(db: Session, addr: schemas.Address):
    """Create an address model instance from given info data.
    """
    db_addr = models.Address(
        pref=addr.pref, city_ward=addr.city_ward,
        house_numbers=addr.house_numbers
    )
    db.add(db_addr)
    db.commit()
    db.refresh(db_addr)

    return db_addr
