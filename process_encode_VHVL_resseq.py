#!/usr/bin/python3
"""
Program:    process_encode_VHVL_resseq
File:       process_encode_VHVL_resseq.py

Version:    V1.0
Date:       09.03.2021
Function:   Encode VH/VL packing amino acids into 4d vectors for machine learning.

Description:
============
Program uses the residue identities

--------------------------------------------------------------------------
"""
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, subprocess for running external program, pandas
# for making dataframes
import sys
sys.path.append('/serv/www/html_lilian/libs')
sys.path.append('./CDRH3lib')
sys.path.append('~/sync_project/WWW/CDRH3loop')
import os
import pandas as pd
import numpy as np
import joblib
import time


# *************************************************************************
def read_csv():
    """Read the directory name from the commandline argument

        Return: pdb_direct      --- Directory of PBD files that will be processed for VH-VL packing angles

        15.03.2021  Original   By: VAB
        """

    columns = ['code', 'L/H position', 'residue']

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=columns)
    return res_file


# *************************************************************************
def make_res_seq(file):

    aggregation_func = {'residue': 'sum'}
    seq_df = file.groupby(file['code']).aggregate(aggregation_func)
    seq_df = seq_df.reset_index()
    seq_df.reset_index()['residue']
    return seq_df


# *************************************************************************
def encode(table):
    columns = ['code', "res_charge", "res_sc_nr", "res_compactness", "res_hydrophob"]
    seq_df = pd.DataFrame(columns=columns)
    for row in table.itertuples():
        seq = row[2]
        for res in seq:
            code = row[1]
            charge_of_res = charge(res)
            hydrophobicity_res = hydophobicity(res)
            compactness_res = compactness(res)
            nr_side_chain_atoms_res = nr_side_chain_atoms(res)

            seq_df = seq_df.append(
                {'code': code, "res_charge": charge_of_res, "res_sc_nr": nr_side_chain_atoms_res,
                 "res_compactness": compactness_res, "res_hydrophob": hydrophobicity_res}, ignore_index=True)
    return seq_df


# *************************************************************************
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


# *************************************************************************
def combine_by_pdb_code(table):
    col = ['code', 'encoded_res']
    itable = []
    for row in table.itertuples():
        code = row[1]

        # charge
        a = row[2]

        # side chain number
        b = row[3]

        # compactness
        c = row[4]

        # hydrophobicity
        d = row[5]

        # the last comma and space had to be added to avoid deletion of of the first vector of each added residue
        res_encoded = '{}, {}, {}, {}, '.format(a, b, c, d)
        res = [code, res_encoded]
        itable.append(res)

    temp_df = pd.DataFrame(data=itable, columns=col)

    # combine all of the encoded residues for a specific pdb file into a single row
    enc_df = temp_df.groupby(temp_df['code']).aggregate(np.sum)
    enc_df = enc_df.reset_index()
    enc_df.reset_index()['encoded_res']

    # re-make pdb codes as a single column
    pdb_code_df = pd.Series(enc_df.code, name='code')

    #
    res_df = pd.DataFrame(enc_df.encoded_res.str.split(', ').tolist(),
                      columns=['L38a', 'L38b', 'L38c', 'L38d', 'L40a', 'L40b', 'L40c', 'L40d',
                               'L41a', 'L41b', 'L41c', 'L41d', 'L44a', 'L44b', 'L44c', 'L44d',
                               'L46a', 'L46b', 'L46c', 'L46d', 'L87a', 'L87b', 'L87c', 'L87d',
                               'H33a', 'H33b', 'H33c', 'H33d', 'H42a', 'H42b', 'H42c', 'H42d',
                               'H45a', 'H45b', 'H45c', 'H45d', 'H60a', 'H60b', 'H60c', 'H60d',
                               'H62a', 'H62b', 'H62c', 'H62d', 'H91a', 'H91b', 'H91c', 'H91d',
                               'H105a', 'H105b', 'H105c', 'H105d', 'trash'])
    res_df = res_df.iloc[:, :-1]

    encoded_df = pd.concat([pdb_code_df, res_df], axis=1)
    return encoded_df






# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

read_file = read_csv()
# print(read_file)

res_seq = make_res_seq(read_file)
# print(res_seq)


parameters = encode(res_seq)
# print(parameters.groupby(['code']))

results = combine_by_pdb_code(parameters)
results.to_csv('things.csv', index=False)