March-Madness
=============

Python analysis for Kaggle March Madness competition (http://www.kaggle.com/c/march-machine-learning-mania).

####Usage:
python Main.py

####Input Data Sources:
- **Kaggle:** http://www.kaggle.com/c/march-machine-learning-mania/data
- **BracketScience:** http://wp.bracketscience.com/
- **KenPom:** http://kenpom.com/
- **KenPomWithIds:** generated from AddKaggleIdToKenPomData.py

####Analysis Files:
- **Analysis.py:** Analysis classes. Changing classes enables easy switching between analysis methods.
- **Constants.py:** Constant "variables".
- **Main.py:** 1) Generates win probabilities for all possible matchups in each years March Madness tournament, this is the submission format for the Kaggle competition. 2) Generates March Madness Bracket predictions.
- **Misc.py:** helper functions.
- **Season.py:** Season & Bracket classes representing 1 NCAA basketball season
- **Team.py:** Team class representing 1 NCAA basketball Team for 1 season
- **WrangleKenPom.py:** Generates InputData/KenPomWithIds/ directory, which adds TeamId column to all files from InputData/KenPom/. The TeamId column enables correlation of teams between Kaggle and KenPom files.

####Software Dependencies:
- Python 2.7
- Python pandas package
