"""Database.

.. seealso:: https://fastapi.tiangolo.com/ja/tutorial/sql-databases/
"""
import contextlib
import pathlib
import typing

import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.orm

from . import constants, utils


Base = sqlalchemy.orm.declarative_base()


def get_engine(
    filepath: typing.Union[str, pathlib.Path] = constants.DATABASE_FILEPATH
):
    """Get an initialized database engine instance.
    """
    return sqlalchemy.create_engine(
        f"sqlite:///{filepath}",
        connect_args={"check_same_thread": False},
        echo=utils.is_verbose_mode()
    )


def init(engine):
    """Create a database.
    """
    Base.metadata.create_all(bind=engine)


def get_session_class(
    filepath: typing.Union[str, pathlib.Path], read_only: bool = False
):
    """Get a database session class.
    """
    engine = get_engine(filepath)
    if not read_only:
        init(engine)

    return sqlalchemy.orm.sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )


def get_session(
    filepath: typing.Union[str, pathlib.Path], read_only: bool = False
):
    """Get a database session.
    """
    cls = get_session_class(filepath, read_only=read_only)
    dbs = cls()
    try:
        yield dbs
        if not read_only:
            dbs.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        if not read_only:
            dbs.rollback()
        raise
    finally:
        dbs.close()


def get_default_session():
    """Get a default database session.
    """
    yield from get_session(constants.DATABASE_FILEPATH)


@contextlib.contextmanager
def get_session_ctx(
    filepath: typing.Union[str, pathlib.Path], read_only: bool = False
):
    """Get a database session can be used with 'with' statement.
    """
    yield from get_session(filepath, read_only)
