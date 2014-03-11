#!/usr/bin/env python
"""
:module: Multilayer Perceptron using Theano to calculate tournament win probabilities.
Built on example code from http://deeplearning.net/tutorial/mlp.html.
"""
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
        pass
