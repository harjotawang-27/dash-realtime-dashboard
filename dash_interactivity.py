import pandas as pd 
import plotly.graph_objects 
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

airlane_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                           encoding='ISO-8859-1',
                           dtype={'Div1Airport':str, 'Div1TailNum':str,
                                  'Div2Airport':str, 'Div2TaiNum':str})
