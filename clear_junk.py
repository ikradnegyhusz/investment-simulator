import os
dirpath="chart_data"
files=os.listdir(dirpath)
for file in files:
    filepath=dirpath+"/"+file
    if os.path.getsize(filepath)<=43:
        os.remove(filepath)