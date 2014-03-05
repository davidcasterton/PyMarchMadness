import pdb

import Analysis
import Constants
import Misc
import Season


if __name__ == "__main__":
    # Predict outcome of NCAA March Madness tournaments.

    seasons = {}
    analysis_method = Analysis.KenPom()

    # analyze each available season
    for _, row in Constants.KAGGLE_INPUT['seasons'].iterrows():
        print("Analyzing %s" % row['years'])
        year = int(row['years'].split("-")[1])

        # create Season object
        seasons[year] = Season.Season(id=row['season'], years=row['years'], day_zero=row['dayzero'])
        seasons[year].set_regions(region_w=row['regionW'], region_x=row['regionX'], region_y=row['regionY'], region_z=row['regionZ'])

        # build Teams and run analysis
        seasons[year].build_teams()
        seasons[year].generate_kaggle_probabilities(analysis_method)
        seasons[year].generate_bracket(analysis_method)

    # write output to files
    Misc.write_bracket_file(seasons)
    Misc.write_kaggle_probabilities_file(seasons)