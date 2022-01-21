#!/usr/bin/python3
import os
import subprocess
import pandas as pd

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
def run_cmd(cmd_list, is_dry_run: bool, stdout=None, env=None):
    log_msg = f"Running {cmd_list}"
    if env is not None:
        log_msg += f'; env={env}'
        env.update(os.environ.copy())
    print(log_msg)
    if not is_dry_run:
        subprocess.run(cmd_list, stdout=stdout, env=env)

# *************************************************************************
def calc_relemse(results_csv, columns, rmse):
    """Read the .csv for angles and take the RMSE from the commandline to calculate the relative RMSE.
    Equation used: RELRMSE = (RMSE*(n**(1/2)))/((sum (angle**2))**(1/2))

    Inputs: results_csv  --- The dataframe containing the predictions and errors
            columns      --- Columns for postprocessing
            rmse         --- Input numerical rmse
    Return: relrmse      --- The relative RMSE
    """
    col = []
    for i in open(columns).readlines():
    i = i.strip('\n')
    col.append(i)

    df = pd.read_csv(results_csv, usecols=col)

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