"""Routers.
"""
import fastapi


ROUTER = fastapi.APIRouter()


@ROUTER.get('/')
async def get_addr_from_zip_code(
    zipcode: str = fastapi.Query(regex="^\\d{7}$")
):
    """API: usage.
    """
    return dict(message="Usage: GET /?zipcode=<zipcode>")
