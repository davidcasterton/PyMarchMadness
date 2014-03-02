import numpy
import os
import pandas
import pandasql
import pdb
import sys

# ----- import data into pandas DataFrames.
# Kaggle data from http://www.kaggle.com/c/march-machine-learning-mania/data
Kaggle = {}
Kaggle['regular_season_results'] = pandas.read_csv('Kaggle/regular_season_results.csv')
Kaggle['seasons'] = pandas.read_csv('Kaggle/seasons.csv')
Kaggle['teams'] = pandas.read_csv('Kaggle/teams.csv')
Kaggle['tourney_results'] = pandas.read_csv('Kaggle/tourney_results.csv')
Kaggle['tourney_seeds'] = pandas.read_csv('Kaggle/tourney_seeds.csv')
Kaggle['tourney_slots'] = pandas.read_csv('Kaggle/tourney_slots.csv')
# KenPom data from http://kenpom.com/
KenPom = {}
for file_type in ['defense', 'misc', 'offense', 'summary']:
    for year_int in range(3, 14):
        file_name = '%s%02d' % (file_type, year_int)
        file_path = os.path.join('KenPom', file_name) + '.csv'
        KenPom[file_name] = pandas.read_csv(file_path)

for year_int in range(3, 14):
    seasons = pandasql.sqldf("SELECT name FROM summary13 WHERE TeamName='%s'" % "Louisville", KenPom)

