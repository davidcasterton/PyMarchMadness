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
for file_type in ['defense', 'misc', 'offense', 'summary']:
    for year_int in range(3, 14):
        file_name = '%s%02d' % (file_type, year_int)
        file_path = os.path.join('KenPomWithIds', file_name) + '.csv'
        KENPOM_DATA[file_name] = pandas.read_csv(file_path)

TOURNAMET_BRACKET = {
    'R1': {
        'W1': None, 'W2': None, 'W3': None, 'W4': None, 'W5': None, 'W6': None, 'W7': None, 'W8': None,
        'X1': None, 'X2': None, 'X3': None, 'X4': None, 'X5': None, 'X6': None, 'X7': None, 'X8': None,
        'Y1': None, 'Y2': None, 'Y3': None, 'Y4': None, 'Y5': None, 'Y6': None, 'Y7': None, 'Y8': None,
        'Z1': None, 'Z2': None, 'Z3': None, 'Z4': None, 'Z5': None, 'Z6': None, 'Z7': None, 'Z8': None,
    },
    'R2': {
        'W1': None, 'W2': None, 'W3': None, 'W4': None,
        'X1': None, 'X2': None, 'X3': None, 'X4': None,
        'Y1': None, 'Y2': None, 'Y3': None, 'Y4': None,
        'Z1': None, 'Z2': None, 'Z3': None, 'Z4': None,
    },
    'R3': {
        'W1': None, 'W2': None,
        'X1': None, 'X2': None,
        'Y1': None, 'Y2': None,
        'Z1': None, 'Z2': None,
    },
    'R4': {
        'W1': None,
        'X1': None,
        'Y1': None,
        'Z1': None,
    },
    'R5': {
        'WX': None,
        'YZ': None,
    }
    'R6': {
        'CH': None
    }
}