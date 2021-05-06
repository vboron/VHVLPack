#!/usr/bin/python3
"""
Program:    process_encode_VHVL_resseq
File:       process_encode_VHVL_resseq.py

Version:    V1.0
Date:       09.03.2021
Function:   Encode VH/VL packing amino acids into 4d vectors for machine learning.

Description:
============
Program uses the residue identities for VH/VL relevant residues and encodes them using 4 vectors (hydrophobicity,
side chain size, charge, and compactness) then appends the packing angle to produce a data table:
e.g.

code	L38a	L38b	L38c	L38d	L40a	...     angle
12E8_1	0	       5	   4	-0.69	   0            -54.9
12E8_2	0	       5	   4	-0.69	   0            -48.5
15C8_1	0	       5	   4	-0.69	   0            -42.3
1A0Q_1	0.5	       6	   4	-0.4	   0            -45.6
------------------------------------------------
"""
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, pandas for making dataframes
import sys
sys.path.append('/serv/www/html_lilian/libs')
sys.path.append('./CDRH3lib')
sys.path.append('~/sync_project/WWW/CDRH3loop')
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
    # seq_df.reset_index()['residue']
    return seq_df


# *************************************************************************
def dual_enc(table):

    columns = ['code', "res_charge", "res_sc_nr", "res_compactness", "res_hydrophob", 'T1', 'T2', 'T3', 'T4', 'T5']
    seq_df = pd.DataFrame(columns=columns)

    # Iterate through all rows in the datatable as sets of tuples
    for row in table.itertuples():
        seq = row[2]
        for res in seq:
            code = row[1]
            charge_of_res = charge(res)
            hydrophobicity_res = hydophobicity(res)
            compactness_res = compactness(res)
            nr_side_chain_atoms_res = nr_side_chain_atoms(res)
            t1_res = t1(res)
            t2_res = t2(res)
            t3_res = t3(res)
            t4_res = t4(res)
            t5_res = t5(res)

            seq_df = seq_df.append(
                {'code': code, "res_charge": charge_of_res, "res_sc_nr": nr_side_chain_atoms_res,
                 "res_compactness": compactness_res, "res_hydrophob": hydrophobicity_res, "T1": t1_res,
                 "T2": t2_res, "T3": t3_res, "T4": t4_res, 'T5': t5_res}, ignore_index=True)
    return seq_df


def nr_side_chain_atoms(resi):
    # 1. total number of side-chain atoms
    nr_side_chain_atoms_dic = {'A': 1, 'R': 7, "N": 4, "D": 4, "C": 2, "Q": 5, "E": 5, "G": 0, "H": 6, "I": 4,
                               "L": 4, "K": 15, "M": 4, "F": 7, "P": 4,
                               "S": 2, "T": 3, "W": 10, "Y": 8, "V": 3, "X": 10.375}  # "X": 10.375
    nr_side_chain_atoms = nr_side_chain_atoms_dic[resi]
    return nr_side_chain_atoms


def compactness(resi):
    # 2. number of side-chain atoms in shortest path from Calpha to most distal atom
    compactness_dic = {'A': 1, 'R': 6, "N": 3, "D": 3, "C": 2, "Q": 4, "E": 4, "G": 0, "H": 4, "I": 3,
                       "L": 3, "K": 6, "M": 4, "F": 5, "P": 2,
                       "S": 2, "T": 2, "W": 6, "Y": 6, "V": 2, "X": 4.45}  # , "X": 4.45
    compactness = compactness_dic[resi]
    return compactness


def hydophobicity(resi):
    # 3. eisenberg consensus hydrophobicity
    # Consensus values: Eisenberg, et al 'Faraday Symp.Chem.Soc'17(1982)109
    Hydrophathy_index = {'A': 00.250, 'R': -1.800, "N": -0.640, "D": -0.720, "C": 00.040, "Q": -0.690, "E": -0.620,
                         "G": 00.160, "H": -0.400, "I": 00.730, "L": 00.530, "K": -1.100, "M": 00.260, "F": 00.610,
                         "P": -0.070,
                         "S": -0.260, "T": -0.180, "W": 00.370, "Y": 00.020, "V": 00.540, "X": -0.5}  # -0.5 is average

    hydrophobicity = Hydrophathy_index[resi]
    return hydrophobicity


def charge(resi):
    dic = {"D": -1, "K": 1, "R": 1, 'E': -1, 'H': 0.5}
    charge = 0
    if resi in dic:
        charge += dic[resi]
    return charge


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
        f = row[7]
        g = row[8]
        h = row[9]
        i = row[10]


        # the last comma and space had to be added to avoid deletion of of the first vector of each added residue
        res_encoded = '{}, {}, {}, {}, {}, {}, {}, {}, {}, '.format(a, b, c, d, e, f, g, h, i)
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
    res_df = pd.DataFrame(enc_df.encoded_res.str.split(', ').tolist(),
                      columns=['L38a', 'L38b', 'L38c', 'L38d', 'L38e', 'L38f', 'L38g', 'L38h', 'L38i',
                               'L40a', 'L40b', 'L40c', 'L40d', 'L40e', 'L40f', 'L40g', 'L40h', 'L40i',
                               'L41a', 'L41b', 'L41c', 'L41d', 'L41e', 'L41f', 'L41g', 'L41h', 'L41i',
                               'L44a', 'L44b', 'L44c', 'L44d', 'L44e', 'L44f', 'L44g', 'L44h', 'L44i',
                               'L46a', 'L46b', 'L46c', 'L46d', 'L46e', 'L46f', 'L46g', 'L46h', 'L46i',
                               'L87a', 'L87b', 'L87c', 'L87d', 'L87e', 'L87f', 'L87g', 'L87h', 'L87i',
                               'H33a', 'H33b', 'H33c', 'H33d', 'H33e', 'H33f', 'H33g', 'H33h', 'H33i',
                               'H42a', 'H42b', 'H42c', 'H42d', 'H42e', 'H42f', 'H42g', 'H42h', 'H42i',
                               'H45a', 'H45b', 'H45c', 'H45d', 'H45e', 'H45f', 'H45g', 'H45h', 'H45i',
                               'H60a', 'H60b', 'H60c', 'H60d', 'H60e', 'H60f', 'H60g', 'H60h', 'H60i',
                               'H62a', 'H62b', 'H62c', 'H62d', 'H62e', 'H62f', 'H62g', 'H62h', 'H62i',
                               'H91a', 'H91b', 'H91c', 'H91d', 'H91e', 'H91f', 'H91g', 'H91h', 'H91i',
                               'H105a', 'H105b', 'H105c', 'H105d', 'H105e', 'H105f', 'H105g', 'H105h',
                               'H105i', 'trash'])

    # Remove the blank column
    res_df = res_df.iloc[:, :-1]

    # Add column containing pdb codes to the table of encoded residues
    encoded_df = pd.concat([pdb_code_df, res_df], axis=1)

    col2 = ['code', 'angle']

    # Take the second input from the commandline (which will be the table of pdb codes and their packing angles)
    if sys.argv[2] != '':
        angle_file = pd.read_csv(sys.argv[2], usecols=col2)

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
#print(read_file)

res_seq = make_res_seq(read_file)
# print(res_seq)

encode = dual_enc(res_seq)

results = combine_by_pdb_code(encode)
results.to_csv('VHVLres_and_angles_4dTS.csv', index=False)