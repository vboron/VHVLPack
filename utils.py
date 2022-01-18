import os
import subprocess

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

def run_cmd(cmd_list, is_dry_run: bool, stdout=None, env=None):
    log_msg = f"Running {cmd_list}"
    if env is not None:
        log_msg += f'; env={env}'
        env.update(os.environ.copy())
    print(log_msg)
    if not is_dry_run:
        subprocess.run(cmd_list, stdout=stdout, env=env)