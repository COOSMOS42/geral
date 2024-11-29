import random
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from gspread_pandas import Spread, Client
from gspread_dataframe import set_with_dataframe

# Definir escopos para Google Sheets e Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Carregar as credenciais de acesso do arquivo JSON
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes= scope)
# Autenticar com o Google Sheets (conectar as credencias)
client = Client(scope=scope, creds=creds)
spreadsheetname = "controlador"
spread = Spread(spreadsheetname, client = client)
#link com a planilha do google sheets
sheet = client.open(spreadsheetname).worksheet("resumo")

val = sheet.get_all_values()
# fr é a variavel da planilha do google sheets
fr = pd.DataFrame(val)
#separa a primeira linha da planilha google sheets
cab = fr.iloc[0]
#fazendo com que a planilha seja lida a partir da primeira linha
fr = fr[1:]
#seta as colunas
fr.columns = cab

def plot_gauge(
        indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=15, r=15, t=75, b=15, pad=12),
    )
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout='wide')

st.header("Resumo")
column_0 = st.columns(1)

column_1, column_2, column_3, column_4, column_5, column_6 = st.columns(6)

column_7, column_8, column_9, column_10, column_11, column_12 = st.columns(6)

val1 = fr["nentregas"].iloc[0] 
val1 = pd.to_numeric(val1, errors='coerce')

val2 = fr["nentregas"].iloc[1] 
val2 = pd.to_numeric(val2, errors='coerce')

val3 = fr["nentregas"].iloc[2] 
val3 = pd.to_numeric(val3, errors='coerce')

val4 = fr["nentregas"].iloc[3] 
val4 = pd.to_numeric(val4, errors='coerce')

val5 = fr["nentregas"].iloc[4] 
val5 = pd.to_numeric(val5, errors='coerce')

val6 = fr["nentregas"].iloc[5] 
val6 = pd.to_numeric(val6, errors='coerce')

val7 = fr["nentregas"].iloc[6] 
val7 = pd.to_numeric(val7, errors='coerce')

val8 = fr["nentregas"].iloc[7] 
val8 = pd.to_numeric(val8, errors='coerce')

val9 = fr["nentregas"].iloc[8] 
val9 = pd.to_numeric(val9, errors='coerce')

val10 = fr["nentregas"].iloc[9] 
val10 = pd.to_numeric(val10, errors='coerce')

val11 = fr["nentregas"].iloc[10] 
val11 = pd.to_numeric(val11, errors='coerce')

val12 = fr["nentregas"].iloc[11] 
val12 = pd.to_numeric(val12, errors='coerce')

sumval = sum([val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12])
total_max = 90
progresso = (total_entregas / total_max) * 100 if total_max > 0 else 0


with column_0:
    st.progress(int(progresso))
    st.write(f"Progresso atual: {progresso:.2f}%")
with column_1:
    plot_gauge(val1, "#78FF0F", "", "PARCELA 01", 8)

with column_2:
    plot_gauge(val2, "#78FF0F", "", "PARCELA 02", 8)

with column_3:
    plot_gauge(val3, "#78FF0F", "", "PARCELA 03", 8)

with column_4:
    plot_gauge(val4, "#78FF0F", "", "PARCELA 04", 8)

with column_5:
    plot_gauge(val5, "#78FF0F", "", "PARCELA 05", 8)

with column_6:
    plot_gauge(val6, "#78FF0F", "", "PARCELA 06", 8)

with column_7:
    plot_gauge(val7, "#78FF0F", "", "PARCELA 07", 8)

with column_8:
    plot_gauge(val8, "#78FF0F", "", "PARCELA 08", 8)

with column_9:
    plot_gauge(val9, "#78FF0F", "", "PARCELA 09", 8)

with column_10:
    plot_gauge(val10, "#78FF0F", "", "PARCECLA 10", 8)

with column_11:
    plot_gauge(val11, "#78FF0F", "", "PARCELA 11", 8)

with column_12:
    plot_gauge(val12, "#78FF0F", "", "PARCELA 12", 8)
