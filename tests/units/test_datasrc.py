# Copyright (C) 2023 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import time

import pytest

from zip2addr import datasrc as TT


@pytest.mark.parametrize(
    ("suffix", ),
    (("backup", ),
     (f"{str(time.time()).replace('.', '_')}", ),
     )
)
def test_backup_if_it_exists(suffix, tmp_path):
    filename = "test.json"
    original = tmp_path / filename
    backup = tmp_path / f"{filename}.{suffix}"

    assert not original.exists()
    TT.backup_if_it_exists(original, suffix=suffix)
    assert not backup.exists()

    original.touch()
    assert original.exists()
    TT.backup_if_it_exists(original, suffix=suffix)
    assert backup.exists()
