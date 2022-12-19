"""Database.
"""
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from . import constants


Engine = sqlalchemy.create_engine(
    constants.DATABASE_URI, connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sqlalchemy.orm.sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)
Base = sqlalchemy.ext.declarative.declarative_base()

Base.metadata.create_all(bind=Engine)
