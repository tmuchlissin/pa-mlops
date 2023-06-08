import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

st.set_option('deprecation.showPyplotGlobalUse', False)

# st.balloons()

st.title(""" Data Export Import Indonesia""")

st.info(""" 

Politeknik Elektronika Negeri Surabaya

Nama Kelompok :
1. Moch Toriqul Muchlisin (3321600001)
2. Rifda Quratul 'Ain (3321600012)
3. Muhammad Dzalhaqi (3321600023)

Jurusan :   
Sains Data Terapan 

Kelas / Angkatan :        
2 / 2021
""")


st.write("""
Data ini diambil dari https://www.bps.go.id/exim/""")

url_data = 'https://raw.githubusercontent.com/Dzalhaqi/pa-mlops/main/dataset/bulanan-ekspor-impor.csv'

data_bulanan_ei = None
month = None

with st.sidebar:
  st.subheader("Filter Controls Configuration")
  month = ["All", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
           "Agustus", "September", "Oktober", "November", "Desember"]
  year = [i for i in range(2019, 2024)]

  show_filter = st.radio("Filter Dataframe", ("No", "Yes"), index=0)

  if show_filter == "Yes":
    col1, col2 = st.columns(2)

    with col1:
      choosen_month = st.selectbox("Select month", month)

    with col2:
      choosen_year = st.selectbox("Select year", year)

    if choosen_month == "All":
      data_bulanan_ei = pd.read_csv(f"{url_data}")
      data_bulanan_ei["Bulan-Tahun"] = pd.to_datetime(
          data_bulanan_ei["Bulan-Tahun"])
      data_bulanan_ei = data_bulanan_ei[data_bulanan_ei["Bulan-Tahun"].dt.year == choosen_year]
      data_bulanan_ei["Bulan-Tahun"] = data_bulanan_ei["Bulan-Tahun"].dt.date

    else:
      data_bulanan_ei = pd.read_csv(f"{url_data}")
      data_bulanan_ei["Bulan-Tahun"] = pd.to_datetime(
          data_bulanan_ei["Bulan-Tahun"])
      data_bulanan_ei = data_bulanan_ei[data_bulanan_ei["Bulan-Tahun"].dt.year == choosen_year]
      data_bulanan_ei = data_bulanan_ei[data_bulanan_ei["Bulan-Tahun"].dt.month ==
                                        month.index(choosen_month)]
      data_bulanan_ei["Bulan-Tahun"] = data_bulanan_ei["Bulan-Tahun"].dt.date

  else:
    data_bulanan_ei = pd.read_csv(f"{url_data}")
    data_bulanan_ei["Bulan-Tahun"] = pd.to_datetime(
        data_bulanan_ei["Bulan-Tahun"])
    data_bulanan_ei["Bulan-Tahun"] = data_bulanan_ei["Bulan-Tahun"].dt.date

# Show dataframe
st.subheader("Data Bulanan Ekspor Impor Indonesia")

st.dataframe(data_bulanan_ei)

# showing plot 
if show_filter == "Yes":
  year_data = data_bulanan_ei[data_bulanan_ei["Bulan-Tahun"].apply(lambda x: x.year) == choosen_year]

  surplus_data = year_data[year_data["Neraca Perdagangan"] > 0]
  defisit_data = year_data[year_data["Neraca Perdagangan"] < 0]

fig = go.Figure()

fig.add_trace(go.Bar(
    # x=defisit_data['Bulan-Tahun'].dt.month,
    x=defisit_data['Bulan-Tahun'].apply(lambda x: x.month),
    y=defisit_data['Neraca Perdagangan'],
    name='Defisit',
    marker_color='yellow'
))

if len(surplus_data) > 0:
    fig.add_trace(go.Bar(
        # x=surplus_data['Bulan-Tahun'].dt.month,
        x=surplus_data['Bulan-Tahun'].apply(lambda x: x.month),
        y=surplus_data['Neraca Perdagangan'],
        name='Surplus',
        marker_color='darkgreen'
    ))

# Customize the layout
fig.update_layout(
    title='Bar Plot Neraca Perdagangan 2020',
    xaxis_title='Bulan',
    yaxis_title='Nilai Neraca Perdagangan',
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    )
)

# Show the plot
# pio.show(fig)

st.plotly_chart(fig)
