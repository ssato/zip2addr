"""Routers.
"""
import fastapi
import fastapi.encoders
import fastapi.responses
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


# @ROUTER.get("/zipcodes/{zipcode}", response_model=schemas.Zipcode)
@ROUTER.get("/zipcodes/{zipcode}")
async def get_zipcode(
    zipcode: str,
    dbs: sqlalchemy.orm.Session = fastapi.Depends(db.get_default_session)
):
    """API: usage.
    """
    res = crud.get_zipcode(dbs, zipcode)
    if res is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Zip code was not found: {zipcode}"
        )
    data = fastapi.encoders.jsonable_encoder(res.as_dict())
    return fastapi.responses.JSONResponse(content=data)


@ROUTER.get(
    "/zipcodes/partial/{partial_zipcode}",
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
