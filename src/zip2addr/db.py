"""Database.

.. seealso:: https://fastapi.tiangolo.com/ja/tutorial/sql-databases/
"""
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from . import constants


ENGINE = sqlalchemy.create_engine(
    constants.DATABASE_URI, connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sqlalchemy.orm.sessionmaker(
    autocommit=False, autoflush=False, bind=ENGINE
)
Base = sqlalchemy.ext.declarative.declarative_base()


def get_session():
    """Get a database session.
    """
    dbs = SessionLocal()
    try:
        return dbs
    finally:
        dbs.close()


def init(renew: bool = True):
    """Create a database.
    """
    if renew:
        Base.metadata.create_all(bind=ENGINE)
