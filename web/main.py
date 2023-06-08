import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

st.set_option('deprecation.showPyplotGlobalUse', False)

st.balloons()

st.title(""" Data Export Import Indonesia""")

st.info(""" 

Politeknik Elektronika Negeri Surabaya

Nama Kelompok :
1. Moch Toriqul Muchlisin (3321600001)
2. Rifda Quratul'Ain (3321600012)
3. Muhammad Dzalhaqi (3321600023)

Jurusan :   
Sains Data Terapan 

Kelas / Angkatan :        
2 / 2021
""")

st.write("Data ini diambil dari https://www.kaggle.com/")

data_bulanan_ei = pd.read_csv(
    "https://github.com/Dzalhaqi/pa-mlops/blob/main/bulanan-ekspor-impor.csv", sep=";")

st.subheader("Data Bulanan Ekspor Impor Indonesia")

st.dataframe(data_bulanan_ei)
