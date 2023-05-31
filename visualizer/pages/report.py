import dash
from dash import html
import glob

dash.register_page(__name__)

def layout(report_id=None):
    return html.Div([
    html.Iframe(src=f'assets/{report_id.upper()}.html',
                style={"height": "100vh",
                        "width": "100%",
                        'overflow':'hidden'})  
    ],
    style={
        "overflow":"hidden"
    },
    id='highlights')