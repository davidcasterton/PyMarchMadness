March-Madness
=============

Python analysis for Kaggle March Madness competition (http://www.kaggle.com/c/march-machine-learning-mania).

InputData Sources:
- Kaggle: http://www.kaggle.com/c/march-machine-learning-mania/data
- BracketScience: http://wp.bracketscience.com/
- KenPom: http://kenpom.com/
- KenPomWithIds: generated from AddKaggleIdToKenPomData.py

Analysis Files:
- Constants.py : Contains unchanging variables.
- AddKaggleIdToKenPomData.py : Generates InputData/KenPomWithIds/ directory, which adds TeamId column to all files from InputData/KenPom/. The TeamId column enables correlation of teams between Kaggle and KenPom files.
- Main.py : 1) Generates win probabilities for all possible matchups in each years NCAA March Madness tournament. 2) Generates NCAA March Madness Bracket predictions.

Software Dependencies:
- Python 2.7
- Python pandas package
