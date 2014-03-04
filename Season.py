import copy
import pandas
import re

import Constants
from Team import Team


class Season(object):
    """
    Season objects represent 1 NCAA backetball season.

    @param id       string  season identifier, defined in Kaggle/seasons.csv season column
    @param years    string  2 years that NCAA season spans in format 'XXXX-YYYY'
    """
    def __init__(self, id, years, day_zero):
        self.id = id
        self.years = years
        self.tournament_year = int(self.years.split("-")[1])
        self.day_zero = day_zero

        self.kaggle_probabilities = pandas.DataFrame(columns=["id", "pred"])
        self.tournament_bracket = copy.deepcopy(Constants.TOURNAMENT_BRACKET)
        self.regions = {}  # dictionary of region names, indexed by region id
        self.teams = {}  # dictionary of Team objects, indexed by team_id
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
        """
        Check if KenPom data is available for this Season's year.

        @return result  bool    True if KenPom data is available
        """
        if self.tournament_year >= Constants.KENPOM_START_YEAR and self.tournament_year != Constants.CURRENT_YEAR:
            result = True
        else:
            result = False
        return result

    def build_teams(self):
        """
        Build Team objects for this season from KAGGLE_INPUT.
        """
        df = Constants.KAGGLE_INPUT['tourney_seeds']
        tourney_teams = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season
        for _id, row in tourney_teams.iterrows():
            # define variables relevant to Team
            team_id = int(row.team)
            df = Constants.KAGGLE_INPUT['teams']
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
        Ensure that seed string has a 2 digit numeric element, e.g. W1 -> W01.

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
            return

        #variable init
        round_1 = "R00"

        # predict winners for play-in games
        df = Constants.KAGGLE_INPUT['tourney_slots']
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
        df = Constants.KAGGLE_INPUT['tourney_seeds']
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
            return

        last_round_id_2digit = "R%02d" % (tourney_round - 1)
        current_round_id_1digit = "R%d" % tourney_round
        current_round_id_2digit = "R%02d" % tourney_round

        df = Constants.KAGGLE_INPUT['tourney_slots']
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
        df = Constants.KAGGLE_INPUT['tourney_seeds']
        tourney_seeds = df[df.season == self.id]  # slice of tourney_seeds DataFrame for current season

        team_df = tourney_seeds[(tourney_seeds.season == self.id) & (tourney_seeds.seed == seed)]
        if not team_df.empty:
            team_id = team_df.team.iloc[0]
            team = self.teams[team_id]
        else:
            team = None

        return team

    def generate_kaggle_probabilities(self):
        """
        Generate matchup probabilities formatted for submission to Kaggle March Madness competition.
        """
        if not self.check_kenpom_available():
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
                pred = self.calculate_win_probability(team_1, team_2)

                probabilities.append({"id": id, "pred": pred})

        self.kaggle_probabilities = self.kaggle_probabilities.append(probabilities, ignore_index=True)

    def calculate_win_probability(self, team_1, team_2):
        """
        Calculate win probability between 2 teams.

        @return team_1_win_probability  float   value between 0.0-1.0 that team 1 will beat team 2. Value > 0.5
                                                indicates that team 1 will win.
        """
        team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)  # scale to be in range of 0.0 - 1.0
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability

    def generate_bracket(self):
        """
        Populate bracket 1st round then predict outcome of all rounds.
        """
        if not self.check_kenpom_available():
            return

        # simulate all rounds of bracket
        self.populate_bracket_1st_round()
        for round_num in range(1, 7):
            self.predict_bracket_round(round_num)

    def predict_winner(self, team_1, team_2):
        """
        Predict the winner between 2 teams.

        @param  team_1  Team object
        @param  team_2  Team object
        @return winner  Team object     object of Team predicted to win
        """
        team_1_win_probability = self.calculate_win_probability(team_1, team_2)
        if team_1_win_probability >= 0.5:
            winner = team_1
        else:
            winner = team_2

        return winner