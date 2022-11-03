import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal')
])

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8055)