PyMarchMadness Overview
=============

####Input Data Sources:
- [**Kaggle**] (http://www.kaggle.com/c/march-machine-learning-mania/data)
- [**BracketScience**] (http://wp.bracketscience.com/)
- [**KenPom**] (http://kenpom.com/)

####Python Files:
- **__ini__.py :**
 - Generates win probabilities for all possible matchups in each years March Madness tournament.
 - Generates March Madness Tournament predictions.
- **AnalysisBase.py :** Analysis base class.
- **Analysis/ :** Analysis derived classes, each class implements a distinct analysis method.
- **Constants.py :** Loads input data files and defines constant values.
- **Season.py :** Season & Tournament classes representing 1 NCAA basketball season.
- **Team.py :** Team class representing 1 NCAA basketball Team for 1 season.
- **WrangleKenPom.py :** Generates InputData/KenPomWithIds/ directory, which adds TeamId column to all files from InputData/KenPom/.

####Usage:
    python Main.py
