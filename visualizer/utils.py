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

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3