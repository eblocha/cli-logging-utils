import functools
import logging
import textwrap
from typing import Type
from pretty_traceback.formatting import exc_to_traceback_str

from .types import TFormatter


def prettify(cls: Type[TFormatter] = None, /, *, color=True, indent=4) -> Type[TFormatter]:
    """Decorator to prettify a logging.Formatter exception output"""

    def wrap(cls: Type[TFormatter]):
        @functools.wraps(cls, updated=())
        class PrettyFormatter(cls):
            def formatException(self, ei):
                _, exc_value, traceback = ei
                return textwrap.indent(
                    exc_to_traceback_str(exc_value, traceback, color=color),
                    " " * indent,
                )

            def format(self, record: logging.LogRecord):
                record.exc_text = None
                return super().format(record)

        return PrettyFormatter

    # See if we're being called as @prettify or @prettify().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @prettify without parens.
    return wrap(cls)
