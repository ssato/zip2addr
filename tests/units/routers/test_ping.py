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
import fastapi.testclient

from zip2addr import (
    main,
)
from zip2addr.routers import ping as TT


CLIENT = fastapi.testclient.TestClient(main.APP)


def test_ping():
    resp = CLIENT.get("/ping/")
    assert resp.status_code == 200
    assert resp.json() == TT.PING_RESPONSE
