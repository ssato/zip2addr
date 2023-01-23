# coding: utf-8
#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
#
# .. seealso::
#    https://fastapi.tiangolo.com/tutorial/testing/
#
import shutil
import typing

import fastapi
import fastapi.testclient
import sqlalchemy
import pytest

from zip2addr import (
    constants,
    db,
    main,
)
# from zip2addr.routers import zipcode as TT


CLIENT = fastapi.testclient.TestClient(main.APP)


@pytest.fixture(scope="function", name="my_db")
def db_session(my_datadir, tmp_path):
    """
    .. seealso::

       - https://fastapi.tiangolo.com/ja/advanced/testing-database/
       - zip2addr.db.get_session_ctx
    """
    db_path = tmp_path / constants.DATABASE_FILENAME
    shutil.copyfile(my_datadir / constants.DATABASE_FILENAME, db_path)

    dbs = db.get_session_class(db_path)()

    def get_session():
        """For tests.
        """
        try:
            yield dbs
        except sqlalchemy.exc.SQLAlchemyError as exc:
            assert exc is not None
            dbs.rollback()
        finally:
            dbs.rollback()
            dbs.close()

    main.APP.dependency_overrides[
        db.get_default_session
    ] = get_session

    yield dbs


def test_get_zipcodes(my_db):
    resp = CLIENT.get("/zipcodes/")
    assert resp.status_code == 200
    assert resp.json()


def dicts_have_same_key_value_pairs(
    lhs: dict, rhs: dict,
    keys: typing.Optional[tuple[str]] = None
) -> bool:
    """Test if dicts have same key and value pairs.

    .. note::

        It's not true always lhs == rhs because rhs may have key and value
        pairs lhs does not have.
    """
    if keys is None:
        keys = lhs.keys()

    for key in keys:
        if key not in lhs:
            return False

        if key not in rhs or rhs[key] != lhs[key]:
            return False

    return True


# .. seealso:: Actual zipcode data, e.g. *.csv, in tests/data/.
@pytest.mark.parametrize(
    ("zipcode", "status_code", "expected"),
    (("0000000", fastapi.status.HTTP_404_NOT_FOUND, None),
     ("9071801", fastapi.status.HTTP_200_OK,
      dict(
          zipcode="9071801",
          pref="沖縄県",
          city_ward="八重山郡　与那国町",
          house_numbers="与那国",
          roman_pref="OKINAWA KEN",
          roman_city_ward="YAEYAMA GUN YONAGUNI CHO",
          roman_house_numbers="YONAGUNI",
          kana_pref="ｵｷﾅﾜｹﾝ",
          kana_city_ward="ﾔｴﾔﾏｸﾞﾝﾖﾅｸﾞﾆﾁｮｳ",
          kana_house_numbers="ﾖﾅｸﾞﾆ",
      )),
     )
)
def test_get_zipcode(zipcode, status_code, expected, my_db):
    """
    .. todo::

       - Use response_model
       - Make the API returns all of address info along with zipcode
        - Maybe we should normalize the data in database files.
    """
    resp = CLIENT.get(f"/zipcodes/{zipcode}")
    assert resp.status_code == status_code
    if expected is not None:
        # assert expected == resp.json()
        assert dicts_have_same_key_value_pairs(
            expected, resp.json(),
            ("zipcode", "pref")
        )


@pytest.mark.parametrize(
    ("partial_zipcode", "min_n_results"),
    (("000", -1),
     ("907", 1),
     )
)
def test_get_zipcodes_by_partial_zipcode(
    partial_zipcode, min_n_results, my_db
):
    resp = CLIENT.get(f"/zipcodes/partial/{partial_zipcode}")
    assert resp.status_code == fastapi.status.HTTP_200_OK
    if min_n_results < 0:
        assert not resp.json()
    else:
        assert len(resp.json()) >= min_n_results
