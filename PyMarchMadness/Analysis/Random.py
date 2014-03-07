#!/usr/bin/env python
"""Win probability randomly generated."""

import random

import Analysis
import Constants

__author__ = "David Casterton"
__license__ = "GPL"


class Random(Analysis.BaseClass):
    def __init__(self):
        self.name = "Random"

    def data_available(self, season):
        df = Constants.KAGGLE_INPUT['tourney_seeds']
        tourney_seeds = df[df.season == season.id]
        if not tourney_seeds.empty:
            result = True
        else:
            result = False

        return result

    def win_probability(self, team_1, team_2):
        team_1_win_probability = random.random()
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability