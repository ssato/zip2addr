# pylint: disable=too-few-public-methods
"""Data models.
"""
import sqlalchemy
import sqlalchemy.orm

from . import db


class KanaAddress(db.Base):
    """A model represents an address data in kana.

    e.g. "ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ﾌｼﾐ"
    """
    __tablename__ = "kana_addresses"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    pref = sqlalchemy.Column(sqlalchemy.String)
    city_ward = sqlalchemy.Column(sqlalchemy.String)
    house_numbers = sqlalchemy.Column(sqlalchemy.String)


class Address(db.Base):
    """A model represents an address data.

    e.g. "北海道","札幌市中央区","伏見"
    """
    __tablename__ = "addresses"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    pref = sqlalchemy.Column(sqlalchemy.String)
    city_ward = sqlalchemy.Column(sqlalchemy.String)
    house_numbers = sqlalchemy.Column(sqlalchemy.String)


class Zipcode(db.Base):
    """A model represents a database of zip codes and addresses.

    e.g.  "0640942","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ﾌｼﾐ","北海道","札幌市中央区","伏見"
    """
    __tablename__ = "zipcodes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    zipcode = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    addr = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("addresses.id")
    )
    # TBD
    # kana_addr = sqlalchemy.Column(
    #    sqlalchemy.Integer, sqlalchemy.ForeignKey("kana_addresses.id")
    # )
