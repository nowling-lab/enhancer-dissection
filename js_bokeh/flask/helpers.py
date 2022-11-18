import numpy as np
import pandas as pd
import os

def read_csv(abs_path: str) -> pd.DataFrame:
    dfs = []
    for subdir, dirs, files in os.walk(f'{abs_path}/csv'):
        for file in files:
            if 'summary' in file:
                print("Found summary file: ",subdir, file)
                dfs.append(pd.read_csv(f'{subdir}/{file}', sep=',', header=0))

    combined_df = pd.DataFrame()
    for df in dfs:
        combined_df = pd.concat([combined_df, df], axis=0)

    return combined_df