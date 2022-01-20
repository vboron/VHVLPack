import argsparser
import pandas as pd
import os

def extract_xval_stats(columns, directory):
    col = []
    for i in open(columns).readlines():
        i = i.strip('\n')
        col.append(i)

    all_data = []
    files = []

    # Open the directory and make a list of .log files that are in there
    for file in os.listdir(directory):
        if file.endswith("_test.log"):
            files.append(os.path.join(directory, file))

    # Open each log file in the directory and find the relevant information
    for log_file in files:
        with open(log_file) as text_file:
            for line in text_file:


    # Make .csv files for all of the data, splitting it into files that have all the data, only outliers, and only the
    # data withing the 'norm'
    df_a = pd.DataFrame(data=all_data, columns=col)
    path = os.path.join(direct, f'{csv_out}.csv')
    df_a.to_csv(path, index=False)