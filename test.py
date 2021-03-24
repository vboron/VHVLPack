import os
import sys

item = sys.argv[1]
def find_filepath(item):
    list = []
    for file in os.listdir(item):
        list.append(os.path.abspath(file))
    print(list)
    return
get_files = find_filepath(item)
#print(get_files)