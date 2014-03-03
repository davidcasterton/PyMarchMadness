import csv
import numpy
import os
import pandas
import pandasql
import pprint
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
        self.tournament_bracket = Constants.TOURNAMENT_BRACKET
        self.max_offense_efficiency = 0
        self.max_defense_efficiency = 0
        self.min_offense_efficiency = 200
        self.min_defense_efficiency = 200

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
            team_object.set_tourney_seed(tourney_seed=tourney_seed, regions=self.regions)
            team_object.retrieve_kenpom()
            self.add_team(team_object)

    def add_team(self, team_object):
        # add Team object to self.teams dictionary
        self.teams[team_object.id] = team_object

        # check offensive and defensive efficiency against max/min's
        if team_object.offense_efficiency > self.max_offense_efficiency:
            self.max_offense_efficiency = team_object.offense_efficiency
        if team_object.defense_efficiency > self.max_defense_efficiency:
            self.max_defense_efficiency = team_object.defense_efficiency
        if team_object.offense_efficiency < self.min_offense_efficiency:
            self.min_offense_efficiency = team_object.offense_efficiency
        if team_object.defense_efficiency < self.min_defense_efficiency:
            self.min_defense_efficiency = team_object.defense_efficiency

    def build_bracket(self):
        """
        Populate predicted NCAA March Madness bracket.
        """
        if self.tournament_year < "2003":
            print("Cannot generate Bracket for year '%s', do not have KenPom data." % self.tournament_year)
            return

        df = Constants.KAGGLE_DATA['tourney_slots']
        tourney_slots = df[df.season == self.id]  # slice of tourney_slots DataFrame for current season

        df = Constants.KAGGLE_DATA['tourney_seeds']
        tourney_seeds = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season

        # predict winners of play-in games

        # populate 1st round of bracket
        pdb.set_trace()
        for _id, row in tourney_slots.iterrows():
            self.tournament_bracket['R1'][row.seed]

    def generate_kaggle_submission(self):
        """
        Generate .csv file formatted for submission to Kaggle March Madness competition.

        This file contains win probabilities for every possible team match-up. Output is formatted into 2 rows:
        - row 1: identifies season and two teams playing
        - row 2: probability that team1 beats team2
        """
        if self.tournament_year < "2003":
            print("Cannot generate Kaggle submission for year '%s', do not have KenPom data." % self.tournament_year)
            return

        # if necessary make kaggle_submission_dir directory
        kaggle_submission_dir = Constants.OUTPUT_DATA
        if not os.path.isdir(kaggle_submission_dir):
            os.mkdir(kaggle_submission_dir)

        # open csv writer
        file_path = os.path.join(kaggle_submission_dir, "kaggle_season%s.csv" % self.id)
        if os.path.isfile(file_path):
            os.remove(file_path)
        handle = open(file_path, "w")
        csv_writer = csv.writer(handle)
        csv_writer.writerow(["id", "pred"])

        # variable init
        team_ids = self.teams.keys()
        team_ids.sort()

        # loop through all possible match ups in tournament and write probability of team1 win to .csv
        for i in range(len(team_ids)):
            for k in range(i+1, len(team_ids)):
                team_1 = self.teams[team_ids[i]]
                team_2 = self.teams[team_ids[k]]
                row = ["%s_%s_%s" % (self.id, team_1.id, team_2.id)]

                team_1_efficiency = team_1.calculate_efficiency(season_max_offensive_efficiency=self.max_offense_efficiency,
                                                                season_max_defensive_efficiency=self.max_defense_efficiency,
                                                                season_min_offensive_efficiency=self.min_offense_efficiency,
                                                                season_min_defensive_efficiency=self.min_defense_efficiency)
                team_2_efficiency = team_2.calculate_efficiency(season_max_offensive_efficiency=self.max_offense_efficiency,
                                                                season_max_defensive_efficiency=self.max_defense_efficiency,
                                                                season_min_offensive_efficiency=self.min_offense_efficiency,
                                                                season_min_defensive_efficiency=self.min_defense_efficiency)

                team_1_win_probability = (((team_1_efficiency - team_2_efficiency) + 1) / 2)  # scale to be in range of 0.0 - 1.0
                
                row.append(team_1_win_probability)
                csv_writer.writerow(row)
        handle.close()

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
        self.offense_efficiency = None
        self.defense_efficiency = None

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

    def set_tourney_seed(self, tourney_seed, regions):
        self.tourney_seed = tourney_seed
        self.division = regions[tourney_seed[0]]
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
                self.offense_efficiency = self.kenpom_data_frame.AdjOE.iloc[0]
                self.defense_efficiency = self.kenpom_data_frame.AdjDE.iloc[0]
            else:
                raise Exception("KenPom data not found for team name:%s, id:%s" % (self.name, self.id))

    def calculate_efficiency(self, season_max_offensive_efficiency, season_max_defensive_efficiency,
                             season_min_offensive_efficiency, season_min_defensive_efficiency,):
        adj_off_eff = (self.offense_efficiency - season_min_offensive_efficiency) / \
                      (season_max_offensive_efficiency - season_min_offensive_efficiency)
        adj_def_eff = (self.defense_efficiency - season_min_defensive_efficiency) / \
                      (season_max_defensive_efficiency - season_min_defensive_efficiency)
        adj_total_eff = (adj_off_eff + adj_def_eff) / 2

        return adj_total_eff

if __name__ == "__main__":
    for _, row in Constants.KAGGLE_DATA['seasons'].iterrows():
        # create Season object
        season = Season(id=row['season'], years=row['years'], day_zero =row['dayzero'])
        season.set_regions(region_w=row['regionW'], region_x=row['regionX'], region_y=row['regionY'], region_z=row['regionZ'])

        # build teams and analyze data
        season.build_teams()
        season.generate_kaggle_submission()
        #season.build_bracket()
        pprint.pprint(season.tournament_bracket)