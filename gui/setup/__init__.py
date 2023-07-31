import sys
import time
import logging

"""
    Require Python >= 3.11
"""
if (sys.version_info.major, sys.version_info.minor) < (3, 11):
    logging.critical("Python 3.11 or later is required. Please update your Python installation.")
    time.sleep(60)
