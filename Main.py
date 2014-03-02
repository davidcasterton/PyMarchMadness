import numpy
import os
import pandas
import pandasql
import pybrain
import pdb

import Constants


class Season(object):
    """
    Season objects represent 1 NCAA backetball season.

    @param id       string  season identifier, defined in Kaggle/seasons.csv season column
    @param years    string  2 years that NCAA season spans in format 'XXXX-YYYY'
    """
    def __init__(self, id, years, day_zero):
        # save input variables to class member variables
        self.id = id
        self.years = years
        self.tournament_year = self.years.split("-")[1]
        self.day_zero = day_zero

        # initialize member variables to be defined after constructor
        self.regions = {}  # dictionary of region names, indexed by region id
        self.teams = {}  # dictionary of Team objects, indexed by team_id
        self.tournament_bracket = Constants.TOURNAMET_BRACKET

    def __str__(self):
        # define how Season object will look if printed
        string = self.years
        for team in self.teams.values():
            string += "\n\t" + str(team)
        return string

    def set_regions(self, region_w, region_x, region_y, region_z):
        self.regions = {
            "W": region_w,
            "X": region_x,
            "Y": region_y,
            "Z": region_z,
        }

    def build_teams(self):
        """
        Build Team objects for this season from KAGGLE_DATA.
        """
        df = Constants.KAGGLE_DATA['tourney_seeds']
        tourney_teams = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_teams.iterrows():
            # define variables relevant to Team
            team_id = int(row.team)
            df = Constants.KAGGLE_DATA['teams']
            team_name = df[df.id == team_id].name.iloc[0]
            tourney_seed = row.seed

            # create Team object
            team_object = Team(id=team_id, name=team_name, years=self.years)
            team_object.set_tourney_seed(tourney_seed)
            team_object.retrieve_kenpom()

            # add Team object to self.teams dictionary
            self.teams[team_id] = team_object

    def run_tournament(self):
        df = Constants.KAGGLE_DATA['tourney_slots']
        tourney_slots = df[df.season == self.id]  # slice of tourney_slots DataFrame for current season


class Team(object):
    """
    Team object representing 1 NCAA backetball team for 1 NCAA season.

    @param years    string  2 years that NCAA season spans in format 'XXXX-YYYY'
    @param id       string  team identifier, defined in Kaggle/teams.csv id column
    @param name     string  team name, defined in Kaggle/teams.csv name column
    """
    def __init__(self, id, name, years):
        # save input variables to class member variables
        self.id = id
        self.name = name
        self.years = years
        self.tournament_year = self.years.split("-")[1]

        # initialize member variables to be defined in set/retrieve methods
        self.tourney_seed = None
        self.division = None
        self.division_seed = None
        self.kenpom_data_frame = pandas.DataFrame
        self.pythag = None

    def __str__(self):
        # define how team object will look if printed
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

    def set_tourney_seed(self, tourney_seed):
        self.tourney_seed = tourney_seed
        self.division = self.regions[tourney_seed[0]]
        self.division_seed = tourney_seed[1:]

    def retrieve_kenpom(self):
        """
        Retrieve KenPom statistics for this team from KENPOM_DATA.
        """
        file_name = 'summary%s' % self.tournament_year[-2:]
        if file_name in Constants.KENPOM_DATA.keys():
            df = Constants.KENPOM_DATA[file_name]
            self.kenpom_data_frame = df[df.TeamId == self.id]  # single row from summaryXX.csv for this team
            if not self.kenpom_data_frame.empty:
                self.pythag = self.kenpom_data_frame.Pythag.iloc[0]
            else:
                raise Exception("KenPom data not found for team name:%s, id:%s" % (self.name, self.id))


if __name__ == "__main__":
    for _, row in Constants.KAGGLE_DATA['seasons'].iterrows():
        # create Season object
        season = Season(id=row['season'], years=row['years'], day_zero =row['dayzero'])
        season.set_regions(region_w=row['regionW'], region_x=row['regionX'], region_y=row['regionY'], region_z=row['regionZ'])
        # create Team objects within Season
        season.build_teams()
        # run tournament
        season.run_tournament()
        print(season)