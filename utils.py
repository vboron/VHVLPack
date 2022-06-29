#!/usr/bin/python3
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
