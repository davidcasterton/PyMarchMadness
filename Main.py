#!/usr/bin/env python
"""
Predict outcome of NCAA March Madness tournaments.

Load data, analyze, and output results.
"""

import pdb

import Analysis
import Constants
import Season

__author__ = "David Casterton"
__license__ = "GPL"


if __name__ == "__main__":
    seasons = {}

    # prompt user to select analysis method
    prompt = "Please enter number of desired analysis method:\n"
    for i in range(Analysis.num_available):
        prompt += "%s) %s\n" % (i, Analysis.available[i].get_name())
    user_input = raw_input(prompt)
    if user_input.isdigit() and (int(user_input) in range(Analysis.num_available)):
        analysis_method = Analysis.available[int(user_input)]
    else:
        raise Exception("Invalid entry '%s', please enter one of following values %s." % (user_input, range(Analysis.num_available)))

    # analyze each available season
    for _, row in Constants.KAGGLE_INPUT['seasons'].iterrows():
        print("Analyzing %s" % row['years'])
        year = int(row['years'].split("-")[1])

        # create Season object
        seasons[year] = Season.Season(id=row['season'], years=row['years'], day_zero=row['dayzero'])
        seasons[year].set_regions(region_w=row['regionW'], region_x=row['regionX'], region_y=row['regionY'], region_z=row['regionZ'])

        # build Teams and run analysis
        seasons[year].build_teams()
        seasons[year].generate_matchup_probabilities(analysis_method)
        seasons[year].generate_bracket(analysis_method)

    # write output to files
    analysis_method.write_bracket_file(seasons)
    analysis_method.write_matchup_probabilities_file(seasons)