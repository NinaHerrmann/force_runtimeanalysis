import os.path
from itertools import combinations
from osgeo import gdal
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
import sys

basepath = sys.argv[1]
settings = sys.argv[2:]
statsequal = pd.DataFrame(0, index=(settings), columns=(settings))
statsavgdiff = pd.DataFrame(0, index=(settings), columns=(settings))
for setting, setting2 in combinations(settings, 2):
    if setting == setting2:
        statsequal.loc[setting, setting2] = -1
        continue
    filecounter = 0
    diffsum = 0
    for folder_path in Path(f"{setting}/").glob("X00*_Y00*"):
        for jpg in Path(f"{folder_path}/").glob("*.jpg"):
            filename = jpg.name
            ds1 = gdal.Open(f'{setting}/{folder_path.name}/{filename}')
            if os.path.isfile(f'{setting2}/{folder_path.name}/{filename}'):
                filecounter += 1
                ds2 = gdal.Open(f'{setting2}/{folder_path.name}/{filename}')
                a = ds1.ReadAsArray()
                b = ds2.ReadAsArray()
                diff = np.abs(a.astype(int) - b.astype(int))
                diff_mask = diff.sum(axis=0) > 0 if diff.ndim == 3 else diff > 0
                Image.fromarray((diff_mask * 255).astype(np.uint8)).save('diff_mask.png')
                difference = diff.sum()
                if diff.sum() > 0:
                    count = np.count_nonzero(diff)
                    diffsum = count + diffsum
                    statsequal.loc[setting, setting2] = statsequal.loc[setting, setting2] + 1

                statsavgdiff.loc[setting, setting2] = diffsum / filecounter
                ds1 = None  # closes the dataset (GDAL's way of releasing the file handle)
                ds2 = None
    print(filecounter)
    if filecounter == 0:
       statsequal.loc[setting, setting2] = -1
       statsavgdiff.loc[setting, setting2] = -1
print(statsequal)
statsequal.to_csv(f'{basepath}/stats_diff.csv')
statsavgdiff.to_csv(f'{basepath}/stats_wo_coreg_23_diff.csv')
