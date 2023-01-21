import dash
from dash.html.Figcaption import Figcaption
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask.scaffold import F
import geopandas as gpd
import json
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px

######## constante #######
VALOR_MILHAO = 1000000

STYLES = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df_desp = pd.DataFrame()
df_desp_dept = pd.DataFrame()

df_desp_20 = pd.read_csv('./files/Ano-2020.csv', sep=';')
df_desp_19 = pd.read_csv('./files/Ano-2019.csv', sep=';')
df_pos = pd.read_csv('./files/posicao-partidos.csv', sep=';')
df_cota = pd.read_csv('./files/cota_por_estado.csv', sep=';')
brasil_map = gpd.read_file('./files/brasil.geojson')

brasil_map['center'] = brasil_map['geometry'].apply(lambda x: x.centroid)

# df_desp = df_desp[df_desp['vlrLiquido'] > 0]
# df_desp['mes_ano'] = df_desp.apply(lambda x: f"{x.numMes}-{x.numAno}", axis=1)
# df_desp_lider = df_desp[df_desp['cpf'].isna()]
# df_desp_dept = df_desp[~df_desp['cpf'].isna()]
# df_desp_lider['sgPartido'] = df_desp_lider['txNomeParlamentar'].str.replace(
#     'LIDERANÇA DO ', '')

########

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Raio-x Deputados Brasil'),
    dcc.Tabs(id="tabs-59", value='tab-2019', children=[
        dcc.Tab(label='Ano 2019', id='2019', value='tab-2019'),
        dcc.Tab(label='Ano 2020', id='2020', value='tab-2020'),
    ]),
    html.Div(id='tabs-content-graph-ranking',
             style={'background-color': '#f8f8ff'})
], style={'background-color': '#f8f8ff'})


@app.callback(Output('tabs-content-graph-ranking', 'children'),
              Input('tabs-59', 'value'))
def render_content(tab):
    get_df_desp(tab)
    if tab == 'tab-2019':
        return html.Div(style={'margin': '50px', 'background-color': '#f8f8ff'}, children=[
            html.H3(f'Ano {tab.replace("tab-","")}'),
            dbc.Col([
                dbc.Card([
                    dbc.Col([
                        html.Div(
                            children=f'Despesas por Legenda - {tab.replace("tab-","")}', style={'margin': '10px'}),
                        dcc.Dropdown(
                            id='dropdown-ranking',
                            options=[{"label": "Valor Líquido Acumulado por partido", "value": "vlrLiquido"},
                                     {"label": "Valor Médio por deputado", "value": "valor_medio"}],
                            value='valor_medio',
                            multi=False,
                            style={'margin': '30px'}
                        )
                    ], width=4),
                    dcc.Graph(
                        id='graph-ranking',
                        clickData={'points': [{'customdata': 'all'}]}
                    )
                ])
            ], ),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H3(id='h3-cota',
                                style={'margin': '10px'}),
                        html.Div(style={'margin': '10px'}, children=[
                            dcc.Dropdown(
                                id='dropdown-tipo-map',
                                options=[{"label": "Valor Líquido médio por estado", "value": "des_percapt"},
                                         {"label": "Valor da Cota por estado",
                                          "value": "VALOR"},
                                         {"label": "Valor Liquido Acumulado por estado",
                                          "value": "vlrLiquido"},
                                         {"label": "Quantidade de Deputados por estado", "value": "txNomeParlamentar"}],
                                value='vlrLiquido'
                            ),
                            dcc.Graph(
                                id='map-sum-partido')
                        ])
                    ])
                ], width=6),
                dbc.Col(
                    dbc.Card([
                        html.Div([
                            dbc.Row([
                                html.H3(f"Tipos de Despesas",id='h3-tipo',
                                        style={'margin': '10px'}),
                                dbc.Col(
                                    html.Div(
                                        dcc.Graph(
                                            id='treemap_classificacao',
                                        )
                                    ),
                                )
                            ])
                        ])
                    ]),
                    width=6)
            ]),
            dbc.Card([
                html.Div([
                    dbc.Row([
                            html.H3(f"Histórico de Gastos",
                                    style={'margin': '10px'}),
                            dbc.Col(
                                html.Div(
                                    dcc.Dropdown(
                                        id='dropdown-candidato',
                                        multi=True,
                                        options=get_options_candidato(),
                                        value=[get_options_candidato()[
                                            0]['value']]
                                    )
                                ), width=6)
                            ]),
                    html.Div(
                        dcc.Graph(
                            id='comparativo-candidato',
                        )
                    )
                ])
            ]),
            dbc.Card([
                html.Div([
                    html.H3("Visão Geral"),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id='dropdown-bubble',
                                multi=False,
                                options=[{"label": "Tamanho pela quantidade de deputados", "value": "txNomeParlamentar"},
                                         {"label": "Tamanho pelo Valor Liquido", "value": "vlrLiquido"}],
                                value='txNomeParlamentar'
                            ),
                            width=6),
                    ]),
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                dcc.Graph(
                                    id='bublle-candidato',)
                            ),
                        )
                    ])
                ])
            ]),
            dbc.Card([
                html.H3("Cota Por Legenda"),
                html.Div(
                    dcc.Graph(
                        id='pie-resumo',
                        figure=get_pie()))
            ])
        ])
    elif tab == 'tab-2020':
        return html.Div(style={'margin': '50px', 'background-color': '#f8f8ff'}, children=[
            html.H3(f'Ano {tab.replace("tab-","")}'),
            dbc.Col([
                dbc.Card([
                    dbc.Col([
                        html.Div(
                            children=f'Despesas por Legenda - {tab.replace("tab-","")}', style={'margin': '10px'}),
                        dcc.Dropdown(
                            id='dropdown-ranking',
                            options=[{"label": "Valor Líquido Acumulado por partido", "value": "vlrLiquido"},
                                     {"label": "Valor Médio por deputado", "value": "valor_medio"}],
                            value='valor_medio',
                            multi=False,
                            style={'margin': '30px'}
                        )
                    ], width=4),
                    dcc.Graph(
                        id='graph-ranking',
                        clickData={'points': [{'customdata': 'all'}]}
                    )
                ])
            ], ),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H3(id='h3-cota',
                                style={'margin': '10px'}),
                        html.Div(style={'margin': '10px'}, children=[
                            dcc.Dropdown(
                                id='dropdown-tipo-map',
                                options=[{"label": "Valor Líquido médio por estado", "value": "des_percapt"},
                                         {"label": "Valor da Cota por estado",
                                          "value": "VALOR"},
                                         {"label": "Valor Liquido Acumulado por estado",
                                          "value": "vlrLiquido"},
                                         {"label": "Quantidade de Deputados por estado", "value": "txNomeParlamentar"}],
                                value='vlrLiquido'
                            ),
                            dcc.Graph(
                                id='map-sum-partido')
                        ])
                    ])
                ], width=6),
                dbc.Col(
                    dbc.Card([
                        html.Div([
                            dbc.Row([
                                html.H3(f"Tipos de Despesas",id='h3-tipo',
                                        style={'margin': '10px'}),
                                dbc.Col(
                                    html.Div(
                                        dcc.Graph(
                                            id='treemap_classificacao',
                                        )
                                    ),
                                )
                            ])
                        ])
                    ]),
                    width=6)
            ]),
            dbc.Card([
                html.Div([
                    dbc.Row([
                            html.H3(f"Histórico de Gastos",
                                    style={'margin': '10px'}),
                            dbc.Col(
                                html.Div(
                                    dcc.Dropdown(
                                        id='dropdown-candidato',
                                        multi=True,
                                        options=get_options_candidato(),
                                        value=[get_options_candidato()[
                                            0]['value']]
                                    )
                                ), width=6)
                            ]),
                    html.Div(
                        dcc.Graph(
                            id='comparativo-candidato',
                        )
                    )
                ])
            ]),
            dbc.Card([
                html.Div([
                    html.H3("Visão Geral"),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id='dropdown-bubble',
                                multi=False,
                                options=[{"label": "Tamanho pela quantidade de deputados", "value": "txNomeParlamentar"},
                                         {"label": "Tamanho pelo Valor Liquido", "value": "vlrLiquido"}],
                                value='txNomeParlamentar'
                            ),
                            width=6),
                    ]),
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                dcc.Graph(
                                    id='bublle-candidato',)
                            ),
                        )
                    ])
                ])
            ]),
            dbc.Card([
                html.H3("Cota Por Legenda"),
                html.Div(
                    dcc.Graph(
                        id='pie-resumo',
                        figure=get_pie()))
            ])
        ])

###### charts ###########

def get_df_desp(ano):
    global df_desp_dept
    df_desp_dept = pd.DataFrame()

    if ano.replace("tab-","") == "2020":
        df_desp = df_desp_20
    elif ano.replace("tab-","") == "2019":
        df_desp = df_desp_19

    df_desp = df_desp[df_desp['codLegislatura']==56]
    df_desp = df_desp[df_desp['vlrLiquido'] > 0]
    df_desp['mes_ano'] = df_desp.apply(lambda x: f"{x.numMes}-{x.numAno}", axis=1)
    df_desp_dept = df_desp[~df_desp['cpf'].isna()]


def pie():
    df_dept_pie = df_desp_dept[[
        'sgPartido', 'sgUF', 'vlrLiquido', 'txNomeParlamentar']]
    df_dept_pie = df_dept_pie.groupby(['sgPartido', 'sgUF', 'txNomeParlamentar'],).agg(
        {'vlrLiquido': np.sum}).reset_index()

    df_dept_pie['vlrLiquido'] = df_dept_pie['vlrLiquido']

    df_pos.nome = df_pos.nome.str.lower()
    df_dept_pie.sgPartido = df_dept_pie.sgPartido.str.lower()

    df_dept_pie = df_dept_pie.merge(
        df_pos, left_on='sgPartido', right_on='nome')

    df_dept_pie.sort_values('classificacao', inplace=True)
    df_dept_pie = df_dept_pie.reset_index()

    return df_dept_pie


def bubble():
    df_dept_scatter = df_desp_dept[[
        'sgPartido', 'vlrLiquido', 'txNomeParlamentar']]
    df_dept_scatter = df_dept_scatter.groupby(['sgPartido'],).agg(
        {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).reset_index()
    df_dept_scatter['vlrLiquido'] = df_dept_scatter['vlrLiquido']

    df_pos.nome = df_pos.nome.str.lower()
    df_dept_scatter.sgPartido = df_dept_scatter.sgPartido.str.lower()

    df_dept_scatter = df_dept_scatter.merge(
        df_pos, left_on='sgPartido', right_on='nome')

    df_dept_scatter.sort_values('classificacao', inplace=True)

    return df_dept_scatter


def comparativo(cand):
    df_compatativo = df_desp_dept[df_desp_dept['txNomeParlamentar'].isin(
        cand)]
    df_compatativo = df_compatativo[['txNomeParlamentar', 'mes_ano', 'vlrLiquido', 'numMes']].groupby(
        ['txNomeParlamentar', 'mes_ano', 'numMes']).sum().sort_index(
        level=['numMes', 'txNomeParlamentar', ]).reset_index().rename(columns={
            'vlrLiquido': 'total'})
    df_compatativo.drop('numMes', inplace=True, axis=1)
    df_compatativo['total'] = df_compatativo['total']/1000
    return df_compatativo


def ranking_partidos():
    df_sum_legenda = df_desp_dept[['sgPartido', 'vlrLiquido', 'txNomeParlamentar']].groupby(
        ['sgPartido']).agg(
        {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).reset_index()

    df_sum_legenda['valor_medio'] = df_sum_legenda['vlrLiquido'] / \
        df_sum_legenda['txNomeParlamentar']

    df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']

    df_pos.nome = df_pos.nome.str.lower()
    df_sum_legenda.sgPartido = df_sum_legenda.sgPartido.str.lower()

    df_sum_legenda = df_sum_legenda.merge(
    df_pos, left_on='sgPartido', right_on='nome')


    print(df_sum_legenda.head())
    return df_sum_legenda


def get_chart_map(sgPartido):
    df_desp_dept_vl_map = df_desp_dept
    if sgPartido:
        if sgPartido=='SDD':
            sgPartido='SOLIDARIEDADE'
        df_desp_dept_vl_map = df_desp_dept[df_desp_dept['sgPartido'] == sgPartido]

    df_cota[['UF', 'VALOR']].groupby(['UF']).sum().sort_values(
        ['VALOR'], ascending=False).reset_index().rename(columns={'VALOR': 'total_cota'})

    df_desp_dept_vl_map = df_desp_dept_vl_map[['sgUF', 'vlrLiquido', 'txNomeParlamentar']].groupby(
        ['sgUF']).agg(
        {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).sort_values(['vlrLiquido'],
                                                                                    ascending=False).reset_index()
    df_desp_dept_vl_map['des_percapt'] = (
        df_desp_dept_vl_map['vlrLiquido']/df_desp_dept_vl_map['txNomeParlamentar'])/12

    df_desp_dept_vl_map['vlrLiquido'] = df_desp_dept_vl_map['vlrLiquido']

    merged = brasil_map.set_index('UF_05').join(
        df_desp_dept_vl_map.set_index('sgUF'))

    merged = merged.merge(
        df_cota, left_on=merged.index, right_on='UF')
    merged = merged.set_index('UF')
    merged.vlrLiquido = merged.vlrLiquido.fillna(0)
    merged.txNomeParlamentar = merged.txNomeParlamentar.fillna(0)
    merged.VALOR = merged.VALOR.fillna(0)
    merged.des_percapt = merged.des_percapt.fillna(0)

    return merged


def get_options_candidato():
    return [{"label": f"{x['txNomeParlamentar']} - {x['sgUF']} - {x['sgPartido']} ", "value": x['txNomeParlamentar']} for _, x in df_desp_dept[['txNomeParlamentar', 'sgPartido', 'sgUF']].drop_duplicates().iterrows()]


def df_treemap(click_event):

    df_sum_legenda = df_desp_dept
    if click_event:
        if click_event=='SDD':
            click_event='SOLIDARIEDADE'
        df_sum_legenda = df_desp_dept[df_desp_dept['sgPartido'] == click_event ]
    
    df_sum_legenda = df_sum_legenda[['sgPartido', 'txtDescricao', 'vlrLiquido']].groupby(
        ['sgPartido', 'txtDescricao']).sum().sort_values('vlrLiquido', ascending=False).reset_index()
    df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']
    return df_sum_legenda

########## CALLBACKS ###############

@app.callback(
    Output('treemap_classificacao', 'figure'),
    [Input('graph-ranking', 'clickData')])
def get_treemap(click_event):
    df = df_treemap(click_event.get('points')[0].get('label'))

    list_color = []
    for cor in px.colors.qualitative.Pastel1:
        list_color.append(cor)
    for cor in px.colors.qualitative.Pastel2:
        list_color.append(cor)

    fig = px.treemap(df, values="vlrLiquido", path=[px.Constant(" "),
                                                    "txtDescricao"], maxdepth=2, color_discrete_sequence=list_color)

    fig.update_layout(
        margin=dict(
            l=5,
            r=0,
            b=0,
            t=0,)
    )

    return fig


def get_pie():
    df_pie = pie()

    dict_cores = pd.Series(df_pie.cores.values, index=df_pie.partido).to_dict()
    dict_cores['(?)'] = '#FFFF'

    fig = px.sunburst(df_pie, path=[px.Constant(" "), 'partido', 'sgUF', 'txNomeParlamentar'],
                      values='vlrLiquido', color='partido',  maxdepth=2, color_discrete_map=dict_cores)

    return fig


@app.callback(
    Output('bublle-candidato', 'figure'),
    [Input('dropdown-bubble', 'value')])
def update_bubble(type_chart):
    df_bubble = bubble()
    y_title = 'Valor - R$'
    y_axis = 'vlrLiquido'
    if type_chart == 'vlrLiquido':
        y_title = 'Quantidade'
        y_axis = 'txNomeParlamentar'

    fig = px.scatter(df_bubble, x='partido', color_discrete_sequence=df_bubble.cores.tolist(), y=y_axis, size=type_chart, color='partido',
                     hover_name='partido',)

    fig.update_layout(yaxis_title=y_title,
                      xaxis_title="Partido",
                      legend_title='Partido',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')

    return fig


@app.callback(
    Output('comparativo-candidato', 'figure'),
    [Input('dropdown-candidato', 'value')])
def update_comparativo(cand):
    df_comparativo = comparativo(cand)
    fig = px.line(df_comparativo, x="mes_ano",
                  y="total", color='txNomeParlamentar', line_shape='spline')
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    fig.update_traces(mode="markers+lines")
    fig.update_layout(yaxis_title="Valor - R$",
                      xaxis_title="Mês",
                      legend_title='Parlamentar',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')

    return fig


@app.callback(
    Output('graph-ranking', 'figure'),
    [Input('dropdown-ranking', 'value')])
def update_output(value):
    df_sum_legenda = ranking_partidos()
    df_sum_legenda.sort_values(value, ascending=False, inplace=True)

    fig = px.bar(df_sum_legenda,
                 x=df_sum_legenda.partido,
                 y=value,
                 color=df_sum_legenda.partido, barmode="overlay",
                 color_discrete_sequence=df_sum_legenda.cores.tolist(),)

    fig.update_layout(yaxis_title="Valor - R$",
                      xaxis_title="Partido",
                      legend_title='Partido',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')
# layout = Layout(
#     paper_bgcolor='rgba(0,0,0,0)',
#     yaxis_color='rgba(0,0,0,0)'
# )

    return fig


@app.callback(
    Output('map-sum-partido', 'figure'),
    [Input('graph-ranking', 'clickData'),
     Input('dropdown-tipo-map', 'value')])
def update_map_output(value, tipo_mapa):
    merged = get_chart_map(value.get('points')[0].get('label'))

    fig_map = px.choropleth_mapbox(merged, geojson=merged.geometry, mapbox_style="carto-positron",
                                   locations=merged.index, color=tipo_mapa, color_continuous_scale=px.colors.sequential.Agsunset_r, zoom=2.3, center={"lat": -15.3889, "lon": -52.882778},)
    fig_map.update_layout(
        margin=dict(
            l=5,
            r=50,
            pad=4), coloraxis_colorbar_title="Valor - R$")

    return fig_map

@app.callback(
    Output('h3-cota', 'children'),
    [Input('graph-ranking', 'clickData')])
def update_map_output(value):
    return f"Cota Parlamenta - {value.get('points','Todos os Pardidos')[0].get('label','Todos os Pardidos')}"


@app.callback(
    Output('h3-tipo', 'children'),
    [Input('graph-ranking', 'clickData')])
def update_map_output(value):
    return f"Tipos de Despesas - {value.get('points','Todos os Pardidos')[0].get('label','Todos os Pardidos')}"


# f"Tipos de Despesas"

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080,debug=False,dev_tools_ui=False,dev_tools_props_check=False)

# debug=False,dev_tools_ui=False,dev_tools_props_check=False
# debug=True,
#                    use_reloader=True, dev_tools_hot_reload=True