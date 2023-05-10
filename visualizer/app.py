from dash import Dash, html, dash_table, dcc, callback, Output, Input
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import dash 
import shutil
from utils import *
import os 
import argparse
import glob
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

parser = argparse.ArgumentParser()
parser.add_argument('--data', help="The folder that genome_highlighter created when ran", required=True)
parser.add_argument('--del', help='Deletes the html files in the assets folder before copying new html files to it', action='store_true')
args = parser.parse_args()

summary_df, counts_df, coverage_df, variant_df = load_files(args)
inputs = [(summary_df, 'summary'), (counts_df, 'counts'), (coverage_df, 'coverage'), (variant_df, 'variant')]

app = Dash(__name__, use_pages=True)

for (df, title) in inputs:
    if title != "summary":
        continue

    df['report_file_path'] = df['report_file_path'].apply(
        lambda x: f'[Report]({x.split("/")[-1].split(".")[0].lower()})'
    )

for input in inputs:
    df: pd.DataFrame = input[0]
    title = input[1]
    path = f'/{title}'
    
    if title == 'summary':
        path = '/'

    dash.register_page(title,  path=path, layout=html.Div([
        html.Div(
        [dash_table.DataTable(
            columns=[
                {'id': x, 'name': x, 'presentation': 'markdown'} if x == 'report_file_path' else {'id': x, 'name': x} for x in df.columns
            ],
            data=df.to_dict('records'),
            filter_action="native",
            sort_action="native",
            page_action="native",
            page_current= 0,
            page_size= 20,
            style_table={'overflowX': 'auto'},
            cell_selectable = False,
            id='interactive-table'
        )],
        id='table-wrapper'),
        html.H4("Histograms"),
        html.Div([
            dcc.RadioItems(options=df.columns, value=df.columns[0], id=f'column-radios'),
            dcc.Graph(figure={}, id=f'column-graph')
        ],
        id="buttons-chart-row", 
        **{'data-page': title})
        ])
    )

# Callback for the filtering of the table
@callback(
    Output(component_id='interactive-table', component_property='data'),
    Input(component_id='column-graph', component_property='clickData'),
    Input(component_id='buttons-chart-row', component_property='data-page'),
    Input('interactive-table', "page_current"),
    Input('interactive-table', "page_size")
)
def update_graph(click_data, page, page_current, page_size):
    df: pd.DataFrame = None
    match page:
        case 'summary':
            df = summary_df
        case 'counts':
            df = counts_df
        case 'coverage':
            df = coverage_df
        case 'variant':
            df = variant_df

    if click_data == None:
        return df.to_dict('records')

    # Click_data is a dict with points in it, which is an array that only has one element, which has a dict with pointNumbers in it...
    # which refers to the different indices in the table aka the dataframe the chart is made out of...
    points_in_clicked_bucket = click_data['points'][0]['pointNumbers'] 

    column_data = df.iloc[points_in_clicked_bucket] 

    return column_data.to_dict('records')

# Changing the graph based on selected radio button
@callback(
    Output(component_id='column-graph', component_property='figure'),
    Input(component_id='column-radios', component_property='value'),
    Input(component_id='buttons-chart-row', component_property='data-page'),
)
def update_graph(col_chosen, page):
    df: pd.DataFrame = None

    match page:
        case 'summary':
            df = summary_df
        case 'counts':
            df = counts_df
        case 'coverage':
            df = coverage_df
        case 'variant':
            df = variant_df

    if col_chosen not in df.columns:
        col_chosen = df.columns[0]

    if df[col_chosen].nunique() == 1:
        fig = px.histogram(df, x=col_chosen, title=f'Histogram of: {col_chosen}', nbins=1, range_x=[0,0])
    else:
        fig = px.histogram(df, x=col_chosen, title=f'Histogram of: {col_chosen}')
    return fig

for html_file in glob.glob('./assets/*.html'):
    file_name = Path(html_file).stem
    dash.register_page(file_name, layout= html.Div([
    html.Iframe(src=html_file[2:],
                style={"height": "100vh",
                        "width": "100%",
                        'overflow':'hidden'})  
    ],
    style={
        "overflow":"hidden"
    },
    id='highlights'))

pages_to_list = [html.Div("Pages:")]
for page in dash.page_registry.values():
    if '-' not in page['name']:
        pages_to_list.append(html.Div(dcc.Link(f"{page['name']}", href=page["relative_path"])) )

app.layout = html.Div([
    html.Div(
        pages_to_list,
        className='nav-bar'
    ),
    html.Br(),
    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=True)