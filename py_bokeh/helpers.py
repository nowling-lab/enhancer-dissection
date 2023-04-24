import numpy as np
import pandas as pd
import os
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HTMLTemplateFormatter, CheckboxGroup, RangeSlider, Div, TabPanel, Tabs
from functools import partial
from enum import Enum

class View(Enum):
    SUMMARY = 1
    COUNT = 2
    COVERAGE = 3
    VARIANT = 4
    LABEL = 5
    RANGE = 6

# State variables
df_reference: pd.DataFrame = None
first_render = False
filters = []
table: DataTable = None
filters:dict = None
defualt_filters = {}


class Webpage:
    def __init__(self, abs_path:str) -> None:
        self.summary = None
        self.count = None
        self.coverage = None
        self.variant = None
        self.abs_path = abs_path
        data_tables = {
            View.SUMMARY: None,
            View.COUNT: None,
            View.COVERAGE: None,
            View.VARIANT: None,
        }
    
    def generate_base_ui(self):
        summary_tab, table = self.get_summary_tab(self.summary, self.abs_path)
        count_tab = self.get_counts_tab(self.count)
        coverage_tab = self.get_coverage_tab(self.coverage)
        variant_tab = self.get_variant_tab(self.variant)
        distribution_tab = self.get_visualizations(self.summary, self.count, self.coverage, self.variant)

        return Tabs(tabs=[summary_tab, count_tab, coverage_tab, variant_tab, distribution_tab])

    def read_csv(self, abs_path: str, file_id: str, tab: View) -> pd.DataFrame:
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

        match tab:
            case View.SUMMARY:
                self.summary = combined_df
                self.summary.set_index(['report_file_path'])
            case View.COUNT:
                self.count = combined_df
            case View.COVERAGE:
                self.coverage = combined_df
            case View.VARIANT:
                self.variant = combined_df
    
    def create_table(self, data:pd.DataFrame, abs_path:str=None):
        # read in files
        # if abs_path != None:
            # data['report_file_path'] = data.apply(lambda row: f'file:///{abs_path}/{row[0]}', axis=1)
            # data['report_file_path'] = data.apply(lambda row: f'https://www.google.com/', axis=1)
            # data['report_file_path'] = data.apply(lambda row: f'<a href="file:///{abs_path}/{row[0]}">Report Link</a>', axis=1)

        source = ColumnDataSource(data)
        columns = []
        for index, header in enumerate(data.columns):
            # if index == 0:
            #     columns.append(TableColumn(field=header, title=header, width=len(header), formatter= HTMLTemplateFormatter(template='<a href="<%= report_file_path %>">Report Link</a>')))
            # else:
            columns.append(TableColumn(field=header, title=header, width=1))

        data_table = DataTable(source=source, columns=columns, width=2000, index_position=None)
        data_table.styles = {
            'height': '100vh',
            'width':'62vw',
            'margin': '0px',
            "padding-bottom": "50px",
        }
        
        global table
        table = data_table

        return data_table

    def labels_callback(self, attr, old, new):
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

    def range_callback(self, attr, old, new, type, range_or_label):
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

    def filter_callback(self, attr, old, new):
        global df_reference
        global filters
        global table

        # if tab == View.SUMMARY:
        #     if range_or_label == View.RANGE:
        #         self.range_callback(attr, old, new, type)
        #     else:
        #         self.labels_callback(attr, old, new)
        # elif tab == View.COUNT:
        #     if range_or_label == View.RANGE:
        #         ...
        #     else:
        #         ...
        # elif tab == View.COVERAGE:
        #     if range_or_label == View.RANGE:
        #         ...
        #     else:
        #         ...
        # elif tab == View.VARIANT:
        #     if range_or_label == View.RANGE:
        #         ...
        #     else:
        #         ...

    def get_inputs(self, col_selection, elements):
        header = Div(text="Filters", 
                    styles={'font-weight': 'bold',
                            'margin': 'auto',
                            'font-size': 'large'})

        inputs = column(header, 
                        col_selection,
                        *elements,
                        sizing_mode="stretch_height")
            
        inputs.styles = {
            "height": "100vh",
            "overflow-y": "scroll",
            "overflow-x": "hidden",
            "padding-right": "10px",
            "padding-left": "10px",
            "padding-bottom": "50px",
            "width": "18vw"
        }
        return inputs

    def get_summary_tab(self, data, abs_path):
        labels = list(data.columns)
        default_active = [*list(range(0,len(labels)))]
        col_selection = CheckboxGroup(labels=labels, active=default_active)
        # col_selection.on_change("active", partial(self.filter_callback, page=View.SUMMARY))
        col_selection.on_change("active", self.filter_callback)

        elements = []
        invalid_cols = {'report_file_path', 'chromosome'}
        for col in data.columns:
            if col in invalid_cols:
                continue
            start = data[col].min()
            end = data[col].max()
            if start == end:
                continue
            defualt_filters[col] = (start, end)
            range_slider = RangeSlider(start=start, end=end, value=(start,end), step=1, title=col)
            range_slider.on_change("value", partial(self.range_callback, type=col, range_or_label=View.RANGE))
            # range_slider.on_change("value", self.filter_callback)

            elements.append(range_slider)
                
        data_table = self.create_table(data, abs_path)

        inputs = self.get_inputs(col_selection, elements)

        ui = row(inputs, data_table, sizing_mode="stretch_height")
        ui.styles = {
            'width': '100%',
            'margin': '0px'
        }

        return TabPanel(child=ui, title="Summary"), data_table

    def get_counts_tab(self, count):
        header = Div(text="Filters", 
                    styles={'font-weight': 'bold',
                            'margin': 'auto',
                            'font-size': 'large'})
        
        ui = row(header, sizing_mode="stretch_height")
        return TabPanel(child=ui, title="Count")

    def get_coverage_tab(self, coverage):
        header = Div(text="Filters", 
                    styles={'font-weight': 'bold',
                            'margin': 'auto',
                            'font-size': 'large'})
        
        ui = row(header, sizing_mode="stretch_height")
        return TabPanel(child=ui, title="Coverage")

    def get_variant_tab(self, variant):
        header = Div(text="Filters", 
                    styles={'font-weight': 'bold',
                            'margin': 'auto',
                            'font-size': 'large'})
        
        ui = row(header, sizing_mode="stretch_height")
        return TabPanel(child=ui, title="Variant")

    def get_visualizations(self, summary, count, coverage, variant):
        header = Div(text="Filters", 
                    styles={'font-weight': 'bold',
                            'margin': 'auto',
                            'font-size': 'large'})
        
        ui = row(header, sizing_mode="stretch_height")
        return TabPanel(child=ui, title="Distributions")
    