from msilib import Table, sequence
import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
import os
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.layouts import row, column
from bokeh.models import Button,ColumnDataSource, Div, Select, Slider, TextInput, TableColumn, DataTable


rootdir = "C:/Users/sanjeevs/PycharmProjects/pythonProject/verification/csv"
appended_data = pd.DataFrame()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if str(file)=='summary.csv':
            #print(os.path.join(subdir, file))
            #print(str(subdir+"\\"+file))
            data = pd.read_csv(str(subdir+"\\"+file), sep=',', header=0)
            #print(data.head())
            appended_data = pd.concat((appended_data, data), axis=0)

# count the number of enhancer peaks
#groupedDataFrame = appended_data.groupby('chromosome')

# get minimum and maximum sequence start value in grouped dataframe
min_sequence_start = appended_data['sequence_start'].min()
max_sequence_start = appended_data['sequence_start'].max()

# get minimum and maximum sequence stop value in grouped dataframe
min_sequence_stop = appended_data['sequence_stop'].min()
max_sequence_stop = appended_data['sequence_stop'].max()

# minimum and maximum sequence length
min_sequence_length = appended_data['sequence_length'].min()
max_sequence_length = appended_data['sequence_length'].max()

# min and max number of variants
min_num_variants = appended_data['num_variants'].min()
max_num_variants = appended_data['num_variants'].max()

# min and max num nucleotides accessible 
min_num_nucleotides = appended_data['num_nucleotides_accessible'].min()
max_num_nucleotides = appended_data['num_nucleotides_accessible'].max()

# min and max num nucleotides accessible 
min_num_nucleotides_highlighted = appended_data['num_nucleotides_highlighted'].min()
max_num_nucleotides_highlighted = appended_data['num_nucleotides_highlighted'].max()

chromosome_list = ["2R","2L","3R","3L","X", "All"]

# Create Input controls
chromosome_name = Select(title="Chromosome Name", value="All", options=chromosome_list)
sequence_start_slider = Slider(title="Minimum Sequence Start value", value=min_sequence_start, start=min_sequence_start, end=max_sequence_start, step=5)
sequence_stop_slider = Slider(title="Minimum Sequence Stop value", value=min_sequence_stop, start=min_sequence_stop, end=max_sequence_stop, step=5)
sequence_length_slider = Slider(title="Minimum Sequence Length", start=min_sequence_length, end=max_sequence_length, value=min_sequence_length, step=1)
num_variants_slider = Slider(title="Minimum Number of Variants", value=min_num_variants, start=min_num_variants, end=max_num_variants, step=1)
num_nucleotides_slider = Slider(title="Minimum Number of Nucleotides Accessible", value=min_num_nucleotides, start=min_num_nucleotides, end=max_num_nucleotides, step=1)
num_highlight_nucleotides_slider =  Slider(title="Minimum Number of Nucleotides Highlighted", value=min_num_nucleotides_highlighted, start=min_num_nucleotides_highlighted, end=max_num_nucleotides_highlighted, step=1)

def select_chromosomes():
    chromosome_name_val = chromosome_name.value
    selected = appended_data[
        (appended_data.sequence_start >= sequence_start_slider.value) &
        (appended_data.sequence_stop >= (sequence_stop_slider.value)) &
        (appended_data.sequence_length >= sequence_length_slider.value) &
        (appended_data.num_variants >= num_variants_slider.value) &
        (appended_data.num_nucleotides_accessible >= num_nucleotides_slider.value) &
        (appended_data.num_nucleotides_highlighted >= num_highlight_nucleotides_slider.value)
    ]
    if (chromosome_name_val != "All"):
        selected = selected[selected.chromosome.str.contains(chromosome_name_val)]
    return selected

src = ColumnDataSource(appended_data)

def update():
    current = select_chromosomes()
    src.data = {
        'report_file_path': current.report_file_path,
        'chromosome': current.chromosome,
        'sequence_start': current.sequence_start,
        'sequence_stop': current.sequence_stop,
        'sequence_length': current.sequence_length,
        'num_variants': current.num_variants,
        'num_accessible_variants': current.num_accessible_variants,
        'num_nucleotides_accessible': current.num_nucleotides_accessible,
        'pi_scores_mean': current.pi_scores_mean,
        'pi_scores_stdev': current.pi_scores_stdev,
        'genotype_mean_missing': current.genotype_mean_missing,
        'genotype_stdev_missing': current.genotype_stdev_missing,
        'num_nucleotides_N': current.num_nucleotides_N,
        'num_nucleotides_highlighted': current.num_nucleotides_highlighted,
        'JASPAR_unique_motifs': current.JASPAR_unique_motifs,
        'num_JASPAR_nucleotide_coverage': current.num_JASPAR_nucleotide_coverage,
        'STREME_unique_motifs': current.STREME_unique_motifs,
        'num_STREME_nucleotide_coverage': current.num_STREME_nucleotide_coverage
    }


controls = [chromosome_name, sequence_start_slider, sequence_stop_slider, sequence_length_slider, num_variants_slider,num_nucleotides_slider,num_highlight_nucleotides_slider]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

columns = appended_data.columns
columns_table = []
for i in range(len(columns)):
    columns_table.append(TableColumn(field=columns[i]))

data_table = DataTable(source=src, columns=columns_table, autosize_mode='fit_columns', sizing_mode='stretch_both', width=800, height=1000)

layout = row(column(chromosome_name,sequence_start_slider, sequence_stop_slider,sequence_length_slider,num_variants_slider,
num_nucleotides_slider,num_highlight_nucleotides_slider),data_table)

curdoc().add_root(layout)

# director = TextInput(title="Director name contains")
# cast = TextInput(title="Cast names contains")
# x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Tomato Meter")
# y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Number of Reviews")

