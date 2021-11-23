#!/usr/bin/env python3
"""
Program:    NR2
File:       NR2.py

Version:    V1.0
Date:       15.11.2021
Function:   Combine duplicate identical sequences with angles identical to 2dp.

Description:
============
The program will take take the output .csv file that contains encoded sequence and angles and if the sequence of
residues are the same and so is the angle (rounded to 2dp), it'll combined the two entries.

Commandline input: 1) encoded .csv file
                   2) .dat file with column names
                   3) outtput name for NR2_{}.csv
--------------------------------------------------------------------------
"""

# *************************************************************************
# Import libraries

import pandas as pd
import sys


# *************************************************************************
def nr():
    """Read the .csv file containing encoded residues and angles and combine lines that have the same PDB code and
    the same encoded sequence into one line, averaging the angle

    Return: seq_df      --- Dataframe that contains a single angle for all PDB files with unique sequences

    17.04.2021  Original   By: VAB
    """

    # The column names contained in the .csv file imported from a .dat file
    col1 = []
    for i in open(sys.argv[2]).readlines():
        i = i.strip('\n')
        col1.append(i)

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=col1)

    # angle needs to be converted to a float to be averaged
    res_file['angle'] = res_file['angle'].astype(float)

    # aggregation function specifies that when the rows are grouped, the first value of code will be kept and the 
    # angles will be averaged
    aggregation_func = {'code': 'first', 'angle': 'mean'}

    # make a column of rounded values for angle 
    res_file['ang2dp']=res_file['angle'].round(decimals=2)
  
    # remove 'angle' and 'code' from columns header list, since program is not grouping by these, but add the rounded
    # angle column
    col1.remove('angle')
    col1.remove('code')
    col1.append('ang2dp')

    # group by values now in col1 (residue identities and rounded angle to 2dp)
    seq_df = res_file.groupby(col1).aggregate(aggregation_func)

    # grouping produces a "sup" column that is over the columns that were grouped by. This resets all column names
    # to the same level
    seq_df = seq_df.reset_index()
 
    # to get back our original column order
    cols=seq_df.columns.tolist()
    cols = [cols[-2]]+ cols[:-3] + cols[-1:]
    seq_df=seq_df[cols]

    return seq_df


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

results = nr()

results.to_csv('NR2_{}.csv'.format(sys.argv[3]), index=False)
