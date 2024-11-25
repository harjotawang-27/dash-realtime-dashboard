#import data 
import pandas as pd 
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load data
df = pd.read_csv('https://cloud-object-storage-cos-standard-mpx.s3.jp-tok.cloud-object-storage.appdomain.cloud/TB_Burden_Country.csv')

# Group and normalize data
df_group = df.groupby(['Year', 'Country or territory name'])['Estimated prevalence of TB (all forms) per 100 000 population'].sum().reset_index()
df_pivot = df_group.pivot_table(index='Year', columns='Country or territory name', values='Estimated prevalence of TB (all forms) per 100 000 population', fill_value=0).reset_index()

# Normalize data
df_normalized = df_pivot.copy()
for country in df_pivot.columns[1:]:
    df_normalized[country] = (df_pivot[country] - df_pivot[country].min()) / (df_pivot[country].max() - df_pivot[country].min())

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1(
        'Tuberculosis Burden by Country',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': '3vw',
            'font-weight': 'bold',
            'text-shadow': '3px 3px 5px rgba(0,0,0,0.1)',
            'padding': '20px',
            'border-bottom': '2px solid #007BFF',
            'letter-spacing': '1px'
        }
    ),
    html.Div([
        "Country: ",
        dcc.Dropdown(
            id='input-country',
            options=[{'label': country, 'value': country} for country in df_pivot.columns[1:]],
            value=[],
            multi=True,
            style={
                'font-size': '16px',
                'padding': '10px',
                'border-radius': '8px',
                'border': '2px solid #007BFF',
                'box-shadow': '0px 4px 10px rgba(0,0,0,0.1)'
            }
        )
    ]),
    html.Br(),
    html.Div(dcc.Graph(id='scatter-chart'))
])

# Callback
@app.callback(
    Output(component_id='scatter-chart', component_property='figure'),
    Input(component_id='input-country', component_property='value')
)
def update_graph(selected_countries):
    if not selected_countries:
        return px.scatter(title='No countries selected')

    # Filter data for selected countries
    filtered_data = df_normalized[['Year'] + selected_countries]
    melted_data = filtered_data.melt(id_vars='Year', var_name='Country', value_name='Normalized Prevalence')

    # Create scatter plot
    fig = px.scatter(
        melted_data, 
        x='Year', 
        y='Normalized Prevalence', 
        color='Country', 
        title='Normalized TB Prevalence for Selected Countries',
        labels={"Normalized Prevalence": "Normalized TB Prevalence", "Year": "Year"},
        opacity=0.7
    )
    fig.update_layout(xaxis_title='Year', yaxis_title='Normalized Prevalence')
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
