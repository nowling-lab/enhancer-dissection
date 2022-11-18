from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.models import Button
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, gridplot, output_file
import pandas as pd
from bokeh.sampledata.iris import flowers 

def get_table(abs_path:str, data:pd.DataFrame, filters:dict):
    # read in files

    source = ColumnDataSource(data)

    columns = []
    for header in data.columns:
        columns.append(TableColumn(field=header, title=header, width=len(header)))

    data_table = DataTable(source=source, columns=columns, width=2000, index_position=None, autosize_mode='fit_columns', sizing_mode='stretch_both')

    return data_table