PyMarchMadness Overview
=============

####Information:
- **Code Documentation:** http://pymarchmadness.readthedocs.org/
- **Download Site:** http://davidcasterton.github.io/March-Madness
- **File Overview:**
  - **\__main\__.py :**
    - Generates win probabilities for all possible matchups in each years March Madness tournament.
    - Generates March Madness Tournament predictions.
  - **Analysis/ :** Analysis base and derived classes, each derived class implements a distinct analysis method.
    - **Analysis.py :** Analysis base class.
  - **Constants.py :** Loads input data files and defines constant values.
  - **Season.py :** Season & Tournament classes representing 1 NCAA basketball season.
  - **Team.py :** Team class representing 1 NCAA basketball Team for 1 season.
  - **WrangleKenPom.py :** Generates InputData/KenPomWithIds/ directory, which adds TeamId column to all files from InputData/KenPom/.
- **How To Add New Analysis To Framework:** 
  - Create an analysis module that inherits from Analysis.BaseClass
  - Implement all methods that were not defined in Analysis.BaseClass
  - Insert analysis module into PyMarchMadness/Analysis/
  - Select new analysis module when prompted at run-time

####Input Data Sources:
- [**Kaggle**] (http://www.kaggle.com/c/march-machine-learning-mania/data)
- [~~**BracketScience**~~] (http://wp.bracketscience.com/) available for purchase at preceeding link
- [~~**KenPom**~~] (http://kenpom.com/) available for purchase at preceeding link

####Usage:
    python PyMarchMadness
