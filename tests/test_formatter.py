import logging
from textwrap import dedent
from typing import Callable
import unittest
from pretty_log import (
    create_console_handler,
    logging_context,
    MultiFormatter,
    PrettyExceptionFormatter,
    DEFAULT_FORMATS as BASE_DEFAULTS,
)

# freeze to prevent the actual defaults from changing the test
DEFAULT_FORMATS = {
    logging.DEBUG: "DEBUG | %(message)s",
    logging.INFO: "INFO | %(message)s",
    logging.WARNING: "WARNING | %(message)s",
    logging.ERROR: "ERROR | %(message)s",
    logging.CRITICAL: "CRITICAL | %(message)s",
}


class TestMultiFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.formatter = MultiFormatter(DEFAULT_FORMATS)
        self.ctx = logging_context(
            self.logger,
            create_console_handler(level=logging.DEBUG, formatter=self.formatter),
        )

    def run_level(self, level: int, log: Callable[[str], None]):
        with self.ctx:
            with self.assertLogs(self.logger, level=level) as cap:
                log("message")

            messages = [self.formatter.format(record) for record in cap.records]
            expected = [DEFAULT_FORMATS[level] % {"message": "message"}]
            self.assertListEqual(messages, expected)

    def test_debug(self):
        self.run_level(logging.DEBUG, self.logger.debug)

    def test_info(self):
        self.run_level(logging.INFO, self.logger.info)

    def test_warning(self):
        self.run_level(logging.WARNING, self.logger.warning)

    def test_error(self):
        self.run_level(logging.ERROR, self.logger.error)

    def test_critical(self):
        self.run_level(logging.CRITICAL, self.logger.critical)


class TestMultiNoFormat(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.formatter = MultiFormatter({})

        self.backup_formatter = PrettyExceptionFormatter()

        self.ctx = logging_context(
            self.logger,
            create_console_handler(level=logging.DEBUG, formatter=self.formatter),
        )

    def test_log(self):
        with self.ctx:
            with self.assertLogs(self.logger) as cap:
                self.logger.info("message")

            messages = [self.formatter.format(record) for record in cap.records]
            expected = [self.backup_formatter.format(record) for record in cap.records]
            self.assertListEqual(messages, expected)


class TestMultiNone(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.formatter = MultiFormatter()
        self.formatter_defaults = MultiFormatter(BASE_DEFAULTS)

        self.ctx = logging_context(
            self.logger,
            create_console_handler(level=logging.DEBUG, formatter=self.formatter),
        )

    def test_log(self):
        with self.ctx:
            with self.assertLogs(self.logger, level=logging.DEBUG) as cap:
                self.logger.debug("message")
                self.logger.info("message")
                self.logger.warning("message")
                self.logger.error("message")
                self.logger.critical("message")

            messages = [self.formatter.format(record) for record in cap.records]
            expected = [
                self.formatter_defaults.format(record) for record in cap.records
            ]
            self.assertListEqual(messages, expected)


class TestPrettyExceptions(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.with_color = PrettyExceptionFormatter()
        self.ctx = logging_context(
            self.logger,
            create_console_handler(level=logging.DEBUG, formatter=self.with_color),
        )

    def test_indents_exception(self):
        """Make sure the exception is indented"""
        with self.ctx:
            with self.assertLogs(self.logger, level=logging.DEBUG) as cap:
                try:
                    raise Exception("error")
                except Exception as e:
                    self.logger.critical(str(e), exc_info=True)

            formatted = self.with_color.format(cap.records[0])
            lines = formatted.splitlines()
            exc_info = "\n".join(lines[1:])
            self.assertNotEqual(exc_info, dedent(exc_info))


class TestMultiplePrettyExceptions(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.with_color = PrettyExceptionFormatter()
        self.without_color = PrettyExceptionFormatter(color=False)
        self.ctx = logging_context(
            self.logger,
            create_console_handler(level=logging.DEBUG, formatter=self.with_color),
            extra_handlers=[
                create_console_handler(
                    level=logging.DEBUG, formatter=self.without_color
                )
            ],
        )

    def test_2_formatters(self):
        """Ensure we don't mangle the records when using 2 pretty exception formatters,
        since they format exceptions differently with and without color"""
        with self.ctx:
            with self.assertLogs(self.logger, level=logging.DEBUG) as cap:
                try:
                    raise Exception("error")
                except Exception as e:
                    self.logger.critical(str(e), exc_info=True)

            with_color = self.with_color.format(cap.records[0])
            without_color = self.without_color.format(cap.records[0])

            self.assertNotEqual(with_color, without_color)
