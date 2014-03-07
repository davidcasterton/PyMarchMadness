PyMarchMadness
=============
###Modular Python framework to analyze the NCAA March Madness tournament.

####Information:
- **Code Documentation:** http://pymarchmadness.readthedocs.org/
- **Download Site:** http://davidcasterton.github.io/March-Madness
- **Source Code:** in PyMarchMadness/
- **How To Add New Analysis To Framework:** 
 - Create an analysis module that inherits from Analysis.BaseClass
 - Implement all methods that were not defined in Analysis.BaseClass
 - Insert analysis module into PyMarchMadness/Analysis/
 - Select new analysis module when prompted at run-time

####Software Dependencies:
- [Python 2.7] (http://www.python.org/download/releases/2.7/)
- [Python Pandas] (http://pandas.pydata.org/)

####Installation:
    python setup.py install

####Usage:
    python PyMarchMadness
