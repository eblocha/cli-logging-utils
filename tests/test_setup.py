import contextlib
import io
import logging
import unittest
from click.testing import CliRunner
from styled_logging import setup


class TestSetupConsole(unittest.TestCase):
    def test_logs_to_stderr(self):
        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            setup()

            logging.info("message")

            self.assertIn("message", buf.getvalue().strip())

    def test_changes_log_level(self):
        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            setup(console_level=logging.WARNING)

            logging.info("message")
            logging.warning("warning")

            s = buf.getvalue().strip()
            self.assertIn("warning", s)
            self.assertNotIn("message", s)


class TestSetupFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = CliRunner()

    def test_logs_to_file(self):
        filename = "log.log"
        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.runner.isolated_filesystem():
                setup(filename=filename)
                logging.warning("message")

                with open(filename, "r") as f:
                    data = f.read().strip()

                self.assertIn("message", data)
                self.assertIn("message", buf.getvalue().strip())
    
    def test_changes_file_level(self):
        filename = "log.log"
        with io.StringIO() as buf, contextlib.redirect_stderr(buf):
            with self.runner.isolated_filesystem():
                setup(filename=filename, file_level=logging.ERROR)
                logging.warning("message")
                logging.error("error")

                with open(filename, "r") as f:
                    data = f.read().strip()

                self.assertNotIn("message", data)
                self.assertIn("error", data)
                self.assertIn("message", buf.getvalue().strip())
