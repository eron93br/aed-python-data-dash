# import pandas as pd




# df_desp = pd.read_csv('./dash_app/files/Ano-2020.csv', sep=';')



# df_desp = df_desp[df_desp['vlrLiquido'] > 0]
# df_desp['mes_ano'] = df_desp.apply(lambda x: f"{x.numMes}-{x.numAno}", axis=1)
# df_desp_lider = df_desp[df_desp['cpf'].isna()]
# df_desp_dept = df_desp[~df_desp['cpf'].isna()]
# df_desp_lider['sgPartido'] = df_desp_lider['txNomeParlamentar'].str.replace(
#     'LIDERANÇA DO ', '')



# df = df_desp_dept[['vlrLiquido','txNomeParlamentar','txtDescricao']].groupby(['txNomeParlamentar','txtDescricao']).sum().rank(method='first')
# print(df.head(25))
import plotly.express as px
print(px.colors.diverging.balance_r)