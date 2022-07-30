import streamlit as st
import numpy as np
import pandas as pd

st.title('Streamlit start!')
df = pd.DataFrame(
    np.random.rand(20,4),
    columns=['a','b','c','d']
    )
st.table(df.style.highlight_max(axis=0))

if st.button('Show grph?'):
    st.line_chart(df)
