#!/usr/bin/env python
""":module: Win probability randomly generated."""

import random

import Analysis
import Constants


class Random(Analysis.BaseClass):
    def __init__(self):
        self.name = "Random"

    def data_available(self, season):
        if not Constants.INPUT_DATA.get('Kaggle'):
            return False

        if not Constants.INPUT_DATA['Kaggle'].get('tourney_seeds'):
            return False

        df = Constants.INPUT_DATA['Kaggle']['tourney_seeds']
        tourney_seeds = df[df.season == season.id]
        if tourney_seeds.empty:
            return False

        return True

    def train(self):
        pass

    def win_probability(self, team_1, team_2):
        team_1_win_probability = random.random()
        team_1_win_probability = round(team_1_win_probability, 6)

        return team_1_win_probability