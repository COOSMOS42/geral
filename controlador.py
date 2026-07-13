import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread_pandas import Spread, Client
from gspread_dataframe import set_with_dataframe


st.set_page_config(page_title='Lançamentos', layout='wide')

# Definir escopos para Google Sheets e Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Carregar as credenciais de acesso do arquivo JSON
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)

# Autenticar com o gspread padrão (evita bugs de compatibilidade)
client = gspread.authorize(creds)


spreadsheetname = "trainee" 

try:
    sheet = client.open(spreadsheetname).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"Erro: A planilha '{spreadsheetname}' não foi encontrada. Certifique-se de que compartilhou ela com o e-mail da Conta de Serviço.")
    st.stop()

# Puxar dados existentes
val = sheet.get_all_values()
if val:
    fr = pd.DataFrame(val)
    cab = fr.iloc[0]
    fr = fr[1:]
    fr.columns = cab
else:
    fr = pd.DataFrame()

if 'jsoninput' not in st.session_state:
    st.session_state.jsoninput = pd.DataFrame(columns=['B', 'C', 'D', 'E', 'F', 'G', 'H'])

def adicionar_entrega(B, C, D, E, F, G, H):
    entrega = {
        'B': [str(B)],
        'C': [C],
        'D': [D],
        'E': [E],
        'F': [F],
        'G': [G],
        'H': [str(H)]
    }
    
    nova_linha = pd.DataFrame(entrega)
    st.session_state.jsoninput = pd.concat([st.session_state.jsoninput, nova_linha], ignore_index=True)
    return st.session_state.jsoninput

with st.form('Preencha os dados', clear_on_submit=False, border=True):
    st.subheader('Lançamento')
    b = st.date_input(label='Selecione uma data', format='DD/MM/YYYY')
    c = st.text_input('Descrição do lançamento')

    lista_cr = ['Suspensão e Dinâmica Veicular', 'Aerodinâmica', 'Drivetrain', 'Powertrain', 'Eletrônica e Controle', 'Estrutura', 'Freio', 'Gestão de Pessoas', 'Marketing', 'Comercial', 'Patrimônio']
    d = st.selectbox('Selecione o centro de responsabilidade', lista_cr)

    e = st.text_input('Valor referente ao lançamento')
    f = st.selectbox('Natureza', ("Faturamento", 'Custo'))
    g = st.selectbox('Status', ("Concluído", 'Pendente'))
    h = st.date_input(label='Selecione uma data de vencimento/entrega', format='DD/MM/YYYY')

    st.write('Salve as informações antes do envio')
    if st.form_submit_button('Salvar'):
        st.session_state.jsoninput = adicionar_entrega(b, c, d, e, f, g, h)
        st.success('Informações salvas localmente com sucesso!')

if st.button('Enviar dados 📨'):
    if not st.session_state.jsoninput.empty:
        # Pega a próxima linha vazia com base nas linhas preenchidas na planilha
        proxima_linha = len(sheet.col_values(1)) + 1
        
        set_with_dataframe(sheet,
                           st.session_state.jsoninput,
                           row=proxima_linha,
                           include_column_header=False)
        st.success('Dados enviados para o Google Sheets com sucesso!')
        # Limpa o estado para o próximo envio
        st.session_state.jsoninput = pd.DataFrame(columns=['B', 'C', 'D', 'E', 'F', 'G', 'H'])
    else:
        st.warning('Não há dados salvos para enviar. Clique em "Salvar" no formulário primeiro.')
