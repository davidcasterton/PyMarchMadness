#!/usr/bin/env python
""":module: Loads input data files and defines constant values."""

import datetime
import os
import pandas

__author__ = "David Casterton"
__license__ = "GPL"


VERSION = 1
CURRENT_YEAR = datetime.date.today().year
BASE_DIR = os.path.dirname(__file__)
INPUT_FOLDER = os.path.join(BASE_DIR, "InputData")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "OutputData")
KAGGLE_INPUT = {}  # dictionary storing DataFrames of data from Kaggle.com
KENPOM_INPUT = {}  # dictionary storing DataFrames of data from KenPom.com


# load Kaggle data from http://www.kaggle.com/c/march-machine-learning-mania/data
_kaggle_dir = os.path.join(INPUT_FOLDER, "Kaggle")
for _file_name in os.listdir(_kaggle_dir):
    _file_path = os.path.join(_kaggle_dir, _file_name)
    _file_base_name = _file_name.split(".")[0]
    KAGGLE_INPUT[_file_base_name] = pandas.read_csv(_file_path)


# load KenPom data from http://kenpom.com/
_kenpom_dir = os.path.join(INPUT_FOLDER, "KenPomWithIds")
for _file_name in os.listdir(_kenpom_dir):
    _file_path = os.path.join(_kenpom_dir, _file_name)
    _file_base_name = _file_name.split(".")[0]
    KENPOM_INPUT[_file_base_name] = pandas.read_csv(_file_path)


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