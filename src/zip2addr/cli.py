# Copyright (C) 2023 Satoru SATOH <satoru.satoh at gmail.com>
# SPDX-License-Identifier: MIT
"""CLI frontend to manage database files.
"""
import click

from . import constants, datasrc


@click.command()
@click.option("--datadir", "-d", default='.')
@click.option("--roman", "-R", default=constants.ROMAN_ZIPCODE_FILENAME)
@click.option("--kana", "-K", default=constants.KANA_ZIPCODE_FILENAME)
@click.option("--out", "-O", default=constants.JSON_FILEPATH)
def make_database(datadir: str, roman: str, kana: str, out: str):
    """Prase csv files and dump its result as a database file.
    """
    datasrc.make_database_from_csv_files(
        datadir=datadir, roman_filename=roman, kana_filename=kana, outpath=out
    )


if __name__ == '__main__':
    make_database()
