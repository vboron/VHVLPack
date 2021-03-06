#!/usr/bin/env python3
import pandas as pd
import argparse
from ordered_set import OrderedSet
import pickle

def one_letter_code(res):
    dic = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K', 'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F',
           'ASN': 'N', 'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'ALA': 'A', 'VAL': 'V', 'GLU': 'E',
           'TYR': 'Y', 'MET': 'M', 'XAA': 'X', 'UNK': 'X'}
    if res not in dic:
        raise ValueError
    one_letter = dic[res]
    return one_letter

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
def make_param(res, param, letter):
    col = param + letter
    if letter == 'a':
        value = nr_side_chain_atoms(res)
    elif letter == 'b':
        value  = compactness(res)
    elif letter == 'c':
        value = hydophobicity(res)
    else:
        value = charge(res)
    return col, value

def seq2df(seq_file):
    good_positions = ['L38', 'L40', 'L41', 'L44', 'L46', 'L87', 'H33', 'H42', 'H45', 'H60', 'H62', 'H91', 'H105']
    dRes = {}
    kv_list = []
    with open(seq_file) as f:
        lines = f.readlines()
        for line in lines:
            line_elements = line.split()
            position = line_elements[0]
            if position in good_positions:
                identity = line_elements[1]
                identity = one_letter_code(identity)
                for letter in ['a', 'b', 'c', 'd']:
                    col, value = make_param(identity, position, letter)
                    dRes[col]=value
                    # kv_list.append((col, value))
    # print(kv_list)
    df = pd.DataFrame(dRes, index=[0])
    # print(df)
    return df

def runningGBR(df, pkl_filename):
    predictors = list(OrderedSet(df.columns))
    X_test = df[predictors].values
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    y_pred = float(pickle_model.predict(X_test))
    print(y_pred)

parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--seqfile', help='.seq file for VHVL packing', required=True)
parser.add_argument('--pklmodel', help='trained model in .pkl format', required=True)
args = parser.parse_args()

data = seq2df(args.seqfile)
runningGBR(data, args.pklmodel)