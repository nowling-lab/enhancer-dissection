from bokeh.models import Button
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, gridplot, output_file
import pandas as pd
from bokeh.sampledata.iris import flowers 
from helpers import *
import sys

abs_path = os.path.abspath(sys.argv[1])

data = read_csv(abs_path)
data.set_index(['report_file_path'])
ui = generate_dynamic_ui(data, abs_path)

curdoc().add_root(ui)