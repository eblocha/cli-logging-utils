import logging

from .formatters import MultiFormatter, PrettyExceptionFormatter


def create_console_handler(
    level: int = logging.INFO,
    formatter: logging.Formatter = None,
):
    """
    Create a logging handler to display messages in the console

    Parameters
    ----------
    level : int, default logging.INFO
        The logging level to set the handler to
    formatter : logging.Formatter, default None
        Can be used to override the formatter.
        If None, uses cli_logging_utils.MultiFormatter
    """
    formatter = formatter or MultiFormatter()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    return console_handler


def create_file_handler(
    path: str,
    level: int = logging.WARNING,
    formatter: logging.Formatter = None,
):
    """
    Create a file handler to log messages to a file

    Parameters
    ----------
    path : path-like
        The path to the log file
    level : int, default logging.WARNING
        Th logging level to set the handler to
    formatter : logging.Formatter, default None
        Can be used to override the formatter.
        If None, uses cli_logging_utils.PrettyExceptionFormatter
    """
    formatter = formatter or PrettyExceptionFormatter(
        "%(levelname)s:%(asctime)s:%(name)s:%(message)s", color=False
    )
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    return file_handler
