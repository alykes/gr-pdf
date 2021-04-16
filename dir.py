import os
import re

path = "./pdfs"

files = os.listdir(path)

for f in files:
    int_position = []
    array = re.split(r'-|\.', f)
    for idx, items in enumerate(array):
         try :
             if int(array[idx]):
                int_position.append(idx)
         except ValueError:
             continue

    print(array[idx - 1][0:4] + "-" + array[idx - 1][4:6] + "-" + array[idx -1][6:8])
