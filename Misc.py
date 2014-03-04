import os
import pandas

import Constants


def calculate_win_probability(team_1, team_2):
    """
    Calculate win probability between 2 teams.

    @return team_1_win_probability  float   value between 0.0-1.0 that team 1 will beat team 2. Value > 0.5
                                            indicates that team 1 will win.
    """
    team_1_win_probability = (((team_1.pythag - team_2.pythag) + 1) / 2)  # scale to be in range of 0.0 - 1.0
    team_1_win_probability = round(team_1_win_probability, 6)

    return team_1_win_probability


def predict_winner(team_1, team_2):
    """
    Predict the winner between 2 teams.

    @param  team_1  Team object
    @param  team_2  Team object
    @return winner  Team object     object of Team predicted to win
    """
    team_1_win_probability = calculate_win_probability(team_1, team_2)
    if team_1_win_probability >= 0.5:
        winner = team_1
    else:
        winner = team_2

    return winner


def write_kaggle_probabilities_file(seasons):
    """
    Write win probabilities to a .csv file for every possible team combination.
    Output is formatted into 2 rows:
    - row 1: identifies season and two teams playing
    - row 2: probability that team1 beats team2
    """
    # if necessary make output directory
    if not os.path.isdir(Constants.OUTPUT_FOLDER):
        os.mkdir(Constants.OUTPUT_FOLDER)

    # if KAGGLE_OUTPUT exists, delete it
    if os.path.isfile(Constants.KAGGLE_OUTPUT):
        os.remove(Constants.KAGGLE_OUTPUT)

    #variable init
    all_season_kaggle_probabilities = pandas.DataFrame()
    years = seasons.keys()
    years.sort()

    for year in years:
        #only write probabilities for last 5 years
        if year < (Constants.CURRENT_YEAR-5):
            continue

        season = seasons[year]
        all_season_kaggle_probabilities = all_season_kaggle_probabilities.append(season.kaggle_probabilities)

    all_season_kaggle_probabilities.to_csv(Constants.KAGGLE_OUTPUT, mode="w", index=False)
    print("Wrote Kaggle probabilities to: '%s'" % Constants.KAGGLE_OUTPUT)


def write_bracket_file(seasons):
    """
    Write tournament bracket to .txt file.
    """
    # if necessary make output directory
    if not os.path.isdir(Constants.OUTPUT_FOLDER):
        os.mkdir(Constants.OUTPUT_FOLDER)

    # if KAGGLE_OUTPUT exists, delete it
    if os.path.isfile(Constants.KAGGLE_OUTPUT):
        os.remove(Constants.KAGGLE_OUTPUT)

    #variable init
    years = seasons.keys()
    years.sort()
    handle = open(Constants.BRACKET_OUTPUT, "w")

    for year in years:
        season = seasons[year]

        if season.bracket.bracket == Constants.TOURNAMENT_BRACKET:
            continue

        # write bracket to  file
        handle.write(season.get_bracket() + "\n")

    handle.close()

    print("Wrote Bracket file to: '%s'" % Constants.BRACKET_OUTPUT)