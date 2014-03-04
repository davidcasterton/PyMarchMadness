import os
import pandas
import pdb

import Constants
from Season import Season


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


def write_bracket_to_file(seasons):
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

        # skip blank brackets
        if season.tournament_bracket == Constants.TOURNAMENT_BRACKET:
            continue

        # write bracket to  file
        handle.write(season.get_bracket() + "\n")

    handle.close()

    print("Wrote Bracket file to: '%s'" % Constants.BRACKET_OUTPUT)


if __name__ == "__main__":
    #analyze each available season
    seasons = {}
    for _, row in Constants.KAGGLE_INPUT['seasons'].iterrows():
        print("Analyzing %s" % row['years'])
        year = int(row['years'].split("-")[1])

        seasons[year] = Season(id=row['season'], years=row['years'], day_zero =row['dayzero'])
        seasons[year].set_regions(region_w=row['regionW'], region_x=row['regionX'], region_y=row['regionY'], region_z=row['regionZ'])

        seasons[year].build_teams()
        seasons[year].generate_kaggle_probabilities()
        seasons[year].generate_bracket()

    #write output to files
    write_bracket_to_file(seasons)
    write_kaggle_probabilities_file(seasons)