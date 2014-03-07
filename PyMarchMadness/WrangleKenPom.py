#!/usr/bin/env python
"""Insert unique team id's to Ken Pomeroy data files."""

import csv
import os
import pdb

import Constants


if __name__ == "__main__":
    # variable init
    kaggle_name_to_kaggle_id = {}
    kenpom_name_to_kaggle_id = {}

    ################################################################################
    # read Kaggle/teams.csv and build kaggle_name_to_kaggle_id dictionary with
    # relationships between team names and ids
    ################################################################################
    file_path = os.path.join(Constants.INPUT_FOLDER, "Kaggle", "teams.csv")
    handle = open(file_path, 'r')
    reader = csv.reader(handle)
    for row in reader:
        team_name = row[1]
        team_id = row[0]
        kaggle_name_to_kaggle_id[team_name] = team_id
    handle.close()

    ################################################################################
    # Open each KenPom file and insert a new column with the Kaggle team_id that
    # corresponds to each team_name.
    #
    # Attempt automated replacement by matching the KenPom team name to the Kaggle
    # team name, if no match is found then prompt the user to find a match between
    # the 2 sets of team names.
    ################################################################################
    source_kenpom_dir = os.path.join(Constants.INPUT_FOLDER, 'KenPom')
    dest_kenpom_dir = os.path.join(Constants.INPUT_FOLDER, 'KenPomWithIds')
    for source_file_name in os.listdir(source_kenpom_dir):
        # read in source KenPom file
        source_file_path = os.path.join(source_kenpom_dir, source_file_name)
        source_handle = open(source_file_path, 'r')
        source_csv = csv.reader(source_handle)

        # if necessary create destination KenPom directory
        if not os.path.isdir(dest_kenpom_dir):
            os.mkdir(dest_kenpom_dir)

        # open destination KenPom file
        dest_file_path = os.path.join(dest_kenpom_dir, source_file_name)
        if os.path.isfile(dest_file_path):
            # if destination file already exists, then delete it
            os.remove(dest_file_path)
        dest_handle = open(dest_file_path, 'w')
        dest_csv = csv.writer(dest_handle)

        #look through each row in source file, modify, and write to destination file
        for row in source_csv:
            kenpom_team_name = row[0]

            # header row, insert TeamId column title
            if kenpom_team_name == 'TeamName':
                row.insert(0, 'TeamId')
                dest_csv.writerow(row)
                continue

            # exactly matched kenpom_team_name, insert team_id into row
            if kaggle_name_to_kaggle_id.get(kenpom_team_name):
                row.insert(0, kaggle_name_to_kaggle_id.get(kenpom_team_name))
                dest_csv.writerow(row)
                continue

            # user already defined mapping for this team name, insert team_id into row
            if kenpom_name_to_kaggle_id.get(kenpom_team_name):
                row.insert(0, kenpom_name_to_kaggle_id.get(kenpom_team_name))
                dest_csv.writerow(row)
                continue

            # prompt user to define mapping between KenPom & Kaggle name with CONSOLIDATED list
            kenpom_words = kenpom_team_name.split(" ")
            kaggle_team_names = kaggle_name_to_kaggle_id.keys()
            kaggle_team_names.sort()
            kaggle_team_names_potential_matches = []
            #search for kaggle names that match any word in kenpom name
            for word in kenpom_words:
                for kaggle_team_name in kaggle_team_names:
                    if word in kaggle_team_name and \
                            kaggle_team_name not in kaggle_team_names_potential_matches:
                        kaggle_team_names_potential_matches.append(kaggle_team_name)
            #prompt user to perform match
            prompt = "Enter the number of the team that matches: '%s', or None if no match.\n" % kenpom_team_name
            for i in range(len(kaggle_team_names_potential_matches)):
                prompt += "\t%d. %s" % (i, kaggle_team_names_potential_matches[i])
            index = raw_input(prompt + "\n")
            if index.isdigit():
                #user entered a match
                matched_kaggle_team_name = kaggle_team_names_potential_matches[int(index)]
                kenpom_name_to_kaggle_id[kenpom_team_name] = kaggle_name_to_kaggle_id.get(matched_kaggle_team_name)
                row.insert(0, kenpom_name_to_kaggle_id.get(kenpom_team_name))
                dest_csv.writerow(row)
                continue

            # prompt user to define mapping between KenPom & Kaggle name with FULL list
            prompt = "Enter the number of the team that matches: '%s'.\n" % kenpom_team_name
            for i in range(len(kaggle_team_names)):
                prompt += "\t%d. %s" % (i, kaggle_team_names[i])
            index = raw_input(prompt + "\n")
            if index.isdigit():
                #user entered a match
                matched_kaggle_team_name = kaggle_team_names[int(index)]
                kenpom_name_to_kaggle_id[kenpom_team_name] = kaggle_name_to_kaggle_id.get(matched_kaggle_team_name)
                row.insert(0, kenpom_name_to_kaggle_id.get(kenpom_team_name))
                dest_csv.writerow(row)
                continue
            else:
                raise Exception("invalid input: '%s'" % index)

        source_handle.close()
        dest_handle.close()