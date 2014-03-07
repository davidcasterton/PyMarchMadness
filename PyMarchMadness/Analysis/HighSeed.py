#!/usr/bin/env python
"""Win probability calculated as difference from division seed values."""

import Analysis
import Constants

__author__ = "David Casterton"
__license__ = "GPL"


class HighSeed(Analysis.BaseClass):
    def __init__(self):
        self.name = "High Seed"

    def data_available(self, season):
        df = Constants.KAGGLE_INPUT['tourney_seeds']
        tourney_seeds = df[df.season == season.id]
        if not tourney_seeds.empty:
            result = True
        else:
            result = False

        return result

    def win_probability(self, team_1, team_2):
        max_seed = 16
        return float((max_seed - team_1.division_seed) - (max_seed - team_2.division_seed)) / max_seed + 0.5