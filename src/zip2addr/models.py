# Copyright (C) 2023 Satoru SATOH <satoru.satoh at gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=too-few-public-methods
#
"""Data models.

.. seealso::
   https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
"""
import sqlalchemy
import sqlalchemy.orm

from . import db


class Address(db.Base):
    """A model represents a database of addresses.
    """
    __tablename__ = "addresses"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    pref = sqlalchemy.Column(sqlalchemy.String)
    city_ward = sqlalchemy.Column(sqlalchemy.String)
    house_numbers = sqlalchemy.Column(sqlalchemy.String)

    kana = sqlalchemy.orm.relationship(
        "KanaAddress", back_populates="address", uselist=False
    )
    roman = sqlalchemy.orm.relationship(
        "RomanAddress", back_populates="address", uselist=False
    )
    zipcode = sqlalchemy.orm.relationship(
        "Zipcode", back_populates="address", uselist=False
    )


class KanaAddress(db.Base):
    """A model represents a database of kana addresses.
    """
    __tablename__ = "kana_addresses"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    pref = sqlalchemy.Column(sqlalchemy.String)
    city_ward = sqlalchemy.Column(sqlalchemy.String)
    house_numbers = sqlalchemy.Column(sqlalchemy.String)

    address_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("addresses.id")
    )
    address = sqlalchemy.orm.relationship(
        "Address", back_populates="kana", uselist=False
    )


class RomanAddress(db.Base):
    """A model represents a database of roman addresses.
    """
    __tablename__ = "roman_addresses"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    pref = sqlalchemy.Column(sqlalchemy.String)
    city_ward = sqlalchemy.Column(sqlalchemy.String)
    house_numbers = sqlalchemy.Column(sqlalchemy.String)

    address_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("addresses.id")
    )
    address = sqlalchemy.orm.relationship(
        "Address", back_populates="roman", uselist=False
    )


class Zipcode(db.Base):
    """A model represents a database of zip codes.
    """
    __tablename__ = "zipcodes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    zipcode = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    address_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("addresses.id")
    )
    address = sqlalchemy.orm.relationship(
        "Address", back_populates="zipcode", uselist=False
    )

    def as_dict(self):
        """Represents self as a dict object.

        .. todo:: https://docs.sqlalchemy.org/en/14/orm/dataclasses.html
        """
        def get_addr_child_attr(child: str, attr: str):
            """Get an address' child's attr.
            """
            # .. todo:: SAWarning: Multiple rows returned with uselist=False...
            child = getattr(self.address, child, None)
            return "" if child is None else getattr(child, attr)

        return dict(
            zipcode=self.zipcode,

            pref=self.address.pref,
            city_ward=self.address.city_ward,
            house_numbers=self.address.house_numbers,

            roman_pref=get_addr_child_attr("roman", "pref"),
            roman_city_ward=get_addr_child_attr("roman", "city_ward"),
            roman_house_numbers=get_addr_child_attr("roman", "house_numbers"),

            kana_pref=get_addr_child_attr("kana", "pref"),
            kana_city_ward=get_addr_child_attr("kana", "city_ward"),
            kana_house_numbers=get_addr_child_attr("kana", "house_numbers")
        )
