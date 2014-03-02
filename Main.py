import numpy
import os
import pandas
import pandasql
import pdb

################################################################################
# initialize variables & import data
################################################################################
Kaggle = {}  # dictionary storing DataFrames of data from Kaggle.com
KenPom = {}  # dictionary storing DataFrames of data from KenPom.com
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
    def __init__(self, id, years):
        self.id = id
        self.years = years
        self.tournament_year = self.years.split("-")[1]

        self.day_zero = None
        self.regions = {}
        self.teams = {}  # dictionary storing Team objects, indexed by team_id

    def __str__(self):
        string = self.years
        for team in self.teams.values():
            string += "\n\t" + str(team)
        return string

    def populate_teams(self):
        df = Kaggle['tourney_seeds']
        tourney_teams = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_teams.iterrows():
            # define variables relevant to Team
            team_id = int(row.team)
            df = Kaggle['teams']
            team_name = df[df.id == team_id].name.iloc[0]
            tourney_seed = row.seed
            division = self.regions[tourney_seed[0]]
            division_seed = tourney_seed[1:]

            # create Team object
            team_object = Team(years=self.years, id=team_id, name=team_name)
            team_object.division = division
            team_object.division_seed = division_seed
            team_object.get_kenpom()

            # add Team to self.teams dictionary
            self.teams[team_id] = team_object


class Team(object):
    def __init__(self, years, id, name):
        self.years = years
        self.tournament_year = self.years.split("-")[1]
        self.id = id
        self.name = name
        self.division = None
        self.division_seed = None

        self.kenpom_data_frame = pandas.DataFrame
        self.pythag = None

    def __str__(self):
        attribute_list = []
        attribute_list.append(self.name.ljust(20))
        attribute_list.append(("year: %s" % self.tournament_year).ljust(10))
        attribute_list.append(("id: %s" % self.id).ljust(10))
        if self.division:
            attribute_list.append(("division: %s" % self.division).ljust(20))
        if self.division_seed:
            attribute_list.append(("seed: %s" % self.division_seed).ljust(10))
        if self.pythag:
            attribute_list.append("Pythag: %s" % self.pythag)
        return "| ".join(attribute_list)

    def get_kenpom(self):
        file_name = 'summary%s' % self.tournament_year[-2:]
        if file_name in KenPom.keys():
            df = KenPom[file_name]
            self.kenpom_data_frame = df[df.TeamId == self.id]  # single row from summaryXX.csv for this team
            if not self.kenpom_data_frame.empty:
                self.pythag = self.kenpom_data_frame.Pythag.iloc[0]
            else:
                raise Exception("KenPom data not found for team name:%s, id:%s" % (self.name, self.id))


for _, row in Kaggle['seasons'].iterrows():
    #pdb.set_trace()
    # create Season object
    season = Season(id=row['season'], years=row['years'])
    season.day_zero = row['dayzero']
    season.regions = {
        "W": row['regionW'],
        "X": row['regionX'],
        "Y": row['regionY'],
        "Z": row['regionZ']
    }
    # create Team objects within Season
    season.populate_teams()
    print(season)