#!/usr/bin/env python
""":module: NCAA basketball module."""

import copy
import pandas
import pdb
import re

import Constants


class Team(object):
    """:class: 1 NCAA backetball team for 1 NCAA season."""
    def __init__(self, id, name, years):
        """
        :param string id:  team identifier, defined in Kaggle/teams.csv id column
        :param string name:  team name, defined in Kaggle/teams.csv name column
        :param string years:  2 years that NCAA season spans in format 'XXXX-YYYY'
        """
        self.id = id
        self.name = name
        self.years = years
        self.tournament_year = int(self.years.split("-")[1])

        self.kenpom_data_frame = pandas.DataFrame
        self.tourney_seed = None
        self.division = None
        self.division_seed = None
        self.pythag = None
        self.offense_efficiency = None
        self.defense_efficiency = None

    def __str__(self):
        attribute_list = list()
        attribute_list.append(self.name.ljust(20))
        attribute_list.append(("season: %s" % self.years).ljust(10))
        attribute_list.append(("id: %s" % self.id).ljust(10))
        if self.division:
            attribute_list.append(("division: %s" % self.division).ljust(20))
        if self.division_seed:
            attribute_list.append(("seed: %s" % self.division_seed).ljust(10))
        if self.pythag:
            attribute_list.append("Pythag: %s" % self.pythag)
        if self.offense_efficiency:
            attribute_list.append("Offensive efficiency: %s" % self.offense_efficiency)
        if self.defense_efficiency:
            attribute_list.append("Defensive efficiency: %s" % self.defense_efficiency)
        return "| ".join(attribute_list)

    def set_tourney_seed(self, tourney_seed, regions):
        """
        :method: Set this teams seed in the tournament.

        :param string tourney_seed: string encoding this teams division and seed
        :param dict regions: dictionary to map between division id's and division names
        """
        self.tourney_seed = str(tourney_seed)
        self.division = regions[self.tourney_seed[0]]
        self.division_seed = int(self.tourney_seed[1:2])

    def load_kenpom_data(self):
        """:method: Search KenPom dataframes and populate member variables."""
        input_file_name = 'summary%s' % str(self.tournament_year)[-2:]
        if input_file_name in Constants.INPUT_DATA['KenPomWithIds'].keys():
            df = Constants.INPUT_DATA['KenPomWithIds'][input_file_name]
            self.kenpom_data_frame = df[df.TeamId == self.id]  # single row from summaryXX.csv for this team
            if not self.kenpom_data_frame.empty:
                self.pythag = self.kenpom_data_frame.Pythag.iloc[0]
                self.offense_efficiency = self.kenpom_data_frame.AdjOE.iloc[0]
                self.defense_efficiency = self.kenpom_data_frame.AdjDE.iloc[0]
            else:
                raise Exception("KenPom data not found for team name:'%s', id:'%s'" % (self.name, self.id))


class Season(object):
    """:class: 1 NCAA backetball season."""
    def __init__(self, id, years, day_zero):
        """
        :param string id: season identifier, defined in Kaggle/seasons.csv season column
        :param string years:  2 years that NCAA season spans in format 'XXXX-YYYY'
        :param string day_zero: Season start day
        """
        self.id = id
        self.years = years
        self.day_zero = day_zero

        self.matchup_probabilities = pandas.DataFrame(columns=["id", "pred"])
        self.tournament = Tournament(season=self)
        self.regions = {}  # dictionary of region names, indexed by region id
        self.teams = {}  # dictionary of Team objects, indexed by team_id

    def __str__(self):
        string = self.years
        return string

    def set_regions(self, region_w, region_x, region_y, region_z):
        """:method: Set mapping between region id's and names, e.g. "W":"East", "X":"MidWest", ..."""
        self.regions = {
            "W": region_w,
            "X": region_x,
            "Y": region_y,
            "Z": region_z,
        }

    def build_teams(self):
        """:method: Build Team objects for this season from INPUT_DATA['Kaggle']."""
        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        tourney_teams = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_teams.iterrows():
            # define variables relevant to Team
            team_id = int(row.team)
            df = Constants.INPUT_DATA['Kaggle']['teams']
            team_name = df[df.id == team_id].name.iloc[0]
            tourney_seed = row.seed

            # create Team object
            team_object = Team(id=team_id, name=team_name, years=self.years)
            team_object.set_tourney_seed(tourney_seed=tourney_seed, regions=self.regions)
            team_object.load_kenpom_data()

            self.add_team(team_object)

    def add_team(self, team_object):
        """
        :method: Add Team object to self.teams dictionary, check for updates to min/max efficiency variables.

        :param object team_object: Team object
        """
        self.teams[team_object.id] = team_object

    def generate_matchup_probabilities(self, analysis):
        """
        :method: Generate matchup probabilities formatted for submission to Kaggle March Madness competition.

        :param object analysis: Analysis object
        """
        if not analysis.data_available(season=self):
            return

        # variable init
        team_ids = self.teams.keys()
        team_ids.sort()
        probabilities = []

        # loop through all possible match ups in tournament and write probability of team1 win to .csv
        for i in range(len(team_ids)):
            for k in range(i+1, len(team_ids)):
                team_1 = self.teams[team_ids[i]]
                team_2 = self.teams[team_ids[k]]

                id = "%s_%s_%s" % (self.id, team_1.id, team_2.id)
                pred = analysis.win_probability(team_1, team_2)

                probabilities.append({"id": id, "pred": pred})

        self.matchup_probabilities = self.matchup_probabilities.append(probabilities, ignore_index=True)

    def generate_bracket(self, analysis):
        """
        :method: Populate bracket 1st round then predict outcome of all rounds.

        :param object analysis: Analysis object
        """
        if not analysis.data_available(season=self):
            return

        # simulate all rounds of bracket
        self.tournament.populate_1st_round(analysis)
        for round_num in range(1, 7):
            self.tournament.predict_round(round_num, analysis)

    def get_bracket(self):
        """
        :returns: current bracket
        :rtype: string
        """
        return str(self.tournament)


class Tournament(object):
    """:class: 1 NCAA March Madness tournament."""
    def __init__(self, season):
        """
        :param object season: Season object
        """
        self.season = season

        self.year = int(self.season.years.split("-")[1])
        self.bracket = copy.deepcopy(Constants.TOURNAMENT_BRACKET)

    def __str__(self):
        bracket_string = self.season.years
        for round_int in range(7):
            round_id = "R%02d" % round_int
            bracket_string += "\nRound %d:  " % (round_int + 1)
            round_list = []
            for bracket_index, team in self.bracket[round_id].iteritems():
                round_list.append("%s: %s" % (bracket_index, team.name if team else ""))
            round_list.sort()
            bracket_string += ",  ".join(round_list)

        return bracket_string

    def get_team_by_seed(self, seed):
        """
        :method: Get team object from tournament seed string.

        :param string seed: tournament seed string
        :returns: Team object
        :rtype: object
        """
        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        tourney_seeds = df[df.season == self.season.id]  # slice of tourney_seeds DataFrame for current season

        team_df = tourney_seeds[(tourney_seeds.season == self.season.id) & (tourney_seeds.seed == seed)]
        if not team_df.empty:
            team_id = team_df.team.iloc[0]
            team = self.season.teams[team_id]
        else:
            team = None

        return team

    @staticmethod
    def zero_pad_seed(original_seed):
        """
        :method: Ensure that seed string has a 2 digit numeric element, e.g. W1 -> W01.

        :param string original_seed:  original seed value
        :returns: seed value with 2 digit numeric element
        :rtype string
        """
        match = re.search("([WXYZ])([\d\w]+)", original_seed)
        if match and len(match.group(2)) == 1:
            seed = match.group(1) + "0" + match.group(2)
        else:
            seed = original_seed

        return seed

    def populate_1st_round(self, analysis):
        """
        :method: Populate 1st round of bracket with teams.

        :param object analysis: Analysis object
        """
        if not analysis.data_available(self.season):
            return

        #variable init
        round_1 = "R00"

        # predict winners for play-in games
        df = Constants.INPUT_DATA['Kaggle']['tourney_slots']
        tourney_slots = df[df.season == self.season.id]  # slice of tourney_slots DataFrame for current season
        for _id, row in tourney_slots.iterrows():
            if row.slot[0] != "R":
                # play-in game
                team_1 = self.get_team_by_seed(row.strongseed)
                team_2 = self.get_team_by_seed(row.weakseed)
                winner = analysis.predict_winner(team_1, team_2)

                slot = self.zero_pad_seed(row.slot)
                self.bracket[round_1][slot] = winner

        # populate non-play-in teams
        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        tourney_seeds = df[df.season == self.season.id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_seeds.iterrows():
            if len(row.seed) == 3:
                self.bracket[round_1][row.seed] = self.get_team_by_seed(row.seed)

    def predict_round(self, tourney_round, analysis):
        """
        :method: Predict winner of a single round of the tournament.

        :param int tourney_round: round of the tournament to predict.
        :param object analysis: Analysis object
        """
        if not analysis.data_available(self.season):
            return

        last_round_id_2digit = "R%02d" % (tourney_round - 1)
        current_round_id_1digit = "R%d" % tourney_round
        current_round_id_2digit = "R%02d" % tourney_round

        df = Constants.INPUT_DATA['Kaggle']['tourney_slots']
        tourney_slots = df[df.season == self.season.id]  # slice of tourney_slots DataFrame for current season
        for _id, row in tourney_slots.iterrows():
            if row.slot[:2] == current_round_id_1digit:
                if tourney_round == 6:
                    strongseed = row.strongseed[-2:]
                    weakseed = row.weakseed[-2:]
                else:
                    strongseed = self.zero_pad_seed(row.strongseed)
                    weakseed = self.zero_pad_seed(row.weakseed)
                team_1 = self.bracket[last_round_id_2digit][strongseed]
                team_2 = self.bracket[last_round_id_2digit][weakseed]
                if not team_1 or not team_2:
                    raise Exception("Cannot predict round '%s', do not have results from prior round." % tourney_round)
                winner = analysis.predict_winner(team_1, team_2)

                if tourney_round == 5:
                    slot = row.slot[-2:]
                else:
                    slot = self.zero_pad_seed(row.slot[-2:])
                self.bracket[current_round_id_2digit][slot] = winner
