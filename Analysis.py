import pandas
import pdb

import Constants


class Analysis(object):
    def data_available(self, season):
        raise NotImplementedError

    def calculate_win_probability(self, team_1, team_2):
        raise NotImplementedError

    def predict_winner(self, team_1, team_2):
        raise NotImplementedError


class KenPom(Analysis):
    def data_available(self, season):
        """
        Check if KenPom data is available for this Season's year.

        @param  season  object      Season object
        @return result  bool        True if KenPom data is available
        """
        if season.tournament_year >= Constants.KENPOM_START_YEAR and season.tournament_year != Constants.CURRENT_YEAR:
            result = True
        else:
            result = False
        return result

    def calculate_win_probability(self, team_1, team_2):
        """
        Calculate win probability between 2 teams.

        @param  team_1  Team object
        @param  team_2  Team object
        @return team_1_win_probability  float   value between 0.0-1.0 that team 1 will beat team 2. Value > 0.5
                                                indicates that team 1 will win.
        """
        team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)  # scale to be in range of 0.0 - 1.0
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability

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