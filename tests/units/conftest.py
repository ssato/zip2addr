# Copyright (C) 2023 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import pathlib

import pytest


@pytest.fixture(name="my_datadir")
def get_datadir(request) -> pathlib.Path:
    return pathlib.Path(request.fspath).parent.parent / "data"
