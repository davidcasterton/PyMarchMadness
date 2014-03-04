March-Madness
=============

Python analysis for Kaggle March Madness competition (http://www.kaggle.com/c/march-machine-learning-mania).

####Input Data Sources:
- **Kaggle**: http://www.kaggle.com/c/march-machine-learning-mania/data
- **BracketScience**: http://wp.bracketscience.com/
- **KenPom**: http://kenpom.com/
- **KenPomWithIds**: generated from AddKaggleIdToKenPomData.py

####Analysis Files:
- **Constants.py** : Constant "variables".
- **AddKaggleIdToKenPomData.py** : Generates InputData/KenPomWithIds/ directory, which adds TeamId column to all files from InputData/KenPom/. The TeamId column enables correlation of teams between Kaggle and KenPom files.
- **Main.py** : 1) Generates win probabilities for all possible matchups in each years NCAA March Madness tournament, this is the submission format for the Kaggle competition. 2) Generates NCAA March Madness Bracket predictions.
- **Season.py** : Class representing 1 NCAA season
- **Team.py** : Class representing 1 NCAA Team for 1 season

####Software Dependencies:
- Python 2.7
- Python pandas package
