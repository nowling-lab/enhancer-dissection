import pandas as pd
import os 
import glob
import shutil

def read_csv(abs_path: str, file_id: str) -> pd.DataFrame:
    dfs = []
    for subdir, dirs, files in os.walk(f'{abs_path}/csv'):
        for file in files:
            if file_id in file:
                print(f"Found {file_id} file: ",subdir, file)
                dfs.append(pd.read_csv(f'{subdir}/{file}', sep=',', header=0))

    combined_df = pd.DataFrame()
    for df in dfs:
        df = df.fillna(0)
        combined_df = pd.concat([combined_df, df], axis=0)

    return combined_df

def delete_old_files():
    num_deleted_files = 0
    for html_file in glob.glob(f'./assets/*.html'):
        num_deleted_files += 1
        os.remove(html_file)

    print(f'Deleted {num_deleted_files} files from {os.getcwd()}/assets')

def copy_new_files(abs_path):
    num_files = 0
    for html_file in glob.glob(f'{abs_path}/*/*.html'):
        num_files += 1
        shutil.copy(html_file, './assets')
    
    return num_files

def load_files(args):
    abs_path = os.path.abspath(args.data)

    if args.__getattribute__('del') == True:
        delete_old_files()

    num_files = copy_new_files(abs_path)

    print(f'Copied {num_files} files from {abs_path} to {os.getcwd()}/assets')

    summary_df = read_csv(abs_path, "summary")
    counts_df = read_csv(abs_path, "counts")
    coverage_df = read_csv(abs_path, "coverage")
    variant_df = read_csv(abs_path, "variant_data")

    return (summary_df, counts_df, coverage_df, variant_df)