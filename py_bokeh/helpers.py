import numpy as np
import pandas as pd
import os
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HTMLTemplateFormatter, CheckboxGroup, RangeSlider, Div
from functools import partial

# State variables
df_reference: pd.DataFrame = None
first_render = False
filters = []
table: DataTable = None
filters:dict = None
defualt_filters = {}

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

def get_table(data:pd.DataFrame, abs_path:str=None):
    # read in files
    if abs_path != None:
        data['report_file_path'] = data.apply(lambda row: f'file:///{abs_path}/{row[0]}', axis=1)
        #data['report_file_path'] = data.apply(lambda row: f'https://www.google.com/', axis=1)
    #data['report_file_path'] = data.apply(lambda row: f'<a href="file:///{abs_path}/{row[0]}">Report Link</a>', axis=1)

    source = ColumnDataSource(data)

    columns = []
    for index, header in enumerate(data.columns):
        if index == 0:
            columns.append(TableColumn(field=header, title=header, width=len(header), formatter= HTMLTemplateFormatter(template='<a href="<%= report_file_path %>">Report Link</a>')))
        else:
            columns.append(TableColumn(field=header, title=header, width=len(header)))

    data_table = DataTable(source=source, columns=columns, width=2000, index_position=None, autosize_mode='fit_columns', sizing_mode='stretch_both')
    
    global table
    table = data_table
    return data_table

def labels_callback(attr, old, new):
    global table
    global df_reference

    new_cols = []
    for index, header in enumerate(df_reference.columns):
        if index in new:
            if index == 0:
                new_cols.append(TableColumn(field=header, title=header, width=len(header), formatter= HTMLTemplateFormatter(template='<a href="<%= report_file_path %>">Report LInk</a>')))
            else:
                new_cols.append(TableColumn(field=header, title=header, width=len(header)))
    table.columns = new_cols

def range_callback(attr, old, new, type):
    global df_reference
    global filters
    filters[type] = new

    filtered_df:pd.DataFrame = df_reference[(df_reference[type] >= new[0]) & (df_reference[type] <= new[1])] 
    for filter in filters:
        if filter == type:
            continue

        start, end = filters[filter]
        defualt_start, default_end = defualt_filters[filter]
        if start == defualt_start and end == default_end:
            continue

        filtered_df = filtered_df[(filtered_df[filter] >= start) & (filtered_df[filter] <= end)] 

    filtered_df.set_index(['report_file_path'])

    new_source = ColumnDataSource(filtered_df)

    table.source.data = dict(new_source.data)

def generate_dynamic_ui(data:pd.DataFrame, abs_path:str):
    global filters
    global df_reference
    global defualt_filters
    df_reference = data
    filters = {}

    labels = list(data.columns)
    default_active = [*list(range(0,len(labels)))]
    col_selection = CheckboxGroup(labels=labels, active=default_active)
    col_selection.on_change("active", labels_callback)

    elements = []
    invalid_cols = {'report_file_path', 'chromosome'}
    for col in data.columns:
        if col in invalid_cols:
            continue
        start = data[col].min()
        end = data[col].max()
        defualt_filters[col] = (start, end)
        range_slider = RangeSlider(start=start, end=end, value=(start,end), step=1, title=col)
        range_slider.on_change("value", partial(range_callback, type=col))
        elements.append(range_slider)
            
    table = get_table(data, abs_path)
    inputs = column(Div(text="Columns:", style={'font-weight': 'bold'}),col_selection, *elements, sizing_mode="stretch_height")
    ui = row(inputs, table, sizing_mode="stretch_height")
    return ui

