#!/usr/bin/env python
"""Loads input data files and defines constant values."""

import datetime
import os
import pandas
import pdb

import Misc


# misc variables
CURRENT_YEAR = datetime.date.today().year
INDENTATION = "    "

# input data variables
BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "InputData")
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputData")
INPUT_DATA = {}

# load InputData into pandas DataFrames
for _sub_dir in os.listdir(INPUT_DIR):
    _sub_path = os.path.join(INPUT_DIR, _sub_dir)

    if not os.path.isdir(_sub_path):
        #skip non directories
        continue

    INPUT_DATA[_sub_dir] = {}
    for _file in os.listdir(_sub_path):
        _file_path = os.path.join(_sub_path, _file)
        _file_base_name, _extension = os.path.splitext(_file)
        if _extension == ".csv":
            INPUT_DATA[_sub_dir][_file_base_name] = pandas.read_csv(_file_path)
        elif _extension == ".xls":
            INPUT_DATA[_sub_dir][_file_base_name] = pandas.read_excel(_file_path, 0, index_col=None, na_values=['NA'])

# lookup dictionaries based on input data
SEASON_ID_TO_YEAR = {}
DIVISIONS = {}
SEASON_YEAR_TO_ID = {}
if Misc.check_input_data("Kaggle", "seasons", raise_exception=False):
    df = INPUT_DATA['Kaggle']['seasons']
    for _, row in df.iterrows():
        season_id = row['season']
        tournament_year = Misc.get_tournament_year(row['years'])

        SEASON_YEAR_TO_ID[tournament_year] = season_id
        SEASON_ID_TO_YEAR[season_id] = tournament_year
        DIVISIONS[season_id] = {
            "W": row['regionW'],
            "X": row['regionX'],
            "Y": row['regionY'],
            "Z": row['regionZ'],
        }

# blank tournament bracket
TOURNAMENT_BRACKET = {
    'R00': {
        'W01': None, 'W02': None, 'W03': None, 'W04': None, 'W05': None, 'W06': None, 'W07': None, 'W08': None, 'W09': None, 'W10': None, 'W11': None, 'W12': None, 'W13': None, 'W14': None, 'W15': None, 'W16': None,
        'X01': None, 'X02': None, 'X03': None, 'X04': None, 'X05': None, 'X06': None, 'X07': None, 'X08': None, 'X09': None, 'X10': None, 'X11': None, 'X12': None, 'X13': None, 'X14': None, 'X15': None, 'X16': None,
        'Y01': None, 'Y02': None, 'Y03': None, 'Y04': None, 'Y05': None, 'Y06': None, 'Y07': None, 'Y08': None, 'Y09': None, 'Y10': None, 'Y11': None, 'Y12': None, 'Y13': None, 'Y14': None, 'Y15': None, 'Y16': None,
        'Z01': None, 'Z02': None, 'Z03': None, 'Z04': None, 'Z05': None, 'Z06': None, 'Z07': None, 'Z08': None, 'Z09': None, 'Z10': None, 'Z11': None, 'Z12': None, 'Z13': None, 'Z14': None, 'Z15': None, 'Z16': None,
    },
    'R01': {
        'W01': None, 'W02': None, 'W03': None, 'W04': None, 'W05': None, 'W06': None, 'W07': None, 'W08': None,
        'X01': None, 'X02': None, 'X03': None, 'X04': None, 'X05': None, 'X06': None, 'X07': None, 'X08': None,
        'Y01': None, 'Y02': None, 'Y03': None, 'Y04': None, 'Y05': None, 'Y06': None, 'Y07': None, 'Y08': None,
        'Z01': None, 'Z02': None, 'Z03': None, 'Z04': None, 'Z05': None, 'Z06': None, 'Z07': None, 'Z08': None,
    },
    'R02': {
        'W01': None, 'W02': None, 'W03': None, 'W04': None,
        'X01': None, 'X02': None, 'X03': None, 'X04': None,
        'Y01': None, 'Y02': None, 'Y03': None, 'Y04': None,
        'Z01': None, 'Z02': None, 'Z03': None, 'Z04': None,
    },
    'R03': {
        'W01': None, 'W02': None,
        'X01': None, 'X02': None,
        'Y01': None, 'Y02': None,
        'Z01': None, 'Z02': None,
    },
    'R04': {
        'W01': None,
        'X01': None,
        'Y01': None,
        'Z01': None,
    },
    'R05': {
        'WX': None,
        'YZ': None,
    },
    'R06': {
        'CH': None
    }
}