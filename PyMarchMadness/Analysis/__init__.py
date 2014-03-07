#!/usr/bin/env python
"""Analysis package, all classes are inherited from AnalysisBase."""

import os
import pdb
import sys

# add Analysis/ directory to python path
analysis_dir = os.path.dirname(__file__)
if analysis_dir not in sys.path:
    sys.path.insert(0, analysis_dir)

# import all files in Analysis/
object_list = []  # list of analysis objects
for file_name in os.listdir(analysis_dir):
    class_name, extension = file_name.split(".")

    # skip __init__ and Parent files
    if extension != "py" or class_name == "__init__":
        continue

    # import file
    exec("from %s import %s" % (class_name, class_name))
    _object = globals()[class_name]
    object_list.append(_object())


def get_objects():
    """
    :function: Get list of Analysis objects.
    :returns: list of Analysis objects
    :rtype: list
    """
    return object_list