import logging
from typing import Sequence

from .handlers import create_console_handler


class LoggingContext:
    """A context manager that will change the log settings temporarily"""

    def __init__(
        self,
        logger: logging.Logger = None,
        level: int = None,
        handler: logging.Handler = None,
        close: bool = True,
    ):
        self.logger = logger or logging.root
        self.level = level
        self.handler = handler
        self.close = close

    def __enter__(self):
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)

        if self.handler:
            self.logger.addHandler(self.handler)

    def __exit__(self, *exc_info):
        if self.level is not None:
            self.logger.setLevel(self.old_level)

        if self.handler:
            self.logger.removeHandler(self.handler)

        if self.handler and self.close:
            self.handler.close()


class MultiContext:
    """Can be used to dynamically combine context managers"""

    def __init__(self, *contexts) -> None:
        self.contexts = contexts

    def __enter__(self):
        return tuple(ctx.__enter__() for ctx in self.contexts)

    def __exit__(self, *exc_info):
        for ctx in self.contexts:
            ctx.__exit__(*exc_info)


def logging_context(
    logger: logging.Logger = None,
    console_handler: logging.Handler = None,
    extra_handlers: Sequence[logging.Handler] = None,
):
    """
    Create a logging context

    Parameters
    ----------
    logger : logging.Logger, default None
        The logger to configure, defaults to the root logger
    console_handler : logging.Handler = None
        The handler to use for printing to the console.
        If None, creates a hander with the default parameters.
    extra_handlers : sequence logging.Handler, default None
        Additional handlers to use
        Create a file handler with cli_logging_utils.create_file_handler
    """
    console_handler = console_handler or create_console_handler()
    extra_handlers = extra_handlers or []

    if extra_handlers:
        min_level = min(console_handler.level, min(h.level for h in extra_handlers))
    else:
        min_level = console_handler.level

    contexts = [
        LoggingContext(logger=logger, level=min_level),
        LoggingContext(logger=logger, handler=console_handler, close=False),
    ]

    contexts.extend(
        LoggingContext(logger=logger, handler=handler) for handler in extra_handlers
    )

    return MultiContext(*contexts)
