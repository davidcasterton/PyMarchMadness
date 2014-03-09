#!/usr/bin/env python
""":module: Perceptron trained on regular season data to calculate tournament win probabilities."""

import Analysis
import Constants
import Misc


class Perceptron(Analysis.BaseClass):
    def __init__(self):
        self.name = "Perceptron"

    def data_available(self, season_id):
        pass

    def train(self, team, season_id):
        pass

    def win_probability(self, team_1, team_2, season_id, daynum=None):
        team_1_season = team_1.get_season(season_id)
        team_2_season = team_2.get_season(season_id)