"""ping route.
"""
import fastapi

from .. import (
    constants,
)


ROUTER = fastapi.APIRouter()

PING_RESPONSE = dict(
    message="Pong!", name=constants.NAME,
    version='.'.join([str(v) for v in constants.VERSION]),
)


@ROUTER.get("/ping/")
async def ping():
    """ping.
    """
    return PING_RESPONSE
