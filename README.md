PyMarchMadness
=============
###Modular Python framework to analyze the NCAA March Madness tournament.

####Download Site:
- http://davidcasterton.github.io/March-Madness

####Requirements:
  - [Python 2.7] (http://www.python.org/download/releases/2.7/)
  - [Python Packages] (PyMarchMadness/requirements.txt)

####Installation:
    python setup.py install

####Usage:
    python PyMarchMadness
    
####Source Code Documentation:
- http://pymarchmadness.readthedocs.org/

####Source Code Location:
- [PyMarchMadness/] (PyMarchMadness/)

####How To Add New Analysis To Framework:
  - Create an analysis module that inherits from [Analysis.BaseClass] (PyMarchMadness/Analysis/Analysis.py)
  - Implement all methods that were not defined in [Analysis.BaseClass] (PyMarchMadness/Analysis/Analysis.py)
  - Insert analysis module into [PyMarchMadness/Analysis/] (PyMarchMadness/Analysis/)
  - Select new analysis module when prompted at run-time

####How To Add New Input Data:
- Add *\<new_folder\>* into [InputData/] (PyMarchMadness/InputData/)
- Add data files into InputData/*\<new_folder\>*
- Modify [Constants.py] (PyMarchMadness/Constants.py) to load new data files, e.g. KAGGLE_INPUT
