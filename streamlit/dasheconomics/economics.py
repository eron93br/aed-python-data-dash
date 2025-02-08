import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import datetime 
from bcb import currency, Expectativas, sgs, TaxaJuros
from utils import TICKERS
import yfinance as yf

START_DATE = '2014-01-02'
END_DATE = '2025-01-31'
currencies = ["CHF", "USD"]

def get_ipca(start_date=START_DATE, end_date=END_DATE):
    em = Expectativas()
    ep = em.get_endpoint('ExpectativasMercadoAnuais')
    collected_ipca = (ep.query()
            .filter(ep.Indicador == 'IPCA')
            .filter(ep.Data >= start_date)
            .filter(ep.Data <= end_date)
            .orderby(ep.Data.desc())
            .collect())
    ipca_data = pd.DataFrame(collected_ipca)
    ipca_data['DataYear'] = ipca_data['Data'].dt.year
    ipca_data['DataReferenciaYear'] = ipca_data['DataReferencia'].astype(int)
    ipca_data = ipca_data[ipca_data['DataYear'] == ipca_data['DataReferenciaYear']]
    ipca_data.drop(['DataYear', 'DataReferenciaYear'], axis=1, inplace=True)
    ipca_data = ipca_data[ipca_data['baseCalculo'] == 0]
    ipca_data.drop(['Indicador', 'IndicadorDetalhe', 'Mediana', 'Maximo', 'DesvioPadrao', 'DataReferencia', 'numeroRespondentes', 'baseCalculo'], axis=1, inplace=True)
    ipca_data.columns = ['IPCA_' + col for col in ipca_data.columns]
    ipca_data.set_index('IPCA_Data', inplace=True)
    return ipca_data

def get_selic(start_date=START_DATE, end_date=END_DATE):
    em = TaxaJuros()
    # Busca a série da SELIC no SGS
    selic = sgs.get({'selic':432}, start = start_date, end = end_date)
    selic.index = pd.to_datetime(selic.index, format='%d-%m-%Y')
    return selic, selic['selic'].iloc[-1], selic['selic'].iloc[-366]

def get_moedas(currencies, start_date=START_DATE, end_date=END_DATE):
    return currency.get(currencies, start=start_date, end=end_date)

def get_stocks(start_date=START_DATE, end_date=END_DATE):
    tickerData = yf.download(TICKERS, period='1d', start=start_date, end=end_date)
    stock_df = tickerData['Close']
    return stock_df