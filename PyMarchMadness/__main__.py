#!/usr/bin/env python
"""
Predict outcome of NCAA March Madness tournaments.

Load data, analyze, and output results.
"""
import os
import pandas
import pdb
import sys

import Analysis
import Constants
import Basketball
import Misc


if __name__ == "__main__":
    tournaments = {}
    analysis_options = Analysis.get_objects()
    num_analysis_options = len(analysis_options)

    # prompt user to select analysis method
    prompt = "Please enter number of desired analysis method:\n"
    for i in range(num_analysis_options):
        prompt += "%s) %s\n" % (i, analysis_options[i].get_name())
    user_input = raw_input(prompt)

    # check user input
    if user_input.isdigit() and (int(user_input) in range(num_analysis_options)):
        analysis = analysis_options[int(user_input)]
    else:
        raise Exception("Invalid entry '%s', please enter one of following values %s." % (user_input, range(num_analysis_options)))

    # create TeamFactory
    team_factory = Basketball.TeamFactory()
    team_factory.add_all_teams()

    # analyze each available season
    Misc.check_input_data("Kaggle", "seasons")
    for _, row in Constants.INPUT_DATA['Kaggle']['seasons'].iterrows():
        year = Misc.get_tournament_year(row.years)
        print("Predicting %s NCAA Tournament" % year)

        season_id = Constants.SEASON_YEAR_TO_ID[year]
        if analysis.data_available(season_id):
            tournament = Basketball.Tournament(team_factory, season_id)

            tournament.generate_matchup_probabilities(analysis)
            tournament.generate_bracket(analysis)

            tournaments[row.season] = tournament

    # if necessary make output directory
    if not os.path.isdir(Constants.OUTPUT_DIR):
        os.mkdir(Constants.OUTPUT_DIR)

    # aggregate matchup probability DataFrames from multiple seasons
    matchup_probabilities = pandas.DataFrame()
    for year in range(Constants.CURRENT_YEAR-5, Constants.CURRENT_YEAR):
        season_id = Constants.SEASON_YEAR_TO_ID[year]
        tournament = tournaments.get(season_id)
        if tournament:
            matchup_probabilities = matchup_probabilities.append(tournament.get_matchup_probabilities())
    # write matchup probabilities file
    file_path = os.path.join(Constants.OUTPUT_DIR, "%s-matchup_probabilities.csv" % analysis.get_name(remove_spaces=True))
    matchup_probabilities.to_csv(file_path, mode="w", index=False)
    print("Wrote match up probabilities to: '%s'" % file_path)

    # write bracket file
    file_path = os.path.join(Constants.OUTPUT_DIR, "%s-tournament_brackets.txt" % analysis.get_name(remove_spaces=True))
    handle = open(file_path, "w")
    season_ids = Constants.SEASON_ID_TO_YEAR.keys()
    season_ids.sort()
    for season_id in season_ids:
        tournament = tournaments.get(season_id)
        bracket = tournament.get_bracket()
        if bracket != Constants.TOURNAMENT_BRACKET:
            handle.write(bracket)
    handle.close()
    print("Wrote tournament brackets to: '%s'" % file_path)