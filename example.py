import logging
from pretty_log import (
    logging_context,
    create_file_handler,
    create_console_handler,
)


if __name__ == "__main__":

    with logging_context(
        console_handler=create_console_handler(level=logging.DEBUG),
        extra_handlers=[create_file_handler("test.log")],
    ):
        try:
            logging.debug("A debug message")
            logging.info("An info message")
            logging.warning("A warning message")
            logging.error("An error message")
            raise ValueError("A critical message from an exception")
        except Exception as exc:
            logging.critical(str(exc), exc_info=True)