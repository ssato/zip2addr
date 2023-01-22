"""Some tiny utility routines.

pylint: disable=bare-except
"""
import logging
import os

from . import constants


def get_logger(name: str = constants.NAME):
    """Get logger instance.
    """
    return logging.getLogger(name)


def set_verbose_mode():
    """Make it running in verbose mode.
    """
    get_logger().setLevel(logging.INFO)


def is_verbose_mode():
    """Detect if it's running in verbose mode.
    """
    return get_logger().level >= logging.INFO


def get_term_lines():
    """
    Get and return the lines in terminal.
    """
    try:
        return os.get_terminal_size().lines
    except BaseException:
        return 50
