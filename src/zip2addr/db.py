"""Database.

.. seealso:: https://fastapi.tiangolo.com/ja/tutorial/sql-databases/
"""
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from . import constants


Base = sqlalchemy.ext.declarative.declarative_base()


def get_engine(
    filepath: str = constants.DATABASE_FILEPATH
):
    """Get an initialized database engine instance.
    """
    return sqlalchemy.create_engine(
        f"sqlite:///{filepath}",
        connect_args={"check_same_thread": False},
        echo=True
    )


def get_session(engine):
    """Get a database session.
    """
    session_cls = sqlalchemy.orm.sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    dbs = session_cls()
    try:
        return dbs
    finally:
        dbs.close()


def init(engine):
    """Create a database.
    """
    Base.metadata.create_all(bind=engine)
