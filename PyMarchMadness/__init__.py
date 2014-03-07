#!/usr/bin/env python
import os
import sys

__author__ = "David Casterton"
__email__ = "david.casterton [AT] gmail.com"
__license__ = "GPL"
__version__ = 1


# add base directory to python path
base_dir = os.path.dirname(__file__)
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)