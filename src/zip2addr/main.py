"""Web app entry point.
"""
import fastapi


APP = fastapi.FastAPI()


@APP.get('/')
async def usage():
    """API: usage.
    """
    return dict(message="Usage: GET /?zipcode=<zipcode>")
