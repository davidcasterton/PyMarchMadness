import os
import pandas


# Kaggle data from http://www.kaggle.com/c/march-machine-learning-mania/data
KAGGLE_DATA = {}  # dictionary storing DataFrames of data from Kaggle.com
KAGGLE_DATA['regular_season_results'] = pandas.read_csv('Kaggle/regular_season_results.csv')
KAGGLE_DATA['seasons'] = pandas.read_csv('Kaggle/seasons.csv')
KAGGLE_DATA['teams'] = pandas.read_csv('Kaggle/teams.csv')
KAGGLE_DATA['tourney_results'] = pandas.read_csv('Kaggle/tourney_results.csv')
KAGGLE_DATA['tourney_seeds'] = pandas.read_csv('Kaggle/tourney_seeds.csv')
KAGGLE_DATA['tourney_slots'] = pandas.read_csv('Kaggle/tourney_slots.csv')


# KenPom data from http://kenpom.com/
KENPOM_DATA = {}  # dictionary storing DataFrames of data from KenPom.com
_kenpom_dir = "KenPomWithIds"
for _file_name in os.listdir(_kenpom_dir):
        _file_path = os.path.join(_kenpom_dir, _file_name)
        _file_base_name = _file_name.split(".")[0]
        KENPOM_DATA[_file_base_name] = pandas.read_csv(_file_path)


TOURNAMENT_BRACKET = {
    'R01': {
        'W01': None, 'W02': None, 'W03': None, 'W04': None, 'W05': None, 'W06': None, 'W07': None, 'W08': None, 'W09': None, 'W10': None, 'W11': None, 'W12': None, 'W13': None, 'W14': None, 'W15': None, 'W16': None,
        'X01': None, 'X02': None, 'X03': None, 'X04': None, 'X05': None, 'X06': None, 'X07': None, 'X08': None, 'X09': None, 'X10': None, 'X11': None, 'X12': None, 'X13': None, 'X14': None, 'X15': None, 'X16': None,
        'Y01': None, 'Y02': None, 'Y03': None, 'Y04': None, 'Y05': None, 'Y06': None, 'Y07': None, 'Y08': None, 'Y09': None, 'Y10': None, 'Y11': None, 'Y12': None, 'Y13': None, 'Y14': None, 'Y15': None, 'Y16': None,
        'Z01': None, 'Z02': None, 'Z03': None, 'Z04': None, 'Z05': None, 'Z06': None, 'Z07': None, 'Z08': None, 'Z09': None, 'Z10': None, 'Z11': None, 'Z12': None, 'Z13': None, 'Z14': None, 'Z15': None, 'Z16': None,
    },
    'R02': {
        'W01': None, 'W02': None, 'W03': None, 'W04': None, 'W05': None, 'W06': None, 'W07': None, 'W08': None,
        'X01': None, 'X02': None, 'X03': None, 'X04': None, 'X05': None, 'X06': None, 'X07': None, 'X08': None,
        'Y01': None, 'Y02': None, 'Y03': None, 'Y04': None, 'Y05': None, 'Y06': None, 'Y07': None, 'Y08': None,
        'Z01': None, 'Z02': None, 'Z03': None, 'Z04': None, 'Z05': None, 'Z06': None, 'Z07': None, 'Z08': None,
    },
    'R03': {
        'W01': None, 'W02': None, 'W03': None, 'W04': None,
        'X01': None, 'X02': None, 'X03': None, 'X04': None,
        'Y01': None, 'Y02': None, 'Y03': None, 'Y04': None,
        'Z01': None, 'Z02': None, 'Z03': None, 'Z04': None,
    },
    'R04': {
        'W01': None, 'W02': None,
        'X01': None, 'X02': None,
        'Y01': None, 'Y02': None,
        'Z01': None, 'Z02': None,
    },
    'R05': {
        'W01': None,
        'X01': None,
        'Y01': None,
        'Z01': None,
    },
    'R06': {
        'W0X0': None,
        'Y0Z0': None,
    },
    'R07': {
        'CH': None
    }
}