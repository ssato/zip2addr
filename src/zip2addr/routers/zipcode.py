"""Routers.
"""
import typing

import fastapi
import sqlalchemy
import sqlalchemy.orm

from .. import (
    constants,
    crud,
    db,
    schemas,
)


ROUTER = fastapi.APIRouter()


@ROUTER.get("/zipcodes/", response_model=list[schemas.Zipcode])
async def get_zipcodes(
    skip: int = 0, limit: int = constants.LIMIT,
    dbs: sqlalchemy.orm.Session = fastapi.Depends(db.get_default_session)
):
    """API: usage.
    """
    return crud.get_zipcodes(dbs, skip=skip, limit=limit)


@ROUTER.get("/zipcodes/{zipcode}", response_model=schemas.Zipcode)
async def get_zipcode(
    zipcode: str,
    dbs: sqlalchemy.orm.Session = fastapi.Depends(db.get_default_session)
):
    """API: usage.
    """
    res = crud.get_zipcode(dbs, zipcode)
    if res is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Zip code was not found: {zipcode}"
        )
    return res


@ROUTER.get(
    "/zipcodes/{partial_zipcode}",
    response_model=list[schemas.Zipcode]
)
async def get_zipcodes_by_partial_zipcode(
    partial_zipcode: str,
    skip: int = 0, limit: int = constants.LIMIT,
    dbs: sqlalchemy.orm.Session = fastapi.Depends(db.get_default_session)
):
    """API: usage.
    """
    return crud.get_zipcodes_by_partial_zipcode(
        dbs, partial_zipcode, skip=skip, limit=limit
    )
