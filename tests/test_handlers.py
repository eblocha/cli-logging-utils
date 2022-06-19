import contextlib
import io
import logging
import unittest
from click.testing import CliRunner
from styled_logging import logging_context, create_console_handler, create_file_handler


class TestConsoleHandler(unittest.TestCase):
    def test_logs_to_stderr(self):
        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with logging_context(
                handlers=[
                    create_console_handler(
                        level=logging.INFO,
                        formatter=logging.Formatter("%(message)s"),
                    )
                ]
            ):
                logging.info("message")

                self.assertEqual(buf.getvalue().strip(), "message")


class TestFileHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = CliRunner()

    def test_logs_to_file(self):
        filename = "log.log"
        with self.runner.isolated_filesystem():
            with logging_context(
                handlers=[
                    create_file_handler(
                        filename,
                        level=logging.INFO,
                        formatter=logging.Formatter("%(message)s"),
                    )
                ]
            ):
                logging.info("message")
            
            with open(filename, "r") as f:
                data = f.read().strip()

            self.assertEqual(data, "message")
