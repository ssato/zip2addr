# Copyright (C) 2023 Satoru SATOH <satoru.satoh at gmail.com>
# SPDX-License-Identifier: MIT
"""CLI frontend to manage database files.
"""
import pprint

import click

from . import constants, iapi, utils


@click.group()
@click.option("--verbose/--quiet", "-v/-q", default=False)
def main(verbose: bool):
    """main entry point.
    """
    if verbose:
        iapi.set_verbose_mode()


# ref.
# https://click.palletsprojects.com/en/8.1.x/options/#multi-value-options
# https://click.palletsprojects.com/en/8.1.x/utils/#pager-support
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
    """
    Prase csv files extracted from zip files, save resutl data as a db file.
    """
    iapi.initdb(
        datadir, output,
        zip_filenames=zip_filenames, csv_filenames=csv_filenames
    )


@main.command()
@click.option("--db-path", "-d", default=constants.DATABASE_FILEPATH)
@click.argument("zipcode")
def search(db_path: str, zipcode: str):
    """
    Search address info from rhe database file by given zip code.
    """
    res = iapi.search_by_zipcode(zipcode, db_path, limit=0)
    fmt = pprint.pformat

    if len(res) > utils.get_term_lines():
        click.echo_via_pager(fmt(r) for r in res)
    else:
        for zipd in res:
            click.echo(fmt(zipd))
