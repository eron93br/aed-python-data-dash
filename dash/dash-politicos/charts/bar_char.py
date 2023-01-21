from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

class Bar_char:

    df_desp_dept = pd.DataFrame()
    VALOR_MILHAO=1000000

    def __top10(self,value):
        df_sum_legenda = self.df_desp_dept[['sgPartido','vlrLiquido']].groupby(['sgPartido']).sum().sort_values('vlrLiquido',ascending=False)
        df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']/self.VALOR_MILHAO

        if value == 't10':
            return df_sum_legenda[:10]

        return df_sum_legenda

    @app.callback(
        Output('example-graph', 'figure'),
        [Input('demo-dropdown', 'value')])
    def update_output(self, value):
        df_sum_legenda = self.__top10(value)
        fig = px.bar(df_sum_legenda, x=df_sum_legenda.index, y="vlrLiquido", color=df_sum_legenda.index, barmode="overlay", )
        fig.update_traces(customdata=[x for  x in df_sum_legenda.index])
        return fig
