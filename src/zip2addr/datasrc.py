"""zip code data management.
"""
import csv
import pathlib
import typing


def parse(row: list[str]) -> dict[

def load(filepath: str) -> typing.Iterator[list[int]]:
    """Load zip code data in csv format.
    """
    with open(filepath, encoding='shift_jis') as csvf:
        for row in csv.reader(csvf):
            yield parse(row)
