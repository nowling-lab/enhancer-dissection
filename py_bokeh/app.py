from bokeh.settings import settings
from bokeh.models import Button
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn, GlobalInlineStyleSheet
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, gridplot, output_file
from bokeh.themes import Theme
import pandas as pd
from bokeh.sampledata.iris import flowers 
from helpers import *
import sys

settings.log_level = "trace"
abs_path = os.path.abspath(sys.argv[1])
ui = Webpage(abs_path)

ui.read_csv(abs_path, 'summary', View.SUMMARY)
ui.read_csv(abs_path, 'counts', View.COUNT)
ui.read_csv(abs_path, 'coverage', View.COVERAGE)
ui.read_csv(abs_path, 'variant_data', View.VARIANT)

curdoc().add_root(ui.generate_base_ui())