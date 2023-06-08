import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

from pyFTS.benchmarks import Measures
from pyFTS.partitioners import Grid
from pyFTS.models import chen

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
choosen_year = None


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


with st.sidebar:
  indicator = st.selectbox("Indicator", data_bulanan_ei.columns[1:], index=0)
  n_part = st.slider("Partitions", 1, 20, 10)

tab_eda, tab_model = st.tabs(["EDA", "Model"])

with tab_eda:
  # Show dataframe
  st.subheader("EDA Bulanan Ekspor Impor Indonesia")

  st.dataframe(data_bulanan_ei)

  # showing plot 
  if show_filter == "Yes":
    year_data = data_bulanan_ei[data_bulanan_ei["Bulan-Tahun"].apply(lambda x: x.year) == choosen_year]

    surplus_data = year_data[year_data["Neraca Perdagangan"] > 0]
    defisit_data = year_data[year_data["Neraca Perdagangan"] < 0]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=defisit_data['Bulan-Tahun'].apply(lambda x: x.month),
        y=defisit_data['Neraca Perdagangan'],
        name='Defisit',
        marker_color='yellow',
        hovertemplate=
        '<b>Tahun %s</b><br>' % choosen_year +
        '<i>Nilai Neraca Perdagangan</i>: $%{y:.2f} <br>' +
        '<i>Bulan</i>: ' + defisit_data['Bulan-Tahun'].apply(lambda x: x.strftime('%B')) + '<br>'
    ))

    if len(surplus_data) > 0:
        fig.add_trace(go.Bar(
            x=surplus_data['Bulan-Tahun'].apply(lambda x: x.month),
            y=surplus_data['Neraca Perdagangan'],
            name='Surplus',
            marker_color='darkgreen',
            hovertemplate=
            '<b>Tahun %s</b><br>' % choosen_year +
            '<i>Nilai Neraca Perdagangan</i>: $%{y:.2f} <br>' +
            '<i>Bulan</i>: ' + surplus_data['Bulan-Tahun'].apply(lambda x: x.strftime('%B')) + '<br>'
        ))

    # Customize the layout
    fig.update_layout(
        title=f"Bar Plot {indicator} {choosen_year}",
        xaxis_title='Bulan',
        yaxis_title='Nilai Neraca Perdagangan',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
        )
    )

    st.plotly_chart(fig)

  else:
    # show all surplus and defisit data in every year
    surplus_data = data_bulanan_ei[data_bulanan_ei["Neraca Perdagangan"] > 0]
    defisit_data = data_bulanan_ei[data_bulanan_ei["Neraca Perdagangan"] < 0]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=defisit_data['Bulan-Tahun'].apply(lambda x: x.year),
        y=defisit_data['Neraca Perdagangan'],
        name='Defisit',
        marker_color='yellow',
        hovertemplate=
        '<b>Tahun %{x}</b><br>' +
        '<i>Nilai Neraca Perdagangan</i>: $%{y:.2f} <br>' +
        '<i>Bulan</i>: ' + defisit_data['Bulan-Tahun'].apply(lambda x: x.strftime('%B')) + '<br>'
    ))

    if len(surplus_data) > 0:
        fig.add_trace(go.Bar(
            x=surplus_data['Bulan-Tahun'].apply(lambda x: x.year),
            y=surplus_data['Neraca Perdagangan'],
            name='Surplus',
            marker_color='darkgreen',
            hovertemplate=
            '<b>Tahun %{x}</b><br>' +
            '<i>Nilai Neraca Perdagangan</i>: $%{y:.2f} <br>' +
            '<i>Bulan</i>: ' + defisit_data['Bulan-Tahun'].apply(lambda x: x.strftime('%B')) + '<br>'
        ))


    # Customize the layout
    fig.update_layout(
        title=f"Bar Plot {indicator} {year[0]} - {year[-1]}",
        xaxis_title='Tahun',
        yaxis_title='Nilai Neraca Perdagangan',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(2019, 2024)),
            ticktext=['2019', '2020', '2021', '2022', '2023']
        )
    )

    st.plotly_chart(fig)

with tab_model:

  st.subheader("Pemodelan Data Bulanan Ekspor Impor Indonesia")

  predict_tab, forecast_tab = st.tabs(["Prediksi", "Peramalan"])

  with predict_tab:


    bulan_tahun = data_bulanan_ei['Bulan-Tahun'].values
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=bulan_tahun,
        y=data_bulanan_ei[indicator],
        name=f"{indicator}",
        marker_color='blue',
        hovertemplate=
        '<b>Tahun %{x}</b><br>' +
        '<i>Nilai Ekspor</i>: $%{y:.2f} <br>' +
        '<i>Bulan</i>: ' + data_bulanan_ei['Bulan-Tahun'].apply(lambda x: x.strftime('%B')) + '<br>'
    ))

    # Customize the layout
    fig.update_layout(
        title=f"Line Plot {indicator} Bulanan Indonesia",
        xaxis_title='Tahun',  
        yaxis_title=f"{indicator}",
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(2019, 2024)),
            ticktext=['2019', '2020', '2021', '2022', '2023']
        )
    )

    st.plotly_chart(fig)

    fs = Grid.GridPartitioner(data=data_bulanan_ei[indicator], npart=n_part)

    fig = go.Figure()

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[25, 10])

    ax.set_xlim(0, len(data_bulanan_ei))
    ax.set_ylim(-0.1, 0.1)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    fs.plot(ax)
    ax.set_title(f"Fuzzy Set {indicator}", fontsize=30)

    st.pyplot(fig)

    model = chen.ConventionalFTS(partitioner=fs)
    model.fit(data_bulanan_ei[indicator].values)
    st.code(model)

    prediction = model.predict(data_bulanan_ei[indicator].values)

    data_fts_result = pd.DataFrame({
      'date': bulan_tahun,
      'actual': data_bulanan_ei[indicator],
      'prediction': prediction
    })

    # Plot the data using Plotly
    fig = go.Figure()

    # Add actual data
    fig.add_trace(go.Scatter(
        x=data_fts_result['date'], y=data_fts_result['actual'], mode='lines', name='Actual'))

    # Add forecast data
    fig.add_trace(go.Scatter(
        x=data_fts_result['date'], y=data_fts_result['prediction'], mode='lines', name='Forecast'))

    # Set layout
    fig.update_layout(
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12),
            tickformat='%Y-%m-%d'
        ),
        yaxis=dict(
            title_font=dict(size=20),
            tickfont=dict(size=20)
        ),
        legend=dict(
            x=1,
            y=0,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    )

    # Add vertical lines with alternating styles
    for i in range(len(bulan_tahun)):
        if i % 2 == 0:
            fig.add_shape(type='line', x0=bulan_tahun[i], y0=0, x1=bulan_tahun[i], y1=1, line=dict(
                color='black', width=1, dash='solid'))
        else:
            fig.add_shape(type='line', x0=bulan_tahun[i], y0=0, x1=bulan_tahun[i], y1=1, line=dict(
                color='black', width=1, dash='dash'))

    st.plotly_chart(fig)

  with forecast_tab:
    forecasting = model.forecast(data_bulanan_ei[indicator].values, steps=10)
    start_month_year = data_bulanan_ei['Bulan-Tahun'].iloc[-1]
    forecasting_dates = pd.date_range(
        start=f"{start_month_year}", periods=20, freq='M').strftime('%Y-%m-%d').tolist()

    forecast_data = dict(zip(forecasting_dates, forecasting))

    # show the line chart with plotly
    fig = go.Figure()

    # forecast data
    fig.add_trace(go.Scatter(
        x=forecasting_dates, y=forecasting, mode='lines', name='Forecasting'))

    # set layout
    fig.update_layout(
        title=f"Forecasting {indicator.title()} of Indonesia",
        yaxis_title="Percentage",
        legend_title="Indicator",
        yaxis=dict(
            title='Percentage',
            title_font=dict(size=12),
            tickfont=dict(size=12)
        ),
        legend=dict(
            x=1,
            y=0,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    )

    # remove x label
    fig.update_xaxes(title=None)

    # show hover template
    fig.update_traces(hovertemplate="Indonesia" +
                      "Year: %{x}<br>" +
                      "Percentage: %{y}<br>%" +
                      "<extra></extra>")

    st.plotly_chart(fig)

  # Performance model
  st.subheader("Performance Model")

  # Calculate RMSE using Measeure class
  rmse = Measures.rmse(data_fts_result['actual'], data_fts_result['prediction'])
  mape = Measures.mape(data_fts_result['actual'], data_fts_result['prediction'])

  st.code(f"""
  RMSE: {rmse} 
  MAPE: {mape}""")



