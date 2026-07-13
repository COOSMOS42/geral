import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from gspread_pandas import Client

# Configuração da página (opcional em subpáginas, mas recomendado para manter o layout)
st.set_page_config(page_title='Remover Peças', layout='wide')

# Autenticação e conexão com o Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = Client(scope=scope, creds=creds)

spreadsheetname = "inventario_sae" 
sheet = client.open(spreadsheetname).sheet1

def carregar_dados():
    val = sheet.get_all_values()
    df = pd.DataFrame(val)
    if not df.empty and len(df) > 1:
        cabecalho = df.iloc[0]
        df = df[1:]
        df.columns = cabecalho
        df = df.reset_index(drop=True)
        # Cria a coluna de referência indicando a linha exata no Sheets
        df.insert(0, 'Linha na Planilha', df.index + 2)
        return df
    return pd.DataFrame()

df_inventario = carregar_dados()

st.title("🗑️ Remover Peças")
st.subheader("Tabela Atual de Inventário")
st.dataframe(df_inventario, use_container_width=True)

st.divider()

st.subheader('Remover Item do Inventário')
st.write("Verifique na tabela acima o número da **Linha na Planilha** que deseja excluir.")

with st.form('rmv_form', clear_on_submit=True, border=True):
    linha_remover = st.number_input('Qual a Linha na Planilha que deseja remover?', min_value=2, step=1)
    
    if st.form_submit_button('Remover Linha'):
        try:
            sheet.delete_rows(linha_remover)
            st.success(f'Linha {linha_remover} removida com sucesso!')
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao remover a linha: {e}")
