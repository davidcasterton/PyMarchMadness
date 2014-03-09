#!/usr/bin/env python

import Constants


def check_input_data(directory, file_name, raise_exception=True):
    """
    :function: check Constants.INPUT_DATA for desired file.
    """
    def _fail(directory, file_name, raise_exception):
        if raise_exception:
            raise Exception("Data from InputData/%s/%s.* not loaded." % (directory, file_name))
        else:
            return False

    if not Constants.INPUT_DATA.get(directory):
        return _fail(raise_exception)

    if file_name not in Constants.INPUT_DATA[directory].keys():
        return _fail(raise_exception)

    if Constants.INPUT_DATA[directory][file_name].empty:
        return _fail(raise_exception)

    return True


def get_tournament_year(year):
        """
        :method: Return tournament year as int

        :param string/int year: possible formats: 1) int(XXXX), 2) str("XXXX"), 3) str("XXXX-YYYY")
        :returns: tournament_year
        :rtype: int
        """
        if type(year) == str:
            # convert from string to int
            tournament_year = int(year.split("-")[1])
        elif type(year) == int:
            tournament_year = year
        else:
            raise Exception("Invalid year data type '%s'" % (type(year)))

        return tournament_year