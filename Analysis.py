import pandas
import pdb

import Constants


class Analysis(object):
    def data_available(self, season):
        """
        Check if KenPom data is available for this Season's year.

        @param  season  object      Season object
        @return result  bool        True if KenPom data is available
        """
        raise NotImplementedError

    def calculate_win_probability(self, team_1, team_2):
        """
        Calculate win probability between 2 teams.

        @param  team_1  Team object
        @param  team_2  Team object
        @return team_1_win_probability  float   value between 0.0-1.0 that team 1 will beat team 2. Value > 0.5
                                                indicates that team 1 will win.
        """
        raise NotImplementedError

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


class KenPom(Analysis):
    def data_available(self, season):
        file_name = 'summary%s' % str(season.tournament_year)[-2:]
        if file_name in Constants.KENPOM_INPUT.keys():
            kenpom_available = True
        else:
            kenpom_available = False

        df = Constants.KAGGLE_INPUT['tourney_seeds']
        tourney_teams = df[df.season == season.id]  # slice of tourney_seeds DataFrame for current season
        if not tourney_teams.empty:
            seeds_available = True
        else:
            seeds_available = False

        if kenpom_available and seeds_available:
            result = True
        else:
            result = False

        return result

    def calculate_win_probability(self, team_1, team_2):
        team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)  # scale to be in range of 0.0 - 1.0
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability


class HighSeed(Analysis):
    def data_available(self, season):
        df = Constants.KAGGLE_INPUT['tourney_seeds']
        tourney_seeds = df[df.season == season.id]
        if not tourney_seeds.empty:
            result = True
        else:
            result = False

        return result

    def calculate_win_probability(self, team_1, team_2):
        max_seed = 16
        return float((max_seed - team_1.division_seed) - (max_seed - team_2.division_seed)) / max_seed + 0.5