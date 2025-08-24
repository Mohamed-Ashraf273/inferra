import logging
import sys

interactive = True


def print_msg(message, line_break=True, level="info"):
    """Print an Inferra message to stdout or logging."""
    global interactive
    if interactive:
        if line_break:
            sys.stdout.write(message + "\n")
        else:
            sys.stdout.write(message)
        sys.stdout.flush()
    else:
        if level == "info":
            logging.info(message)
        elif level == "warning":
            logging.warning(message)
        elif level == "error":
            logging.error(message)
        else:
            logging.debug(message)
