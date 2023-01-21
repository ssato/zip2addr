# Copyright (C) 2023 Satoru SATOH <satoru.satoh at gmail.com>
# SPDX-License-Identifier: MIT
"""CLI frontend to manage database files.
"""
import click

from . import constants, datasrc


@click.group()
def main():
    """main entry point.
    """


@main.command()
@main.option("--datadir", "-d", default='.')
@main.option("--roman", "-R", default=constants.ROMAN_ZIPCODE_FILENAME)
@main.option("--kana", "-K", default=constants.KANA_ZIPCODE_FILENAME)
@main.option("--out", "-O", default=constants.JSON_FILEPATH)
def initdb(datadir: str, roman: str, kana: str, out: str):
    """Prase csv files and dump its result as a database file.
    """
    datasrc.make_database_from_csv_files(
        datadir=datadir, roman_filename=roman, kana_filename=kana, outpath=out
    )
