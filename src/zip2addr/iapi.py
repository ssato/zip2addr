# Copyright (C) 2023 Satoru SATOH <satoru.satoh at gmail.com>
# SPDX-License-Identifier: MIT
"""Internal APIs used commonly from web ui and cli.
"""
import pathlib
import typing

from . import (
    constants,
    crud,
    datagen,
    db,
    utils
)


def set_verbose_mode():
    """
    Make it more verbose.
    """
    utils.set_verbose_mode()


def initdb(
    datadir: str, output: str,
    zip_filenames: tuple[str, str] = constants.ZIPCODE_ZIP_FILENAMES,
    csv_filenames: tuple[str, str] = constants.ZIPCODE_CSV_FILENAMES
):
    """
    Prase csv files extracted from zip files, save resutl data as a db file.
    """
    opath = pathlib.Path(output)
    (outdir, outname) = (opath.parent, opath.name)

    datagen.make_database_from_zip_files(
        pathlib.Path(datadir), outdir, zip_filenames=zip_filenames,
        csv_filenames=csv_filenames, outname=outname
    )


def search_by_zipcode(
    zipcode: str,
    db_path: str,
    skip: int = 0, limit: int = constants.LIMIT
) -> list[typing.Any]:
    """
    Search address info from rhe database file by given zip code.
    """
    dpath = pathlib.Path(db_path)
    if not dpath.exists():
        utils.get_logger().error(f"Not found: {db_path}")
        return

    with db.get_session(dpath, read_only=True) as dbs:
        res = crud.get_zipcodes_by_partial_zipcode(
            dbs, zipcode, skip=skip, limit=limit
        )
        if not res:
            utils.get_logger().warning(f"Not found {zipcode} in {db_path}")
            return []

        return [r.as_dict() for r in res]
