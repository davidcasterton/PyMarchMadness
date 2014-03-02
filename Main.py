import numpy
import os
import pandas
import pandasql
import pdb

# ----- initialize variables
Kaggle = {}  # dictionary storing DataFrames of data from Kaggle.com
KenPom = {}  # dictionary storing DataFrames of data from KenPom.com

# ----- import data from .csv files into DataFrames
# Kaggle data from http://www.kaggle.com/c/march-machine-learning-mania/data
Kaggle['regular_season_results'] = pandas.read_csv('Kaggle/regular_season_results.csv')
Kaggle['seasons'] = pandas.read_csv('Kaggle/seasons.csv')
Kaggle['teams'] = pandas.read_csv('Kaggle/teams.csv')
Kaggle['tourney_results'] = pandas.read_csv('Kaggle/tourney_results.csv')
Kaggle['tourney_seeds'] = pandas.read_csv('Kaggle/tourney_seeds.csv')
Kaggle['tourney_slots'] = pandas.read_csv('Kaggle/tourney_slots.csv')
# KenPom data from http://kenpom.com/
for file_type in ['defense', 'misc', 'offense', 'summary']:
    for year_int in range(3, 14):
        file_name = '%s%02d' % (file_type, year_int)
        file_path = os.path.join('KenPomWithIds', file_name) + '.csv'
        KenPom[file_name] = pandas.read_csv(file_path)


class Season(object):
    def __init__(self, id, years, day_zero, region_w, region_x, region_y, region_z):
        self.id = id
        self.years = years
        self.tournament_year = self.years.split("-")[1]
        self.day_zero = day_zero
        self.regions = {
            "W": region_w,
            "X": region_x,
            "Y": region_y,
            "Z": region_z
        }
        self.teams = {}  # dictionary storing Team objects

    def __str__(self):
        string = self.years
        for team in self.teams.values():
            string += "\n\t" + str(team)
        return string

    def populate_teams(self):
        df = Kaggle['tourney_seeds']
        tourney_teams = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_teams.iterrows():
            team_id = int(row.team)
            df = Kaggle['teams']
            team_name = df[df.id == team_id].name.iloc[0]
            tourney_seed = row.seed
            division = self.regions[tourney_seed[0]]
            division_seed = int(tourney_seed[1:])

            team_object = Team(years=self.years, id=team_id, name=team_name)
            team_object.division = division
            team_object.division_seed = division_seed
            self.teams[team_name] = team_object


class Team(object):
    def __init__(self, years, id, name):
        self.years = years
        self.tournament_year = self.years.split("-")[1]
        self.id = id
        self.name = name
        self.division = None
        self.division_seed = None

    def __str__(self):
        attribute_list = []
        attribute_list.append(self.name.ljust(20))
        attribute_list.append(("year: %s" % self.tournament_year).ljust(10))
        attribute_list.append(("id: %s" % self.id).ljust(10))
        if self.division:
            attribute_list.append(("division: %s" % self.division).ljust(20))
        if self.division_seed:
            attribute_list.append(("seed: %s" % self.division_seed).ljust(10))
        return "| ".join(attribute_list)


pdb.set_trace()
for _, row in Kaggle['seasons'].iterrows():
    season = Season(id=row['season'], years=row['years'], day_zero=row['dayzero'], region_w=row['regionW'],
                    region_x=row['regionX'], region_y=row['regionY'], region_z=row['regionZ'])
    season.populate_teams()
    print(season)