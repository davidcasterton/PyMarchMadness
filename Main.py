import copy
import csv
import inspect
import os
import pandas
import pdb
import re

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
        self.tournament_bracket = copy.deepcopy(Constants.TOURNAMENT_BRACKET)
        self.max_offense_efficiency = 0
        self.max_defense_efficiency = 0
        self.min_offense_efficiency = 200
        self.min_defense_efficiency = 200

    def __str__(self):
        # define how Season object will look if printed
        string = self.years
        return string

    def set_regions(self, region_w, region_x, region_y, region_z):
        self.regions = {
            "W": region_w,
            "X": region_x,
            "Y": region_y,
            "Z": region_z,
        }

    def get_bracket(self):
        """
        Return formatted string of predicted tournament bracket.

         @return bracket_string     string  formatted tournament bracket
        """
        if not self.check_kenpom_available():
            print("%s:%s: No KenPom data for year '%s'." % (self.__class__.__name__, inspect.stack()[0][3], self.tournament_year))
            return

        bracket_string = self.years
        for round_int in range(7):
            round_id = "R%02d" % round_int
            bracket_string += "\nRound %d:  " % round_int
            round_list = []
            for bracket_index, team in self.tournament_bracket[round_id].iteritems():
                round_list.append("%s: %s" % (bracket_index, team.name if team else "?"))
            round_list.sort()
            bracket_string += ",  ".join(round_list)

        return bracket_string

    def check_kenpom_available(self):
        if self.tournament_year < "2003" or self.tournament_year > "2013":
            result = False
        else:
            result = True
        return result

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
        """
        Add Team object to self.teams dictionary, check for updates to min/max efficiency variables.

        @param team_object  Team object
        """
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

    def zero_pad_seed(self, original_seed):
        """
        Ensure that seed string has a 2 digit numeric element.
        e.g. W1 -> W01

        @param  original_seed   string  original seed value
        @return seed            string  seed value with 2 digit numeric element
        """
        match = re.search("([WXYZ])([\d\w]+)", original_seed)
        if match and len(match.group(2)) == 1:
            seed = match.group(1) + "0" + match.group(2)
        else:
            seed = original_seed

        return seed

    def populate_bracket_1st_round(self):
        """
        Populate 1st round of bracket with teams from Kaggle/tourney_slots.csv.
        """
        if not self.check_kenpom_available():
            print("%s:%s: No KenPom data for year '%s'." % (self.__class__.__name__, inspect.stack()[0][3], self.tournament_year))
            return

        round_1 = "R00"

        # predict winners for play-in games
        df = Constants.KAGGLE_DATA['tourney_slots']
        tourney_slots = df[df.season == self.id]  # slice of tourney_slots DataFrame for current season
        for _id, row in tourney_slots.iterrows():
            if row.slot[0] != "R":
                # play-in game
                team_1 = self.get_team_by_tourney_seed(row.strongseed)
                team_2 = self.get_team_by_tourney_seed(row.weakseed)
                winner = self.predict_winner(team_1, team_2)

                slot = self.zero_pad_seed(row.slot)
                self.tournament_bracket[round_1][slot] = winner

        # populate non-play-in teams
        df = Constants.KAGGLE_DATA['tourney_seeds']
        tourney_seeds = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_seeds.iterrows():
            if len(row.seed) == 3:
                self.tournament_bracket[round_1][row.seed] = self.get_team_by_tourney_seed(row.seed)

    def predict_bracket_round(self, tourney_round):
        """
        Predict winner of a single round of the tournament.

        @param tourney_round    int     round of the tournament to predict.
        """
        if not self.check_kenpom_available():
            print("%s:%s: No KenPom data for year '%s'." % (self.__class__.__name__, inspect.stack()[0][3], self.tournament_year))
            return

        last_round_id_2digit = "R%02d" % (tourney_round - 1)
        current_round_id_1digit = "R%d" % tourney_round
        current_round_id_2digit = "R%02d" % tourney_round

        df = Constants.KAGGLE_DATA['tourney_slots']
        tourney_slots = df[df.season == self.id]  # slice of tourney_slots DataFrame for current season
        for _id, row in tourney_slots.iterrows():
            if row.slot[:2] == current_round_id_1digit:
                if tourney_round == 6:
                    strongseed = row.strongseed[-2:]
                    weakseed = row.weakseed[-2:]
                else:
                    strongseed = self.zero_pad_seed(row.strongseed)
                    weakseed = self.zero_pad_seed(row.weakseed)
                team_1 = self.tournament_bracket[last_round_id_2digit][strongseed]
                team_2 = self.tournament_bracket[last_round_id_2digit][weakseed]
                if not team_1 or not team_2:
                    raise Exception("Cannot predict round '%s', do not have results from prior round." % tourney_round)
                winner = self.predict_winner(team_1, team_2)

                if tourney_round == 5:
                    slot = row.slot[-2:]
                else:
                    slot = self.zero_pad_seed(row.slot[-2:])
                self.tournament_bracket[current_round_id_2digit][slot] = winner

    def get_team_by_tourney_seed(self, seed):
        """
        Get team object from tournament seed string.

        @param  seed    string          tournament seed string
        @return team    Team object
        """
        df = Constants.KAGGLE_DATA['tourney_seeds']
        tourney_seeds = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season

        team_df = tourney_seeds[(tourney_seeds.season == self.id) & (tourney_seeds.seed == seed)]
        if not team_df.empty:
            team_id = team_df.team.iloc[0]
            team = self.teams[team_id]
        else:
            team = None

        return team

    def generate_kaggle_submission(self):
        """
        Generate .csv file formatted for submission to Kaggle March Madness competition.

        This file contains win probabilities for every possible team match-up. Output is formatted into 2 rows:
        - row 1: identifies season and two teams playing
        - row 2: probability that team1 beats team2
        """
        if not self.check_kenpom_available():
            print("%s:%s: No KenPom data for year '%s'." % (self.__class__.__name__, inspect.stack()[0][3], self.tournament_year))
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

                team_1_win_probability = self.calculate_win_probability(team_1, team_2)
                
                row.append(team_1_win_probability)
                csv_writer.writerow(row)
        handle.close()

    def calculate_win_probability(self, team_1, team_2):
        """
        Calculate win probability between 2 teams.

        @return team_1_win_probability  float   value between 0.0-1.0 that team 1 will beat team 2. Value > 0.5
                                                indicates that team 1 will win.
        """
        team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)  # scale to be in range of 0.0 - 1.0

        return team_1_win_probability

    def generate_bracket(self):
        """
        Populate bracket 1st round then predict outcome of all rounds.
        """
        if not self.check_kenpom_available():
            print("%s:%s: No KenPom data for year '%s'." % (self.__class__.__name__, inspect.stack()[0][3], self.tournament_year))
            return

        self.populate_bracket_1st_round()
        self.predict_bracket_round(1)
        self.predict_bracket_round(2)
        self.predict_bracket_round(3)
        self.predict_bracket_round(4)
        self.predict_bracket_round(5)
        self.predict_bracket_round(6)

    def predict_winner(self, team_1, team_2):
        """
        Predict the winner between 2 teams.

        @param  team_1  Team object
        @param  team_2  Team object
        """
        if team_1.pythag >= team_2.pythag:
            winner = team_1
        else:
            winner = team_2

        return winner

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
        """
        Set this teams seed in the tournament.

        @param  tourney_seed    string  string encoding this teams division and seed
        @param  regions         dict    dictionary to map between division id's and division names
        """
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
        """
        Calculate total adjusted efficiency.
        """
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

        # build teams
        season.build_teams()
        # generate Kaggle submission files
        season.generate_kaggle_submission()
        # generate and print bracket
        season.generate_bracket()
        bracket = season.get_bracket()
        if bracket:
            print(bracket)