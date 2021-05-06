#!/usr/bin/python3
"""
Program:    RELRMSE
File:       RELRMSE.py

Version:    V1.0
Date:       05.05.2021
Function:   Calculate the relative root mean error for packing angle prediction

Description:
============
Program takes a .csv file containing the pdb code as 'code' and the non-normalized packing angle as 'angle', and the
RMSE calculated by program as the second input.
------------------------------------------------
"""


# *************************************************************************
# Import libraries
import sys
import pandas as pd
import numpy as np


# *************************************************************************
def calc_relemse():
    """Read the .csv for angles and take the RMSE from the commandline to calculate the relative RMSE.
    Equation used: RELRMSE = (RMSE*(n**(1/2)))/((sum (angle**2))**(1/2))

    Return: relrmse      --- The relative RMSE

    05.05.2021  Original   By: VAB
    """

    # The column names contained in the .csv file
    col1 = ['code', 'angle']

    # Read the .csv files from the commandline and convert it into a dataframe
    if sys.argv[1] != '':
        data = pd.read_csv(sys.argv[1], usecols=col1)

    # Take the rmse from the second commandline input and convert it into a float
    rmse = float(sys.argv[2])

    # Count the number of angles in the dataframe
    n = data['angle'].count()

    # Take the square root of the number of angles
    rn = float(n)**(1/2)

    # Makes a list of all the angles squared
    sq_angle = []
    for angle in data['angle']:
        angle_2 = float(angle)**2
        sq_angle.append(angle_2)

    col2 = ['sqangle']

    # Create a dataframe of all angles squared
    df = pd.DataFrame(data=sq_angle, columns=col2)

    # Take the sum of all the square angles
    c_sangles = df['sqangle'].sum()

    # Take the sqroot of summed square angles
    rc_sangles = float(c_sangles)**(1/2)

    relrmse = (rmse*rn)/rc_sangles
    return relrmse


# *************************************************************************
result = calc_relemse()
print(result)