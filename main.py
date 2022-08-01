#from time import strftime
#
#from sqlalchemy import true
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import yfinance as yf

pd.options.display.precision = 0

st.title('yfinance by Streamlit')
st.subheader('現在のダイコク電機の株価')
dk = yf.Ticker('6430.T')
dkpd = dk.history(period='2d')
delta = dkpd.iloc[1, 3] - dkpd.iloc[0, 3]
value = dkpd.iloc[1, 3]
st.metric(label='株価', value=f'{value}円', delta=f'{delta}円')

st.sidebar.write("""
# 表示設定
下記オプションから、日数指定を可能です。
""")
st.sidebar.write("""
## 表示日数設定
""")

days =st.sidebar.slider('日数を指定戒能です。',1,90,30)
st.write(f"""
### **各社の{days}日間** の株価データ
""")

st.sidebar.write("""
## 株価グラフの範囲指定
""")
ymin,ymax = st.sidebar.slider(
    '範囲を指定可能です。',
    0, 30000, (500, 4500)
)

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        #divdf = pd.DataFrame(
        #    tkr.dividends
        #)
        #divdf.iloc[::-1]
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

tickers = {
    'Nikkei225' : '^N225',
    'Daikoku' : '6430.T',
    'SegasammyHD' : '6460.T',
    'MarsHD' : '6419.T',
    'Glory' : '6457.T',
    'Heiwa' : '6412.T',
    'Sankyo' : '6417.T',
    'FujiShoji' : '6257.T',
    'Univarsal' : '6425.T',
    'Ohizumi' : '6428.T',
    'Fields' : '2767.T',
    'Axell' : '6730.T'
}

df = get_data(days, tickers)

companies = st.multiselect(
    '会社をリストから指定できます。',
    list(df.index),
    ['Daikoku']
)
data = df.loc[companies]
#deta_revece = data.columns[::-1]
#deta_revece.columns[::-1]
#st.write("## 株価", data)
st.dataframe(data.style.highlight_max(axis=1))

data = data.T.reset_index()
data = pd.melt(data,id_vars=['Date']).rename(
    columns={'value':'Prices(JPN)'}
)
chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Prices(JPN):Q", stack=None, scale=alt.Scale(domain=[ymin,ymax])),
        color='Name:N'
    )
)

st.altair_chart(chart, use_container_width=True)

#if st.button('Show graph?'):
#    st.line_chart(df.T)
