"""Database.

.. seealso:: https://fastapi.tiangolo.com/ja/tutorial/sql-databases/
"""
import contextlib
import pathlib
import typing

import sqlalchemy
import sqlalchemy.orm

from . import constants


Base = sqlalchemy.orm.declarative_base()


def get_engine(
    filepath: typing.Union[str, pathlib.Path] = constants.DATABASE_FILEPATH
):
    """Get an initialized database engine instance.
    """
    return sqlalchemy.create_engine(
        f"sqlite:///{filepath}",
        connect_args={"check_same_thread": False},
        echo=True
    )


def init(engine):
    """Create a database.
    """
    Base.metadata.create_all(bind=engine)


@contextlib.contextmanager
def get_session(
    filepath: typing.Union[str, pathlib.Path], read_only: bool = False
):
    """Get a database session.
    """
    engine = get_engine(filepath)
    init(engine)

    session_cls = sqlalchemy.orm.sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    dbs = session_cls()
    try:
        yield dbs
        if not read_only:
            dbs.commit()
    except:  # noqa: E722
        if not read_only:
            dbs.rollback()
        raise
    finally:
        dbs.close()
