#!/usr/bin/env python
""":module: Win probability randomly generated."""

import random

import Analysis
import Constants
import Misc


class Random(Analysis.BaseClass):
    def __init__(self):
        self.name = "Random"

    def data_available(self, season):
        return True

    def train(self, team, season_id):
        pass

    def win_probability(self, team_1, team_2, season_id, daynum=None):
        team_1_win_probability = random.random()
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability