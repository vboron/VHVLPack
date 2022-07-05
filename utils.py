#!/usr/bin/python3
from cmath import nan
import math
import subprocess
import pandas as pd
import numpy as np

# *************************************************************************


def one_letter_code(pdb, res):
    """
    Go from the three-letter code to the one-letter code.

    Input:  residue      --- Three-letter residue identifier
    Return: one_letter   --- The one-letter residue identifier

    20.10.2020  Original   By: LD
    """

    dic = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K', 'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F',
           'ASN': 'N', 'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'ALA': 'A', 'VAL': 'V', 'GLU': 'E',
           'TYR': 'Y', 'MET': 'M', 'XAA': 'X', 'UNK': 'X'}
    if res not in dic:
        raise ValueError("{}: {} not in dic".format(pdb, res))

    one_letter = dic[res]
    return one_letter

# *************************************************************************


def run_cmd(cmd_list, is_dry_run: bool, stdout=None, env=None, cwd=None, stderr=None):
    log_msg = f"Running {cmd_list}"
    # if env is not None:
    #     log_msg += f'; env={env}'
    #     env.update(os.environ.copy())
    if cwd is not None:
        log_msg += f'; cwd={cwd}'
    print(log_msg)
    if not is_dry_run:
        comp_process = subprocess.run(
            cmd_list, stdout=stdout, env=env, cwd=cwd, stderr=stderr)
        comp_process.check_returncode()

# *************************************************************************


def calc_relemse_from_csv(results_csv, rmse):
    """Read the .csv for angles and take the RMSE from the commandline to calculate the relative RMSE.
    Equation used: RELRMSE = (RMSE*(n**(1/2)))/((sum (angle**2))**(1/2))

    Inputs: results_csv  --- The dataframe containing the predictions and errors
            columns      --- Columns for postprocessing
            rmse         --- Input numerical rmse
    Return: relrmse      --- The relative RMSE
    """

    df = pd.read_csv(results_csv)

    # Take the rmse from the second commandline input and convert it into a float
    rmse = float(rmse)

    # Count the number of angles in the dataframe
    n = df['angle'].count()

    # Take the square root of the number of angles
    rn = float(n)**(1/2)

    # Makes a list of all the angles squared
    sq_angle = []
    for angle in df['angle']:
        angle_2 = float(angle)**2
        sq_angle.append(angle_2)

    col2 = ['sqangle']

    # Create a dataframe of all angles squared
    df2 = pd.DataFrame(data=sq_angle, columns=col2)

    # Take the sum of all the square angles
    c_sangles = df2['sqangle'].sum()

    # Take the sqroot of summed square angles
    rc_sangles = float(c_sangles)**(1/2)

    relrmse = (rmse*rn)/rc_sangles
    return relrmse

# *************************************************************************


def relrmse_from_df(df, rmse):
    """Read the df for angles and take the RMSE from the commandline to calculate the relative RMSE.
    Equation used: RELRMSE = (RMSE*(n**(1/2)))/((sum (angle**2))**(1/2))

    Inputs: df           --- The dataframe containing the predictions and errors
            rmse         --- Input numerical rmse
    Return: relrmse      --- The relative RMSE
    """

    rmse = float(rmse)

    # Count the number of angles in the dataframe
    n = df['angle'].count()

    # Take the square root of the number of angles
    rn = float(n)**(1/2)

    # Makes a list of all the angles squared
    sq_angle = []
    for angle in df['angle']:
        angle_2 = float(angle)**2
        sq_angle.append(angle_2)

    col2 = ['sqangle']

    # Create a dataframe of all angles squared
    df2 = pd.DataFrame(data=sq_angle, columns=col2)

    # Take the sum of all the square angles
    c_sangles = df2['sqangle'].sum()

    # Take the sqroot of summed square angles
    rc_sangles = float(c_sangles)**(1/2)

    relrmse = (rmse*rn)/rc_sangles
    return relrmse

# *************************************************************************


def stats_for_pred_vs_actual_graph(df):

    df['sqerror'] = np.square(df['error'])
    sum_sqerror = df['sqerror'].sum()
    average_error = sum_sqerror / int(df['angle'].size)
    rmse = math.sqrt(average_error)

    relrmse = relrmse_from_df(df, rmse)

    # .corr() returns the correlation between two columns
    pearson_a = df['angle'].corr(df['predicted'])

    mean_abs_err = df['error'].abs().mean()
    stat_data = [pearson_a, mean_abs_err, rmse, relrmse]
    stat_col = ['pearson', 'error', 'RMSE', 'RELRMSE']
    stats_df = pd.DataFrame(data=[stat_data], columns=stat_col)
    return stats_df, stat_data

# *************************************************************************
def nr_side_chain_atoms(resi):
    # 1. total number of side-chain atoms
    nr_side_chain_atoms_dic = {'A': 1, 'R': 7, "N": 4, "D": 4, "C": 2, "Q": 5, "E": 5, "G": 0, "H": 6, "I": 4,
                               "L": 4, "K": 15, "M": 4, "F": 7, "P": 4,
                               "S": 2, "T": 3, "W": 10, "Y": 8, "V": 3, "X": 10.375, "nan": 10.375}  # "X": 10.375
    nr_side_chain_atoms = nr_side_chain_atoms_dic[resi]
    return nr_side_chain_atoms

# *************************************************************************
def compactness(resi):
    # 2. number of side-chain atoms in shortest path from Calpha to most distal atom
    compactness_dic = {'A': 1, 'R': 6, "N": 3, "D": 3, "C": 2, "Q": 4, "E": 4, "G": 0, "H": 4, "I": 3,
                       "L": 3, "K": 6, "M": 4, "F": 5, "P": 2,
                       "S": 2, "T": 2, "W": 6, "Y": 6, "V": 2, "X": 4.45}  # , "X": 4.45
    compactness = nan
    if resi != nan:
        compactness = compactness_dic[resi]
    return compactness

# *************************************************************************
def hydrophobicity(resi):
    # 3. eisenberg consensus hydrophobicity
    # Consensus values: Eisenberg, et al 'Faraday Symp.Chem.Soc'17(1982)109
    Hydrophathy_index = {'A': 00.250, 'R': -1.800, "N": -0.640, "D": -0.720, "C": 00.040, "Q": -0.690, "E": -0.620,
                         "G": 00.160, "H": -0.400, "I": 00.730, "L": 00.530, "K": -1.100, "M": 00.260, "F": 00.610,
                         "P": -0.070,
                         "S": -0.260, "T": -0.180, "W": 00.370, "Y": 00.020, "V": 00.540, "X": -0.5}  # -0.5 is average

    hydrophobicity = Hydrophathy_index[resi]
    return hydrophobicity

# *************************************************************************
def charge(resi):
    dic = {"D": -1, "K": 1, "R": 1, 'E': -1, 'H': 0.5}
    charge = 0
    if resi in dic:
        charge += dic[resi]
    return charge