#!/usr/bin/env python
""":module: Classes representing Basketball concepts."""

import copy
import os
import pandas
import pdb
import re
import sys

import Constants
import Misc


class TeamFactory(object):
    """:class: Factory generating, storing, retrieving Team objects."""
    def __init__(self):
        self.teams = {}  # dictionary of Team objects, indexed by team_id

    def get_team(self, team_id):
        return self.teams.get(team_id)

    def add_team(self, team_id, team_name):
        if not self.get_team(team_id):
            team = Team(team_id, team_name)
            self.teams[team_id] = team

        return self.get_team(team_id)

    def add_all_teams(self):
        """:method: Build objects for all teams from Kaggle data & add them to factory."""
        Misc.check_input_data("Kaggle", "tourney_seeds")
        Misc.check_input_data("Kaggle", "teams")

        df_seeds = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        for _id, row in df_seeds.iterrows():
            # variable init
            season_id = row.season
            team_id = int(row.team)
            df_teams = Constants.INPUT_DATA['Kaggle']['teams']
            team_name = df_teams[df_teams.id == team_id].name.iloc[0]
            tourney_seed = row.seed

            # create Team object
            team = self.get_team(team_id)
            if not team:
                team = Team(id=team_id, name=team_name)
            season = team.add_season(season_id)
            season.set_tourney_seed(tourney_seed)

            self.add_team(team_id, team_name)


class Team(object):
    """:class: 1 NCAA backetball team."""
    def __init__(self, id, name):
        """
        :param int id:  team identifier, defined in Kaggle/teams.csv id column
        :param string name:  team name, defined in Kaggle/teams.csv name column
        """
        self.id = id
        self.name = name

        self.seasons = {}  # dictionary of Season objects, indexed by season_id (int)

    def __str__(self, indentation_level=0):
        indentation = Constants.INDENTATION * indentation_level

        _string = "%s%s\n" % (indentation, self.name)
        _string += "%sid: %s\n" % (indentation, self.id)

        # add seasons
        seasons = self.seasons.keys()
        seasons.sort()
        for season in seasons:
            season_object = self.seasons.get(season)
            _string += season_object.__str__(indentation_level=indentation_level+1)

        return _string

    def get_season(self, season_id):
        """
        :method: Get Season object from season_id

        :param season_id: Kaggle season_id
        """
        return self.seasons.get(season_id)

    def add_season(self, season_id):
        """
        :method: Add Season object for season_id

        :param string season_id:  year of NCAA tournament
        """
        if not self.get_season(season_id):
            season = Season(season_id)
            self.seasons[season_id] = season

        return self.get_season(season_id)


class Season(object):
    """:method: 1 Season worth of data for 1 team. This class is mostly a data container populated by Analysis classes."""
    def __init__(self, id):
        """
        :param int season_id: Kaggle season id
        """
        self.id = id
        self.tournament_year = Constants.SEASON_ID_TO_YEAR.get(id)

        self.tourney_seed = None
        self.division = None
        self.division_seed = None

    def __str__(self, indentation_level=0):
        """
        :method: Return string of all variables in local namespace

        :param int indentation_level: top level indentation level for each line in response
        :results: string of all variables in locals()
        """
        def _variable_name(obj, namespace):
            return [name for name in namespace if namespace[name] is obj]

        indentation = Constants.INDENTATION * indentation_level

        _string = "%sSeason: %s (%s)\n" % (indentation, self.tournament_year, self.id)

        indentation = Constants.INDENTATION * (indentation_level+1)
        for variable_name, value in locals():
            #variable_name = _variable_name(variable, locals())
            _string += "%s%s: %s\n" % (indentation, variable_name, value)

        return _string

    def set_tourney_seed(self, tourney_seed):
        """
        :method: Set this teams seed in the tournament.

        :param string tourney_seed: string encoding this teams division and seed
        :param dict regions: dictionary to map between division id's and division names
        """
        self.tourney_seed = str(tourney_seed)
        division_id = self.tourney_seed[0]
        self.division = Constants.DIVISIONS[self.id][division_id]
        self.division_seed = int(self.tourney_seed[1:2])


class Tournament(object):
    """:class: 1 NCAA March Madness tournament."""
    def __init__(self, team_factory, season_id):
        """
        :param object team_factory: TeamFactory object
        :param str season_id: Kaggle season id
        """
        self.team_factory = team_factory
        self.season_id = season_id

        self.matchup_probabilities = pandas.DataFrame(columns=["id", "pred"])
        self.bracket = copy.deepcopy(Constants.TOURNAMENT_BRACKET)

    def __str__(self):
        year = Constants.SEASON_ID_TO_YEAR[self.season_id]
        return "%s Tournament" % (year)

    def get_team_by_seed(self, seed):
        """
        :method: Get team object from tournament seed string.

        :param string seed: tournament seed string
        :returns: Team object
        :rtype: object
        """
        Misc.check_input_data("Kaggle", "tourney_seeds")

        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        team_df = df[(df.season == self.season_id) & (df.seed == seed)]
        if not team_df.empty:
            team_id = team_df.team.iloc[0]
            team = self.team_factory.get_team(team_id)
        else:
            team = None

        return team

    @staticmethod
    def zero_pad_seed(original_seed):
        """
        :method: Ensure that seed string has a 2 digit numeric element, e.g. W1 -> W01.

        :param string original_seed:  original seed value
        :returns: seed value with 2 digit numeric element
        :rtype: string
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
        Misc.check_input_data("Kaggle", "tourney_slots")
        Misc.check_input_data("Kaggle", "tourney_seeds")

        #variable init
        round_1 = "R00"

        # predict winners for play-in games
        df = Constants.INPUT_DATA['Kaggle']['tourney_slots']
        tourney_slots = df[df.season == self.season_id]  # slice of tourney_slots DataFrame for current season
        for _id, row in tourney_slots.iterrows():
            if row.slot[0] != "R":
                # play-in game
                team_1 = self.get_team_by_seed(row.strongseed)
                team_2 = self.get_team_by_seed(row.weakseed)
                winner = analysis.predict_winner(team_1, team_2, self.season_id)

                slot = self.zero_pad_seed(row.slot)
                self.bracket[round_1][slot] = winner

        # populate non-play-in teams
        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        tourney_seeds = df[df.season == self.season_id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_seeds.iterrows():
            if len(row.seed) == 3:
                self.bracket[round_1][row.seed] = self.get_team_by_seed(row.seed)

    def predict_round(self, tourney_round, analysis):
        """
        :method: Predict winner of a single round of the tournament.

        :param int tourney_round: round of the tournament to predict.
        :param object analysis: Analysis object
        """
        Misc.check_input_data("Kaggle", "tourney_slots")

        last_round_id_2digit = "R%02d" % (tourney_round - 1)
        current_round_id_1digit = "R%d" % tourney_round
        current_round_id_2digit = "R%02d" % tourney_round

        df = Constants.INPUT_DATA['Kaggle']['tourney_slots']
        tourney_slots = df[df.season == self.season_id]  # slice of tourney_slots DataFrame for current season
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
                winner = analysis.predict_winner(team_1, team_2, self.season_id)

                if tourney_round == 5:
                    slot = row.slot[-2:]
                else:
                    slot = self.zero_pad_seed(row.slot[-2:])
                self.bracket[current_round_id_2digit][slot] = winner

    def generate_matchup_probabilities(self, analysis):
        """
        :method: Generate matchup probabilities formatted for submission to Kaggle March Madness competition.

        :param object analysis: Analysis object
        """
        # variable init
        probabilities = []
        team_ids = []
        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        tourney_seeds = df[df.season == self.season_id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_seeds.iterrows():
            team_ids.append(row.team)
        team_ids.sort()

        # loop through all possible match ups in tournament and write probability of team1 win to .csv
        for i in range(len(team_ids)):
            for k in range(i+1, len(team_ids)):
                team_1 = self.team_factory.get_team(team_ids[i])
                team_2 = self.team_factory.get_team(team_ids[k])

                id = "%s_%s_%s" % (self.season_id, team_1.id, team_2.id)
                pred = analysis.win_probability(team_1, team_2, self.season_id)

                probabilities.append({"id": id, "pred": pred})

        if probabilities:
            self.matchup_probabilities = self.matchup_probabilities.append(probabilities, ignore_index=True)

    def generate_bracket(self, analysis):
        """
        :method: Populate bracket 1st round then predict outcome of all rounds.

        :param object analysis: Analysis object
        """
        # simulate all rounds of bracket
        self.populate_1st_round(analysis)
        for tourney_round in range(1, 7):
            self.predict_round(tourney_round, analysis)

    def get_matchup_probabilities(self):
        """
        :method: Write win probabilities to a .csv file for every possible team combination.

        :returns: matchup probabilities
        :rtype: DataFrame
        """
        return self.matchup_probabilities

    def get_bracket(self):
        """
        :method: Write tournament bracket to .txt file.

        :returns: tournament bracket
        :rtype: string
        """
        year = Constants.SEASON_ID_TO_YEAR[self.season_id]
        bracket_string = str(year)
        for round_int in range(7):
            round_id = "R%02d" % round_int
            bracket_string += "\nRound %d:  " % (round_int + 1)
            round_list = []
            for bracket_index, team in self.bracket[round_id].iteritems():
                round_list.append("%s: %s" % (bracket_index, team.name if team else ""))
            round_list.sort()
            bracket_string += ",  ".join(round_list)
        bracket_string += "\n"

        return bracket_string
