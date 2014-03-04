import os
import pandas
import pdb

import Constants
import Misc
import Season


#if this file was executed directly, then perform following
if __name__ == "__main__":
    #analyze each available season
    seasons = {}
    for _, row in Constants.KAGGLE_INPUT['seasons'].iterrows():
        print("Analyzing %s" % row['years'])
        year = int(row['years'].split("-")[1])

        seasons[year] = Season.Season(id=row['season'], years=row['years'], day_zero=row['dayzero'])
        seasons[year].set_regions(region_w=row['regionW'], region_x=row['regionX'], region_y=row['regionY'], region_z=row['regionZ'])

        seasons[year].build_teams()
        seasons[year].generate_kaggle_probabilities()
        seasons[year].generate_bracket()

    #write output to files
    Misc.write_bracket_file(seasons)
    Misc.write_kaggle_probabilities_file(seasons)