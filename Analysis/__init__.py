#!/usr/bin/env python
"""Analysis package, all classes are inherited from AnalysisBase."""

import os
import pdb
import sys

__author__ = 'davidcasterton'
__license__ = "GPL"


# add Analysis directory to python path
analysis_dir = os.path.dirname(__file__)
sys.path.insert(0, analysis_dir)

available = []

for file_name in os.listdir('Analysis'):
    class_name, extension = file_name.split(".")

    # skip __init__ and Parent files
    if extension != "py" or class_name == "__init__" or class_name == "Analysis":
        continue

    exec("from %s import %s" % (class_name, class_name))
    _object = globals()[class_name]
    available.append(_object())

num_available = len(available)