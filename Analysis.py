import os
import pandas
import pdb
import random
import re

import Constants


class Analysis(object):
    """
    Analysis base class, must be subclassed to implement analysis methods.
    """
    def __init__(self):
        self.name = None

        #prevent base class from being called directly
        if type(self) == Analysis:
            raise Exception("Analysis must be subclassed.")

    def data_available(self, season):
        """
        Check if KenPom data is available for this Season's year.

        @param  season  object      Season object
        @return result  bool        True if KenPom data is available
        """
        raise NotImplementedError

    def get_name(self, remove_spaces=False):
        if remove_spaces:
            name = re.sub(" ", "", self.name)
        else:
            name = self.name

        return name

    def win_probability(self, team_1, team_2):
        """
        Calculate win probability between 2 teams.

        @param  team_1  Team object
        @param  team_2  Team object
        @return team_1_win_probability  float   value between 0.0-1.0 that team 1 will beat team 2. Value > 0.5
                                                indicates that team 1 will win.
        """
        raise NotImplementedError

    def predict_winner(self, team_1, team_2):
        """
        Predict the winner between 2 teams.

        @param  team_1  Team object
        @param  team_2  Team object
        @return winner  Team object     object of Team predicted to win
        """
        team_1_win_probability = self.win_probability(team_1, team_2)
        if team_1_win_probability >= 0.5:
            winner = team_1
        else:
            winner = team_2

        return winner

    def write_kaggle_probabilities_file(self, seasons):
        """
        Write win probabilities to a .csv file for every possible team combination.
        Output is formatted into 2 rows:
        - row 1: identifies season and two teams playing
        - row 2: probability that team1 beats team2

        @param seasons  dict        key : tournament year, value : Season object
        """
        # if necessary make output directory
        if not os.path.isdir(Constants.OUTPUT_FOLDER):
            os.mkdir(Constants.OUTPUT_FOLDER)

        #variable init
        file_path = os.path.join(Constants.OUTPUT_FOLDER, "%s-kaggle_submission.csv" % self.get_name(remove_spaces=True))
        all_season_kaggle_probabilities = pandas.DataFrame()
        years = seasons.keys()
        years.sort()

        for year in years:
            #only write probabilities for last 5 years
            if year < (Constants.CURRENT_YEAR-5):
                continue

            season = seasons[year]
            all_season_kaggle_probabilities = all_season_kaggle_probabilities.append(season.kaggle_probabilities)

        #write probabilities file
        all_season_kaggle_probabilities.to_csv(file_path, mode="w", index=False)

        print("Wrote Kaggle probabilities to: '%s'" % file_path)


    def write_bracket_file(self, seasons):
        """
        Write tournament bracket to .txt file.

        @param seasons  dict        key : tournament year, value : Season object
        """
        # if necessary make output directory
        if not os.path.isdir(Constants.OUTPUT_FOLDER):
            os.mkdir(Constants.OUTPUT_FOLDER)

        #variable init
        file_path = os.path.join(Constants.OUTPUT_FOLDER, "%s-bracket.txt" % self.get_name(remove_spaces=True))
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

        print("Wrote Bracket file to: '%s'" % file_path)

class Pythag(Analysis):
    """
    Win probability calculated as difference from Ken Pomeroy Pythag values.
    """
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


class HighSeed(Analysis):
    """
    Win probability calculated as difference from division seed values.
    """
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


class Random(Analysis):
    """
    Win probability randomly generated.
    """
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