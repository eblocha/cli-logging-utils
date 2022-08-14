import logging
import unittest

from styled_logging.decorator import prettify


class TestPrettifyDecorator(unittest.TestCase):
    def test_no_parens(self):
        @prettify
        class MyFormatter(logging.Formatter):
            pass

        self.assertIsNot(MyFormatter.formatException, logging.Formatter.formatException)

    def test_parens(self):
        @prettify()
        class MyFormatter(logging.Formatter):
            pass

        self.assertIsNot(MyFormatter.formatException, logging.Formatter.formatException)
