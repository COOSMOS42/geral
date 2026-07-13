import streamlit as st
import pandas as pd
import time
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from gspread_pandas import Spread, Client

# 1. DEFINIÇÃO DE ESCOPOS E AUTENTICAÇÃO
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Carrega as credenciais salvas nos Secrets do Streamlit
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = Client(scope=scope, creds=creds)

# !!! AJUSTE AQUI: Nome da sua nova planilha de Inventário !!!
spreadsheetname = "inventario_sae" 
sheet = client.open(spreadsheetname).sheet1

# 2. LEITURA E TRATAMENTO DOS DADOS DA PLANILHA
val = sheet.get_all_values()
df_inventario = pd.DataFrame(val)

# Define a primeira linha como o cabeçalho das colunas
cabecalho = df_inventario.iloc[0]
df_inventario = df_inventario[1:]
df_inventario.columns = cabecalho

# Configura a página do Streamlit para o modo amplo
st.set_page_config(layout='wide')

# 3. INTERFACE DO USUÁRIO
st.header('📦 Sistema de Inventário - SAE')

# Formulário de Busca por Subsistema
with st.form('busca_subsistema', clear_on_submit=False, border=True):
    st.subheader('Consultar Itens por Subsistema')
    
    # Criando uma caixa de texto para o usuário digitar o subsistema
    # Dica: se a coluna 'subsistema' tiver nomes fixos, você pode trocar por st.selectbox mais tarde
    lista_cr = ['Suspensão e Dinâmica Veicular', 'Aerodinâmica', 'Drivetrain', 'Powertrain', 'Eletrônica e Controle', 'Estrutura', 'Freio', 'Gestão de Pessoas', 'Marketing', 'Comercial', 'Patrimônio']
    subsistema_procurado = st.selectbox('Selecione o Subsistema (Ex: Aerodinamica, Elétrica):', (lista_cr))

    if st.form_submit_button('Pesquisar'):
        progress_text = "Buscando dados no inventário, aguarde..."
        my_bar = st.progress(0, text=progress_text)
        
        # Efeito visual de carregamento que você tinha no código original
        for percent_complete in range(100):
            time.sleep(0.005)
            my_bar.progress(percent_complete + 1, text=progress_text)

        # !!! IMPORTANTE: Certifique-se de que a coluna na sua planilha se chama exatamente 'subsistema' !!!
        # O .str.contains(..., case=False) ajuda a encontrar mesmo se o usuário digitar em maiúsculo ou minúsculo
        if subsistema_procurado:
            df_filtrado = df_inventario[df_inventario['subsistema'].str.contains(subsistema_procurado, case=False, na=False)]
            
            my_bar.empty() # Remove a barra de progresso
            
            # Mostra o resultado
            if not df_filtrado.empty:
                st.success(f"Foram encontrados {len(df_filtrado)} itens para o subsistema '{subsistema_procurado}'.")
                st.dataframe(df_filtrado, use_container_width=True)
            else:
                st.warning(f"Nenhum item encontrado para o subsistema '{subsistema_procurado}'. Verifique a grafia.")
        else:
            my_bar.empty()
            st.info("Por favor, digite um subsistema para pesquisar.")

# 4. VISUALIZAÇÃO COMPLETA DO INVENTÁRIO
st.subheader('📋 Inventário Completo')
with st.expander('Mostrar Todos os Itens'):
    st.dataframe(df_inventario, use_container_width=True, height=600)
