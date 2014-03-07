#!/usr/bin/env python
"""Win probability calculated as difference from Ken Pomeroy Pythag values."""

import Analysis
import Constants

__author__ = "David Casterton"
__license__ = "GPL"


class Pythag(Analysis.BaseClass):
    def __init__(self):
        self.name = "Ken Pomeroy Pythag"

    def data_available(self, season):
        file_name = 'summary%s' % str(season.tournament.year)[-2:]
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

    def win_probability(self, team_1, team_2):
        team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability