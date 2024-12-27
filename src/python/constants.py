import os
import sys
import logging
from datetime import timedelta
from enum import StrEnum

from semantic_version import Version

class TimeFormats(StrEnum):
    Static_Timer  = '%Y-%m-%d %I:%M:%S'
    Finished_Date = '%B %d @ %I:%M %p'
    Saved_Date    = '%Y-%m-%d %H:%M:%S'


# Used for debugging, flag to see if program is ran through the main.py script or an exe
# This is used for when dealing with files that are packaged within the exe such as guide.html
IS_SCRIPT: bool = not getattr(sys, 'frozen', False)

# checks directory for debug file, if present, logging level is set to debug
DEBUG_MODE = os.path.isfile('DEBUG_MODE')

# Loading paths, using `os.curdir` instead of `os.dirname(__file__)` because the file dir is in a temp dir
ROOT = os.path.abspath(os.path.dirname(__file__)) if not IS_SCRIPT else os.path.join(os.path.abspath(os.getcwd()), 'src', 'python')
CONFIG = os.path.abspath('config.ini')
SAVEFILE = os.path.abspath('save.txt')
ICON = os.path.join(ROOT, 'icon.ico')
GUIDE = os.path.join(ROOT, 'guide.html')

# Date Values
ZERO = timedelta(days=0, hours=0, seconds=0)
ONE = timedelta(seconds=1)

# Program Info
VERSION = Version(major=2, minor=2, patch=0)
PROGRAM_NAME = 'Genshin Stopwatch'

# Object Names
MAIN_WINDOW = 'mw'
SYS_TRAY = 'System Tray'
TOOLBAR = 'tb'

#initialize logger
LOGGER = logging.getLogger('Genshin Stopwatch')
if os.path.isfile('debug.log') == False:
    open('debug.log', 'w').close()
if DEBUG_MODE:
    logLevel = logging.DEBUG
else:
    logLevel = logging.INFO
logging.basicConfig(filename='debug.log', encoding='utf-8', level=logLevel)
LOGGER.debug('Loaded constants.py')