#!/usr/bin/python3
"""
Program:    encode_ts
File:       encode_ts.py

Version:    V1.0
Date:       15.04.2021
Function:   Encode VH/VL packing amino acids into 4d vectors for machine learning.

Description:
============
Program uses the residue identities for VH/VL relevant residues and encodes them using 5 vectors (T-Scale)
then appends the packing angle to produce a data table:
e.g.

------------------------------------------------
"""
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, pandas for making dataframes
import sys
import pandas as pd
import numpy as np



# *************************************************************************
def read_csv():
    """Read the file containing pdb id and the VHVL residue identity

        Return: res_file      --- Data file with residue identities read by column names

        15.03.2021  Original   By: VAB
        """

    # The column names contained in the .csv file
    col1 = ['code', 'L/H position', 'residue']

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=col1)

    return res_file


# *************************************************************************
def make_res_seq(rfile):
    """Take all individual residue identities for a pdb file and combine them into a single sequence for
    each individual pdb

    Input:  rfile       --- Dataframe containing residue identities for VHVL region
    Return: seq_df      --- Dataframe containing the pdb code and the sequence of VHVL residues for each pdb
    e.g.
        code        residue
0     12E8_1  QPGPLFYELVKYQ
1     12E8_2  QPGPLFYELVKYQ
2     15C8_1  QPGPLYYELDKYQ

    10.04.2021  Original   By: VAB
    """

    # Add all items under the 'residue' column into one field
    aggregation_func = {'residue': 'sum'}

    # Group rows  by pdb code and then combine them into one field
    #         residue
    # code
    # 12E8_1  QPGPLFYELVKYQ
    # 12E8_2  QPGPLFYELVKYQ

    seq_df = rfile.groupby(rfile['code']).aggregate(aggregation_func)

    # Reset the indices back to single row of column names for easier manipulation:
    #         code        residue
    # 0     12E8_1  QPGPLFYELVKYQ
    # 1     12E8_2  QPGPLFYELVKYQ

    seq_df = seq_df.reset_index()
    return seq_df


# *************************************************************************
def encode(table):
    """Take all individual residue identities for a pdb file and combine them into a single sequence for
       each individual pdb

       Input:  rfile       --- Dataframe containing residue identities for VHVL region
       Return: seq_df      --- Dataframe containing the pdb code and the sequence of VHVL residues for each pdb
       e.g.
           code        residue
   0     12E8_1  QPGPLFYELVKYQ
   1     12E8_2  QPGPLFYELVKYQ
   2     15C8_1  QPGPLYYELDKYQ

       10.04.2021  Original   By: VAB
       """

    columns = ['code', 'T1', 'T2', 'T3', 'T4', 'T5']
    seq_df = pd.DataFrame(columns=columns)

    # Iterate through all rows in the datatable as sets of tuples
    for row in table.itertuples():
        seq = row[2]
        for res in seq:
            code = row[1]
            t1_res = t1(res)
            t2_res = t2(res)
            t3_res = t3(res)
            t4_res = t4(res)
            t5_res = t5(res)

            seq_df = seq_df.append(
                {'code': code, "T1": t1_res, "T2": t2_res,
                 "T3": t3_res, "T4": t4_res, 'T5': t5_res}, ignore_index=True)
    return seq_df


def t1(resi):
    T1_dic = {'A': -9.11, 'R': 0.23, "N": -4.62, "D": -4.65, "C": -7.35, "Q": -3, "E": -3.03,
               "G": -10.61, "H": -1.01, "I": -4.25,
               "L": -4.38, "K": -2.59, "M": -4.08, "F": 0.49, "P": -5.11,
               "S": -7.44, "T": -5.97, "W": 5.73, "Y": 2.08, "V": -5.87, "X": -3.73}  # "X" is average
    T1 = T1_dic[resi]
    return T1


def t2(resi):

    T2_dic = {'A': -1.63, 'R': 3.89, "N": 0.66, "D": 0.75, "C": -0.86, "Q": 1.72, "E": 1.82, "G": -1.21,
              "H": -1.31, "I": -0.28, "L": 0.28, "K": 2.34, "M": 0.98, "F": -0.94, "P": -3.54,
              "S": -0.65, "T": -0.62, "W": -2.67, "Y": -0.47, "V": -0.94, "X": -0.18}  # 'X' is average
    T2 = T2_dic[resi]
    return T2


def t3(resi):
    T3_dic = {'A': 0.63, 'R': -1.16, "N": 1.16, "D": 1.39, "C": -0.33, "Q": 0.28, "E": 0.51,
              "G": -0.12, "H": 0.01, "I": -0.15, "L": -0.49, "K": -1.69, "M": -2.34, "F": -0.63, "P": -0.53,
              "S": 0.68, "T": 1.11, "W": -0.07, "Y": 0.07, "V": 0.28, "X": -0.03}  # -0.03 is average

    T3 = T3_dic[resi]
    return T3


def t4(resi):
    T4_dic = {'A': 1.04, 'R': -0.39, "N": -0.22, "D": -0.40, "C": 0.80, "Q": -0.39, "E": -0.58,
              "G": 0.75, "H": -1.81, "I": 1.40, "L": 1.45, "K": 0.41, "M": 1.64, "F": -1.27, "P": -0.36,
              "S": -0.17, "T": 0.31, "W": -1.96, "Y": -1.67, "V": 1.10, "X": -0.07}  # -0.07 is average

    T4 = T4_dic[resi]
    return T4


def t5(resi):
    T5_dic = {'A': 2.26, 'R': -0.06, "N": 0.93, "D": 1.05, "C": 0.98, "Q": 0.33, "E": 0.43,
              "G": 3.25, "H": -0.21, "I": -0.21, "L": 0.02, "K": -0.21, "M": -0.79, "F": -0.44, "P": -0.29,
              "S": 1.58, "T": 0.95, "W": -0.54, "Y": -0.35, "V": 0.48, "X": 0.35}  # 0.35 is average

    T5 = T5_dic[resi]
    return T5


# *************************************************************************
def combine_by_pdb_code(table):
    """Take all individual residue identities for a pdb file and combine them into a single sequence for
    each individual pdb

    Input:  table            --- Data frame containing the residue sequence for each pdb
    Return: training_df      --- Dataframe containing the pdb code, all encoded residues and the packing angle
    e.g.
        code L38a L38b L38c   L38d L40a  ...  H91d H105a H105b H105c  H105d angle
0     12E8_1    0    5    4  -0.69    0  ...  0.02     0     5     4  -0.69 -54.9
1     12E8_2    0    5    4  -0.69    0  ...  0.02     0     5     4  -0.69 -48.5

    10.04.2021  Original   By: VAB
    """

    col = ['code', 'encoded_res']
    itable = []
    for row in table.itertuples():
        code = row[1]
        a = row[2]
        b = row[3]
        c = row[4]
        d = row[5]
        e = row[6]


        # the last comma and space had to be added to avoid deletion of of the first vector of each added residue
        res_encoded = '{}, {}, {}, {}, {}, '.format(a, b, c, d, e)
        res = [code, res_encoded]
        itable.append(res)

    temp_df = pd.DataFrame(data=itable, columns=col)

    # Combine all of the encoded residues for a specific pdb file into a single row
    enc_df = temp_df.groupby(temp_df['code']).aggregate(np.sum)
    enc_df = enc_df.reset_index()

    # Re-make pdb codes as a single column
    pdb_code_df = pd.Series(enc_df.code, name='code')

    # Split combined codes into separate fields with the position and parameter as the column name
    # ('trash' column created because the adjustment above that corrects data removal
    # ends up creating a blank column)

    col2 = []
    for i in open(sys.argv[3]).readlines():
        i = i.strip('\n')
        col2.append(i)

    col2.remove('code')
    col2.append('trash')
    col2.remove('angle')

    res_df = pd.DataFrame(enc_df.encoded_res.str.split(', ').tolist(),
                      columns=col2)

    # Remove the blank column
    res_df = res_df.iloc[:, :-1]

    # Add column containing pdb codes to the table of encoded residues
    encoded_df = pd.concat([pdb_code_df, res_df], axis=1)

    col3 = ['code', 'angle']

    # Take the second input from the commandline (which will be the table of pdb codes and their packing angles)
    if sys.argv[2] != '':
        angle_file = pd.read_csv(sys.argv[2], usecols=col3)

    # Angle column will be added to the table of encoded residues and the table is sorted by code
    # to make sure all the data is for the right pdb file
    training_df = pd.merge(encoded_df, angle_file, how="right", on=["code"], sort=True)
    nan_value = float('NaN')
    training_df.replace('', nan_value, inplace=True)
    training_df.dropna(axis=0, how='any', inplace=True)

    return training_df


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

read_file = read_csv()
# print(read_file)

res_seq = make_res_seq(read_file)
#print(res_seq)


parameters = encode(res_seq)
#print(parameters)

results = combine_by_pdb_code(parameters)
results.to_csv('{}.csv'.format(sys.argv[4]), index=False)
