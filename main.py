#from time import strftime
#
#from sqlalchemy import true
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import pandas_datareader.data as web
from datetime import datetime, timedelta

#pd.options.display.precision = 0

st.title('― 業界株価分析site -')
st.subheader('現在のダイコク電機の株価')
end = datetime.today()
start = end - timedelta(days=7)
dkpd = web.DataReader('6430.jp', 'stooq', start, end)
dkpd = dkpd.sort_index()
dkpd = dkpd.tail(2)

# エラーハンドリング：データが取得できたか
if dkpd.empty:
    st.error("株価データが取得できませんでした。ティッカー名や期間をご確認ください。")
else:
    dkpd = dkpd.astype('int64')
    dkpd.iloc[:, :5]
    delta = dkpd.iloc[-1, 3] - dkpd.iloc[-2, 3]
    value = dkpd.iloc[-1, 3]
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
## **各社の{days}日間** の株データ
### 株価　推移
""")

st.sidebar.write("""
## 株価グラフの範囲指定
""")
ymin,ymax = st.sidebar.slider(
    '範囲を指定可能です。',
    0, 30000, (500, 4500)
)

#@st.cache
def get_data(days, tickers, moji):
    df = pd.DataFrame()
    end = datetime.today()
    start = end - timedelta(days=days * 2)
    for company, symbol in tickers.items():
        if symbol.endswith('.T'):
            symbol = symbol.replace('.T', '.jp')
        hist = web.DataReader(symbol, 'stooq', start, end)
        hist = hist.sort_index().tail(days)
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[[moji]]
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

df = get_data(days, tickers,'Close')
companies = st.multiselect(
    '会社をリストから指定できます。',
    list(df.index),
    ['Daikoku']
)
data = df.loc[companies]
data = data.astype('int64')
data = data[data.columns[::-1]]
st.dataframe(data.style.highlight_max(axis=1))
data = data[data.columns[::-1]]

data = data.T.reset_index()
data = data.rename(columns={'index': 'Date'})
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

with st.expander("出来高　推移（(株)）"):
    df = get_data(days, tickers,'Volume')
    data = df.loc[companies]
    data = data[data.columns[::-1]]
    st.dataframe(data.style.highlight_max(axis=1))
#    data = data[data.columns[::-1]]

with st.expander("時価総額　推移 (百万円)"):
    # 発行株式をytのjsonから取得すると遅いので固定値
    shares = [0,
            14783000,
            220679008,
            16536400,
            58767900,
            98631504,
            54791000,
            22395500,
            77484000,
            22495300,
            32331700,
            10828400]
    df = get_data(days, tickers,'Close')
    #時価総額の計算
    for i, (index, listdata) in enumerate(df.iterrows()):
        #onelist = df.iloc[index]
        listdata = [n*shares[i]/1000000 for n in listdata ]
        df.loc[index] = listdata        
    
    data = df.loc[companies]
    data = data.astype('int64')
    data = data[data.columns[::-1]]
    st.dataframe(data.style.highlight_max(axis=1))
 #   data = data[data.columns[::-1]]

#if st.button('Show graph?'):
#    st.line_chart(df.T)
