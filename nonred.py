#!/usr/bin/python3
import os
import pandas as pd
from utils import one_letter_code

# *************************************************************************
def make_seq_pdb_dict(dir_of_pdbs):
    """Read PDB files as lines, then make a dictionary of the PDB code and all the lines that start with 'ATOM'

    Return: pdb_dict    --- Dictionary of PDB names with all of the lines containing atom details
    e.g.

    16.12.2021  Original   By: VAB
    """

    # create a new directory
    seq_dict = {}

    # look through files in the directory
    for file in os.listdir(dir_of_pdbs):

        # make sure that the file is a
        if file.endswith(".pdb") or file.endswith(".ent"):

            # create the full file path so the file can be found
            file_path = os.path.join(dir_of_pdbs, file)

            # open file in 'read' mode
            with open(file_path, "r") as text_file:

                # create empty string where the sequence will be added
                sequence=''

                # Search for lines that contain the alpha carbon atoms of the amino acid
                for line in text_file.readlines():
                    if 'ATOM' in str(line) and 'CA' in str(line):

                        # split line so that we can access its elements
                        split_line = line.split()

                        # the .pdb file containes the names of the amino acids in the three-letter code
                        # we use the dictionary that we made earlier to convert these into single letter code
                        residue = one_letter_code(file, split_line[3])

                        # we add the residue into the string to create the full one-letter sequence
                        sequence = sequence + residue

                # we create a dictionary entry, where the sequence is the key and the pdb file the value. This allows
                # us to find only one file per sequence.
                seq_dict[sequence] = file

    return seq_dict


def filter_df(csv_file, seq_dict):

    df = pd.read_csv(csv_file)
    pdbcode_list = [seq_dict.values()]

    return df[~df['code'].isin(pdbcode_list)]


def NR1(dir_dataset_pdbs, out_file, encoded_csv):
    dictionary = make_seq_pdb_dict(dir_dataset_pdbs)
    nr1_dataframe = filter_df(encoded_csv, dictionary)
    nr1_path = os.path.join(dir_dataset_pdbs, f'{out_file}.csv')
    nr1_dataframe.to_csv(nr1_path, index=False)

# *************************************************************************
def NR2(encoded_df, directory, out_file):
    """Read the .csv file containing encoded residues and angles and combine lines that have the same PDB code and
    the same encoded sequence into one line, averaging the angle

    Return: seq_df      --- Dataframe that contains a single angle for all PDB files with unique sequences
    """

    col1 = list(encoded_df)
    # angle needs to be converted to a float to be averaged
    encoded_df['angle'] = encoded_df['angle'].astype(float)

    # aggregation function specifies that when the rows are grouped, the first value of code will be kept and the
    # angles will be averaged
    aggregation_func = {'code': 'first', 'angle': 'first'}

    # make a column of rounded values for angle
    encoded_df['ang2dp']=encoded_df['angle'].round(decimals=2)

    # remove 'angle' and 'code' from columns header list, since program is not grouping by these, but add the rounded
    # angle column
    col1.remove('angle')
    col1.remove('code')
    col1.append('ang2dp')

    # group by values now in col1 (residue identities and rounded angle to 2dp)
    seq_df = encoded_df.groupby(col1).aggregate(aggregation_func)

    # grouping produces a "sup" column that is over the columns that were grouped by. This resets all column names
    # to the same level
    seq_df = seq_df.reset_index()

    # to get back our original column order
    cols=seq_df.columns.tolist()
    cols = [cols[-2]]+ cols[:-3] + cols[-1:]
    seq_df=seq_df[cols]
    if '/' in out_file:
        out_file = out_file.replace('/', '')
    nr2_path = os.path.join(directory, f'{out_file}.csv')
    seq_df.to_csv(nr2_path, index=False)
    return seq_df

# *************************************************************************
def NR3(encoded_csv_file, columns, directory, out_file):
    """Read the .csv file containing encoded residues and angles and combine lines that have the same PDB code and
    the same encoded sequence into one line, averaging the angle

    Return: seq_df      --- Dataframe that contains a single angle for all PDB files with unique sequences
    """

    # The column names contained in the .csv file imported from a .dat file
    col1 = [l.strip('\n') for l in open(columns).readlines()]

    # Take the commandline input as the directory, otherwise look in current directory
    res_file = pd.read_csv(encoded_csv_file)

    # angle needs to be converted to a float to be averaged
    res_file['angle'] = res_file['angle'].astype(float)

    # aggregation function specifies that when the rows are grouped, the first value of code will be kept and the
    # angles will be averaged
    aggregation_func = {'code': 'first', 'angle': 'mean'}

    # remove 'angle' and 'code' from columns header list, since program is not grouping by these
    col1.remove('angle')
    col1.remove('code')

    seq_df = res_file.groupby(col1).aggregate(aggregation_func)
    seq_df = seq_df.reset_index()

    cols=seq_df.columns.tolist()

    cols = [cols[-2]]+ cols[:-2] + cols[-1:]
    seq_df=seq_df[cols]

    if '/' in out_file:
        out_file = out_file.replace('/', '')
    nr3_path = os.path.join(directory, f'{out_file}.csv')
    seq_df.to_csv(nr3_path, index=False)