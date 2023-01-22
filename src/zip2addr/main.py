"""Web app entry point.
"""
import fastapi

from .routers import (
    ping,
    zipcode,
)


APP = fastapi.FastAPI()
APP.include_router(ping.ROUTER)
APP.include_router(zipcode.ROUTER)
