import sys
import os
import shutil


# *************************************************************************
def get_old():
    """Read the directory name from the commandline argument

    Return: pdb_direct      --- Directory of PBD files that will be processed for VH-VL packing angles

    15.03.2021  Original   By: VAB
    """

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        old_direct = sys.argv[1]
    return old_direct


# *************************************************************************
def get_new():
    """Read the directory name from the commandline argument

    Return: pdb_direct      --- Directory of PBD files that will be processed for VH-VL packing angles

    15.03.2021  Original   By: VAB
    """

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[2] != '':
        new_direct = sys.argv[2]
    return new_direct


# *************************************************************************
def find_files(od, nd):

    o_files = []
    cwd = os.getcwd()
    new_directory = 'original_pdbs'
    path = os.path.join(cwd, new_directory)
    #print(path)
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
    for file in os.listdir(od):
        o_files.append(file[:4])
        o_files = [x.upper() for x in o_files]
        for item in o_files:
            for pdb in os.listdir(nd):
                if item in str(pdb):
                    shutil.copy(os.path.join(sys.argv[2], '{}'.format(pdb)), path)

    return


# *************************************************************************
old = get_old()

new = get_new()

final = find_files(old, new)
