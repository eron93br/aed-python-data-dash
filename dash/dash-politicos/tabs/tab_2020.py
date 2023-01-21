from dash import html
from dash import dcc
from charts.bar_char import Bar_char
import dash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

class Tab2020:

    def render_tab(self):
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 50, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])
