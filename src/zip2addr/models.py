# pylint: disable=too-few-public-methods
"""Data models.
"""
import sqlalchemy

from . import db


class Zipcode(db.Base):
    """A model represents a database of zip codes and addresses.

    e.g.  "0640942","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ﾌｼﾐ","北海道","札幌市中央区","伏見"
    """
    __tablename__ = "zipcodes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    zipcode = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)

    pref = sqlalchemy.Column(sqlalchemy.String)
    city_ward = sqlalchemy.Column(sqlalchemy.String)
    house_numbers = sqlalchemy.Column(sqlalchemy.String)

    kana_pref = sqlalchemy.Column(sqlalchemy.String)
    kana_city_ward = sqlalchemy.Column(sqlalchemy.String)
    kana_house_numbers = sqlalchemy.Column(sqlalchemy.String)
