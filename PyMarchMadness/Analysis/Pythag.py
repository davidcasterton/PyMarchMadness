#!/usr/bin/env python
""":module: Win probability calculated as difference from Ken Pomeroy Pythag values."""

import Analysis
import Constants
import Misc


class Pythag(Analysis.BaseClass):
    def __init__(self):
        self.name = "Ken Pomeroy Pythag"

    def data_available(self, season_id):
        tournament_year = Constants.SEASON_ID_TO_YEAR.get(season_id)
        file_name = 'summary%s' % str(tournament_year)[-2:]
        Misc.check_input_data("KenPomWithIds", file_name, raise_exception=True)

        Misc.check_input_data("Kaggle", "tourney_seeds", raise_exception=True)

        return True

    def train(self, team, season_id):
        pass

    def get_pythag(self, season_id, team):
        """:method: Load pythag value to team.year from KenPom dataframes."""
        tournament_year = Constants.SEASON_ID_TO_YEAR.get(season_id)
        file_name = 'summary%s' % str(tournament_year)[-2:]
        Misc.check_input_data('KenPomWithIds', file_name, raise_exception=True)

        df = Constants.INPUT_DATA['KenPomWithIds'][file_name]
        df_team = df[df.TeamId == team.id]  # single row from summaryXX.csv for this team

        year_object = team.get_year(tournament_year)
        year_object.pythag = df_team.Pythag.iloc[0]

    def win_probability(self, team_1, team_2, season_id, daynum=None):
        team_1_season = team_1.get_season(season_id)
        team_2_season = team_2.get_season(season_id)

        # load pythag if needed
        if not hasattr(team_1_season, 'pythag'):
            self.get_pythag(season_id, team_1)
        if not hasattr(team_2_season, 'pythag'):
            self.get_pythag(season_id, team_2)

        team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability