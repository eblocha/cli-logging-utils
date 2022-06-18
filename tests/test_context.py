import logging
import unittest
from styled_logging import logging_context, create_console_handler


class TestLogContext(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)

    def test_resets(self):
        logging.root.setLevel(logging.DEBUG)
        with logging_context(handlers=[create_console_handler(level=logging.INFO)]):
            self.assertEqual(logging.root.level, logging.INFO)

        self.assertEqual(logging.root.level, logging.DEBUG)

    def test_resets_specific_logger(self):
        logging.root.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.DEBUG)
        with logging_context(
            self.logger, handlers=[create_console_handler(level=logging.INFO)]
        ):
            self.assertEqual(logging.root.level, logging.DEBUG)
            self.assertEqual(self.logger.level, logging.INFO)

        self.assertEqual(logging.root.level, logging.DEBUG)
        self.assertEqual(self.logger.level, logging.DEBUG)

    def test_sets_to_lowest(self):
        logging.root.setLevel(logging.DEBUG)
        with logging_context(
            handlers=[
                create_console_handler(level=logging.WARNING),
                create_console_handler(level=logging.INFO),
            ],
        ):
            self.assertEqual(logging.root.level, logging.INFO)

        self.assertEqual(logging.root.level, logging.DEBUG)
