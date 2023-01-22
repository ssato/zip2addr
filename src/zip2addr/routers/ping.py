"""ping route.
"""
import fastapi

from .. import (
    constants,
    schemas,
)


ROUTER = fastapi.APIRouter()

PING_RESPONSE = dict(
    message="Pong!", name=constants.NAME,
    version=list(constants.VERSION),
)


@ROUTER.get("/ping/", response_model=schemas.Pong)
async def ping():
    """ping.
    """
    return PING_RESPONSE
