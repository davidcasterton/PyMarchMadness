#!/usr/bin/env python
"""Parent Analysis class, all classes in Analysis/ directory inherit from here."""

import os
import pandas
import pdb
import re

import Constants

__author__ = "David Casterton"
__license__ = "GPL"


class AnalysisBase(object):
    """Analysis parent class, must be inherited into children classes which implement analysis details."""
    def __init__(self):
        self.name = None

        #prevent base class from being called directly
        if type(self) == AnalysisBase:
            raise Exception("Analysis must be subclassed.")

    def data_available(self, season):
        """
        Check if KenPom data is available for this Season's year.

        Args:
            season (object): Season object

        Returns:
            result (bool): True if KenPom data is available
        """
        raise NotImplementedError

    def get_name(self, remove_spaces=False):
        """
        Kwargs:
            remove_spaces (bool, optional): if True then removes spaces from name

        Returns:
            name (string): name of Analysis method
        """
        if remove_spaces:
            name = re.sub(" ", "", self.name)
        else:
            name = self.name

        return name

    def win_probability(self, team_1, team_2):
        """
        Calculate win probability between 2 teams.

        Args:
            team_1 (object): Team object
            team_2 (object): Team object

        Returns:
            team_1_win_probability (float): value between 0.0-1.0 that team 1 will beat team 2. Value > 0.5 indicates that team 1 will win.
        """
        raise NotImplementedError

    def predict_winner(self, team_1, team_2):
        """
        Predict the winner between 2 teams.

        Args:
            team_1 (object): Team object
            team_2 (object): Team object

        Returns:
            winner (object): object of Team predicted to win
        """
        team_1_win_probability = self.win_probability(team_1, team_2)
        if team_1_win_probability >= 0.5:
            winner = team_1
        else:
            winner = team_2

        return winner

    def write_matchup_probabilities_file(self, seasons):
        """
        Write win probabilities to a .csv file for every possible team combination.

        Args:
            seasons (dict): key=tournament year, value=Season object
        """
        # if necessary make output directory
        if not os.path.isdir(Constants.OUTPUT_FOLDER):
            os.mkdir(Constants.OUTPUT_FOLDER)

        #variable init
        file_path = os.path.join(Constants.OUTPUT_FOLDER, "%s-matchup_probabilities.csv" % self.get_name(remove_spaces=True))
        all_season_matchup_probabilities = pandas.DataFrame()
        years = seasons.keys()
        years.sort()

        for year in years:
            #only write probabilities for last 5 years
            if year < (Constants.CURRENT_YEAR-5):
                continue

            season = seasons[year]
            all_season_matchup_probabilities = all_season_matchup_probabilities.append(season.matchup_probabilities)

        # Write probabilities file. Output is formatted into 2 rows:
        #   row 1: identifies season and two teams playing
        #   row 2: probability that team1 beats team2
        all_season_matchup_probabilities.to_csv(file_path, mode="w", index=False)

        print("Wrote match up probabilities to: '%s'" % file_path)


    def write_bracket_file(self, seasons):
        """
        Write tournament bracket to .txt file.

        Args:
            seasons (dict): key=tournament year, value=Season object
        """
        # if necessary make output directory
        if not os.path.isdir(Constants.OUTPUT_FOLDER):
            os.mkdir(Constants.OUTPUT_FOLDER)

        #variable init
        file_path = os.path.join(Constants.OUTPUT_FOLDER, "%s-tournament_brackets.txt" % self.get_name(remove_spaces=True))
        years = seasons.keys()
        years.sort()
        handle = open(file_path, "w")

        for year in years:
            season = seasons[year]

            if season.tournament.bracket == Constants.TOURNAMENT_BRACKET:
                continue

            # write bracket to  file
            handle.write(season.get_bracket() + "\n")

        handle.close()

        print("Wrote predicted tournament bracket to: '%s'" % file_path)