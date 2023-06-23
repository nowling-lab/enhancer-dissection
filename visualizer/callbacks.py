# Add controls to build the interaction
@callback(
    Output(component_id='column-graph-summary', component_property='figure'),
    Input(component_id='column-radios-summary', component_property='value')
)
def update_graph(col_chosen):
    if summary_df[col_chosen].nunique() == 1:
        fig = px.histogram(summary_df, x=col_chosen, title=f'Histogram of: {col_chosen}', nbins=1, range_x=[0,0])
    else:
        fig = px.histogram(summary_df, x=col_chosen, title=f'Histogram of: {col_chosen}')
    return fig