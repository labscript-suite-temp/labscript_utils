#####################################################################
#                                                                   #
# /setup_logging.py                                                 #
#                                                                   #
# Copyright 2013, Monash University                                 #
#                                                                   #
# This file is part of labscript_utils, in the labscript suite      #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
from __future__ import division, unicode_literals, print_function, absolute_import

import sys, os
import logging, logging.handlers
import __main__


class LessThanFilter(logging.Filter):
    def __init__(self, less_than):
        self.less_than = less_than
        logging.Filter.__init__(self)
    def filter(self, record):
        return record.levelno < self.less_than


def setup_logging(program_name, log_level=logging.DEBUG, terminal_level=logging.INFO, maxBytes=1024*1024*50, backupCount=1):
    logger = logging.getLogger(program_name)
    # Clear any previously added handlers from the logger:
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    try:
        try:
            program_module = __import__(program_name)
        except ImportError:
            program_module = __import__(program_name.lower())
        main_path = program_module.__file__
    except ImportError:
        main_path = __main__.__file__ if hasattr(__main__, '__file__') else __file__

    log_dir = os.path.dirname(os.path.realpath(main_path))
    log_path = os.path.join(log_dir, '%s.log' % program_name)
    # TODO: Log rotation disabled for the time being, to be restored once multiprocess logging implemented.
    # handler = logging.handlers.FileHandler(log_path, maxBytes=maxBytes, backupCount=backupCount)
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logger.addHandler(handler)
    if sys.stdout is not None and sys.stdout.fileno() >= 0:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(terminal_level)
        logger.addHandler(stdout_handler)
        if sys.stderr is not None and sys.stderr.fileno() >= 0:
            # Send warnings and greater to stderr instead of stdout:
            stdout_handler.addFilter(LessThanFilter(logging.WARNING))
            sterr_handler = logging.StreamHandler(sys.stderr)
            sterr_handler.setFormatter(formatter)
            sterr_handler.setLevel(logging.WARNING)
            logger.addHandler(sterr_handler)
    else:
        # Prevent bug on windows where writing to stdout without a command
        # window causes a crash:
        sys.stdout = sys.stderr = open(os.devnull, 'w')
    logger.setLevel(logging.DEBUG)
    return logger
