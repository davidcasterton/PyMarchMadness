#!/usr/bin/env python
""":module: Win probability calculated as difference from Ken Pomeroy Pythag values."""

import Analysis
import Constants


class Pythag(Analysis.BaseClass):
    def __init__(self):
        self.name = "Ken Pomeroy Pythag"

    def data_available(self, season):
        if not Constants.INPUT_DATA.get('KenPomWithIds'):
            return False

        file_name = 'summary%s' % str(season.tournament.year)[-2:]
        if not Constants.INPUT_DATA['KenPomWithIds'].get(file_name):
            return False

        if not Constants.INPUT_DATA['Kaggle'].get('tourney_seeds'):
            return False

        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        tourney_teams = df[df.season == season.id]  # slice of tourney_seeds DataFrame for current season
        if tourney_teams.empty:
            return False

        return True

    def train(self):
        pass

    def win_probability(self, team_1, team_2):
        team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability