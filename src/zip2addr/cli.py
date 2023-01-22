# Copyright (C) 2023 Satoru SATOH <satoru.satoh at gmail.com>
# SPDX-License-Identifier: MIT
"""CLI frontend to manage database files.
"""
import pathlib

import click

from . import constants, datagen


@click.group()
def main():
    """main entry point.
    """


# ref.
# - https://click.palletsprojects.com/en/8.1.x/options/#multi-value-options
@main.command()
@click.option("--datadir", "-d", default='.')
@click.option("--output", "-o", default=constants.DATABASE_FILEPATH)
@click.option(
    "--zip-filenames", "-Z", nargs=2,
    default=constants.ZIPCODE_ZIP_FILENAMES
)
@click.option(
    "--csv-filenames", "-C", nargs=2,
    default=constants.ZIPCODE_CSV_FILENAMES
)
def initdb(
    datadir: str, output: str,
    zip_filenames: tuple[str, str],
    csv_filenames: tuple[str, str],
):
    """Prase csv files and dump its result as a database file.
    """
    opath = pathlib.Path(output)
    (outdir, outname) = (opath.parent, opath.name)

    datagen.make_database_from_zip_files(
        pathlib.Path(datadir), outdir, zip_filenames=zip_filenames,
        csv_filenames=csv_filenames, outname=outname
    )
