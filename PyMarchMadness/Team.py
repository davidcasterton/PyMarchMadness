#!/usr/bin/env python
""":module: Classes representing a NCAA basketball team."""

import pandas

import Constants


class Team(object):
    """:class: 1 NCAA backetball team for 1 NCAA season."""
    def __init__(self, id, name, years):
        """
        :param string id:  team identifier, defined in Kaggle/teams.csv id column
        :param string name:  team name, defined in Kaggle/teams.csv name column
        :param string years:  2 years that NCAA season spans in format 'XXXX-YYYY'
        """
        self.id = id
        self.name = name
        self.years = years
        self.tournament_year = int(self.years.split("-")[1])

        self.kenpom_data_frame = pandas.DataFrame
        self.tourney_seed = None
        self.division = None
        self.division_seed = None
        self.pythag = None
        self.offense_efficiency = None
        self.defense_efficiency = None

    def __str__(self):
        attribute_list = list()
        attribute_list.append(self.name.ljust(20))
        attribute_list.append(("season: %s" % self.years).ljust(10))
        attribute_list.append(("id: %s" % self.id).ljust(10))
        if self.division:
            attribute_list.append(("division: %s" % self.division).ljust(20))
        if self.division_seed:
            attribute_list.append(("seed: %s" % self.division_seed).ljust(10))
        if self.pythag:
            attribute_list.append("Pythag: %s" % self.pythag)
        if self.offense_efficiency:
            attribute_list.append("Offensive efficiency: %s" % self.offense_efficiency)
        if self.defense_efficiency:
            attribute_list.append("Defensive efficiency: %s" % self.defense_efficiency)
        return "| ".join(attribute_list)

    def set_tourney_seed(self, tourney_seed, regions):
        """
        :method: Set this teams seed in the tournament.

        :param string tourney_seed: string encoding this teams division and seed
        :param dict regions: dictionary to map between division id's and division names
        """
        self.tourney_seed = str(tourney_seed)
        self.division = regions[self.tourney_seed[0]]
        self.division_seed = int(self.tourney_seed[1:2])

    def load_kenpom_data(self):
        """:method: Search KenPom dataframes and populate member variables."""
        input_file_name = 'summary%s' % str(self.tournament_year)[-2:]
        if input_file_name in Constants.KENPOM_INPUT.keys():
            df = Constants.KENPOM_INPUT[input_file_name]
            self.kenpom_data_frame = df[df.TeamId == self.id]  # single row from summaryXX.csv for this team
            if not self.kenpom_data_frame.empty:
                self.pythag = self.kenpom_data_frame.Pythag.iloc[0]
                self.offense_efficiency = self.kenpom_data_frame.AdjOE.iloc[0]
                self.defense_efficiency = self.kenpom_data_frame.AdjDE.iloc[0]
            else:
                raise Exception("KenPom data not found for team name:'%s', id:'%s'" % (self.name, self.id))