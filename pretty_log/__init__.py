from .handlers import create_console_handler, create_file_handler
from .color import style
from .context import LoggingContext, MultiContext, logging_context
from .formatters import MultiFormatter, PrettyExceptionFormatter, DEFAULT_FORMATS


def setup(filename: str = None):
    if filename:
        file_handler = create_file_handler(filename)

    logging_context(extra_handlers=[file_handler]).__enter__()

__all__ = [
    "create_console_handler",
    "create_file_handler",
    "style",
    "LoggingContext",
    "MultiContext",
    "logging_context",
    "MultiFormatter",
    "PrettyExceptionFormatter",
    "DEFAULT_FORMATS",
    "setup",
]
