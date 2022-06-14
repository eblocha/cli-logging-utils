import logging
import typing as t
from textwrap import indent
from pretty_traceback.formatting import exc_to_traceback_str

from .color import style


DEFAULT_FORMATS = {
    logging.DEBUG: style("DEBUG", fg="cyan") + " | " + style("%(message)s", fg="cyan"),
    #
    logging.INFO: "%(message)s",
    #
    logging.WARNING: style("WARN ", fg="yellow")
    + " | "
    + style("%(message)s", fg="yellow"),
    #
    logging.ERROR: style("ERROR", fg="red") + " | " + style("%(message)s", fg="red"),
    #
    logging.CRITICAL: style("FATAL", fg="white", bg="red", bold=True)
    + " | "
    + style("%(message)s", fg="red", bold=True),
}


class PrettyExceptionFormatter(logging.Formatter):
    """Uses pretty-traceback to format exceptions. Set color=False when logging to a file."""

    def __init__(self, *args, color=True, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color

    def formatException(self, ei):
        _, exc_value, traceback = ei
        return exc_to_traceback_str(exc_value, traceback, color=self.color)

    def format(self, record: logging.LogRecord):
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        s = self.formatMessage(record)

        if record.exc_info:
            # Don't assign to exc_text here, since we don't want to inject color all the time
            if s[-1:] != "\n":
                s += "\n"
            # Add indent to indicate the traceback is part of the previous message
            text = indent(self.formatException(record.exc_info), " " * 4)
            s += text

        return s


class MultiFormatter(PrettyExceptionFormatter):
    """
    Format log messages differently for each log level

    Parameters
    ----------
    formats : dict of int to str
        This is a mapping of log level to format string.
        If a level is omitted, the base logging.Formatter will be used for that level.
    kwargs : dict
        Keyword arguments to forward to logging.Formatter.
    """

    def __init__(self, formats: t.Dict[int, str] = None, **kwargs):
        base_format = kwargs.pop("fmt", None)
        super().__init__(base_format, **kwargs)

        formats = formats or DEFAULT_FORMATS

        self.formatters = {
            level: PrettyExceptionFormatter(fmt, **kwargs)
            for level, fmt in formats.items()
        }

    def format(self, record: logging.LogRecord):
        formatter = self.formatters.get(record.levelno)

        if formatter is None:
            return super().format(record)

        return formatter.format(record)
