#!/usr/bin/env python
""":module: Win probability calculated as difference from division seed values."""
import pdb

import Analysis
import Constants
import Misc


class HighSeed(Analysis.BaseClass):
    def __init__(self):
        self.name = "High Seed"

    def data_available(self, season_id):
        Misc.check_input_data("Kaggle", "tourney_seeds", raise_exception=True)

        return True

    def train_season(self, team, season_id):
        pass

    def win_probability(self, team_1, team_2, season_id, daynum=None):
        max_seed = 16

        team_1_season = team_1.get_season(season_id)
        team_2_season = team_2.get_season(season_id)

        result = float((max_seed - team_1_season.division_seed) - (max_seed - team_2_season.division_seed)) / max_seed + 0.5

        return result