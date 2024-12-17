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
#sheet para os valores dos documentos aprovados
sheet2 = client.open(spreadsheetname).worksheet("aprovado")



val = sheet.get_all_values()
# fr é a variavel da planilha do google sheets
fr = pd.DataFrame(val)
#separa a primeira linha da planilha google sheets
cab = fr.iloc[0]
#fazendo com que a planilha seja lida a partir da primeira linha
fr = fr[1:]
#seta as colunas
fr.columns = cab

#dataframe dos documentos aprovados
val100 = sheet2.get_all_values()
# fr é a variavel da planilha do google sheets
fr1 = pd.DataFrame(val100)
#separa a primeira linha da planilha google sheets
cab1 = fr1.iloc[0]
#fazendo com que a planilha seja lida a partir da primeira linha
fr1 = fr1[1:]
#seta as colunas
fr1.columns = cab1

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



val13 = fr1["naprovados"].iloc[0] 
val13 = pd.to_numeric(val13, errors='coerce')

val14 = fr1["naprovados"].iloc[1] 
val14 = pd.to_numeric(val14, errors='coerce')

val15 = fr1["naprovados"].iloc[2] 
val15 = pd.to_numeric(val15, errors='coerce')

val16 = fr1["naprovados"].iloc[3] 
val16 = pd.to_numeric(val16, errors='coerce')

val17 = fr1["naprovados"].iloc[4] 
val17 = pd.to_numeric(val17, errors='coerce')

val18 = fr1["naprovados"].iloc[5] 
val18 = pd.to_numeric(val18, errors='coerce')

val19 = fr1["naprovados"].iloc[6] 
val19 = pd.to_numeric(val19, errors='coerce')

val20 = fr1["naprovados"].iloc[7] 
val20 = pd.to_numeric(val20, errors='coerce')

val21 = fr1["naprovados"].iloc[8] 
val21 = pd.to_numeric(val21, errors='coerce')

val22 = fr1["naprovados"].iloc[9] 
val22 = pd.to_numeric(val22, errors='coerce')

val23 = fr1["naprovados"].iloc[10] 
val23 = pd.to_numeric(val23, errors='coerce')

val24 = fr1["naprovados"].iloc[11] 
val24 = pd.to_numeric(val24, errors='coerce')




total_entregas = sum([val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12])
total_max = 90
progresso = (total_entregas / total_max) * 100 if total_max > 0 else 0

st.markdown("### Progresso do Trabalho")
st.progress(int(progresso)) 
st.write(f"Progresso atual: {progresso:.2f}%")


column_1, column_2, column_3, column_4, column_5, column_6 = st.columns(6)

column_7, column_8, column_9, column_10, column_11, column_12 = st.columns(6)

column_13, column_14, column_15, column_16, column_17, column_18 = st.columns(6)

column_19, column_20, column_21, column_22, column_23, column_24 = st.columns(6)

with column_1:
    plot_gauge(val1, "#1C83E1", "", "PARCELA 01", 8)

with column_2:
    plot_gauge(val2, "#1C83E1", "", "PARCELA 02", 8)

with column_3:
    plot_gauge(val3, "#1C83E1", "", "PARCELA 03", 8)

with column_4:
    plot_gauge(val4, "#1C83E1", "", "PARCELA 04", 8)

with column_5:
    plot_gauge(val5, "#1C83E1", "", "PARCELA 05", 8)

with column_6:
    plot_gauge(val6, "#1C83E1", "", "PARCELA 06", 8)

with column_7:
    plot_gauge(val7, "#1C83E1", "", "PARCELA 07", 8)

with column_8:
    plot_gauge(val8, "#1C83E1", "", "PARCELA 08", 8)

with column_9:
    plot_gauge(val9, "#1C83E1", "", "PARCELA 09", 8)

with column_10:
    plot_gauge(val10, "#1C83E1", "", "PARCECLA 10", 8)

with column_11:
    plot_gauge(val11, "#1C83E1", "", "PARCELA 11", 8)

with column_12:
    plot_gauge(val12, "#1C83E1", "", "PARCELA 12", 8)


with st.expander('Mostrar Aprovados'):
    with column_13:
        plot_gauge(val13, "#1C83E1", "", "PARCELA 1", 8)

    with column_14:
        plot_gauge(val14, "#1C83E1", "", "PARCELA 2", 8)

    with column_15:
        plot_gauge(val15, "#1C83E1", "", "PARCELA 3", 8)
    
    with column_16:
        plot_gauge(val16, "#1C83E1", "", "PARCELA 4", 8)

    with column_17:
        plot_gauge(val17, "#1C83E1", "", "PARCELA 5", 8)
    
    with column_18:
        plot_gauge(val18, "#1C83E1", "", "PARCELA 6", 8)

    with column_19:
        plot_gauge(val19, "#1C83E1", "", "PARCELA 7", 8)
    
    with column_20:
        plot_gauge(val20, "#1C83E1", "", "PARCELA 8", 8)

    with column_21:
        plot_gauge(val21, "#1C83E1", "", "PARCELA 9", 8)

    with column_22:
        plot_gauge(val22, "#1C83E1", "", "PARCELA 10", 8)

    with column_23:
        plot_gauge(val23, "#1C83E1", "", "PARCELA 11", 8)

    with column_24:
        plot_gauge(val24, "#1C83E1", "", "PARCELA 12", 8)
















