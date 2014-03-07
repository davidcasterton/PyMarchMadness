import os
import sys

dirname = os.path.dirname(__file__)
sys.path.insert(0, dirname)

import Analysis
import Constants
import Main
import Season
import Team

__version__ = Constants.VERSION