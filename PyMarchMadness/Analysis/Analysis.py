#!/usr/bin/env python
""":module: Analysis base module."""

import os
import pandas
import pdb
import re

import Constants


class BaseClass(object):
    """:class: Analysis base class, all classes in Analysis/ directory inherit from here."""
    def __init__(self):
        self.name = None

        #prevent base class from being called directly
        if type(self) == BaseClass:
            raise Exception("Analysis must be subclassed.")

    def data_available(self, season_id):
        """
        :method: Check if required data is available for this season.

        :param str season: Kaggle season id
        :returns: True if KenPom data is available
        :rtype: bool
        """
        raise NotImplementedError

    def get_name(self, remove_spaces=False):
        """
        :method: Returns class name.

        :param bool remove_spaces: if True then removes spaces from name
        :returns: name of current Analysis class
        :rtype: string
        """
        if remove_spaces:
            name = re.sub(" ", "", self.name)
        else:
            name = self.name

        return name

    def train(self, team, season_id):
        """
        :method: Train on regular season data

        :param object team: Team object
        :param object season: Kaggle season id
        """
        raise NotImplementedError

    def win_probability(self, team_1, team_2, season_id, daynum=None):
        """
        :method: Calculate win probability between 2 teams.

        :param object team_1: Team object
        :param object team_2: Team object
        :param int season_id: Kaggle season id
        :param int daynum: day number within season, 1st game is day 0
        :returns: probability that team 1 will beat team 2. Value > 0.5 indicates that team 1 will win.
        :rtype: float
        """
        raise NotImplementedError

    def predict_winner(self, team_1, team_2, season_id, daynum=None):
        """
        :method: Predict the winner between 2 teams.

        :param object team_1: Team object
        :param object team_2: Team object
        :param int season_id: Kaggle season id
        :param int daynum: day number within season, 1st game is day 0
        :returns: Team predicted to win
        :rtype: object
        """
        team_1_win_probability = self.win_probability(team_1, team_2, season_id, daynum)
        if team_1_win_probability >= 0.5:
            winner = team_1
        else:
            winner = team_2

        return winner