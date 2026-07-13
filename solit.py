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

# Autenticar com o gspread padrão
client = gspread.authorize(creds)

spreadsheetname = "inventario_sae" 

try:
    sheet = client.open(spreadsheetname).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"Erro: A planilha '{spreadsheetname}' não foi encontrada.")
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

# Inicializa a tabela local se não existir
if 'jsoninput' not in st.session_state:
    st.session_state.jsoninput = pd.DataFrame(columns=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])

# --- NOVO: Inicializa o rastreador do último item salvo para evitar duplicadas por Enter ---
if 'ultimo_salvo' not in st.session_state:
    st.session_state.ultimo_salvo = None

def adicionar_entrega(B, C, D, E, F, G, H, I):
    entrega = {
        'B': [str(B)],
        'C': [C],
        'D': [D],
        'E': [E],
        'F': [F],
        'G': [G],
        'H': [str(H)],
        'I': [I]
    }
    
    nova_linha = pd.DataFrame(entrega)
    st.session_state.jsoninput = pd.concat([st.session_state.jsoninput, nova_linha], ignore_index=True)
    return st.session_state.jsoninput

with st.form('Preencha os dados', clear_on_submit=False, border=True):
    st.subheader('Solicitar')
    b = st.date_input(label='Selecione uma data', format='DD/MM/YYYY')
  
    lista_cr = ['Suspensão e Dinâmica Veicular', 'Aerodinâmica', 'Drivetrain', 'Powertrain', 'Eletrônica e Controle', 'Estrutura', 'Freio', 'Gestão de Pessoas', 'Marketing', 'Comercial', 'Patrimônio']
    c = st.selectbox('Selecione o centro de responsabilidade', lista_cr)
  
    d = st.text_input('Nome da Peça')
    e = st.text_input('Valor')
    f = st.selectbox('Quantidade', range(1,101))
    g = st.selectbox('Natureza', ("Descartavel", 'Não Descartavel'))
    h = st.text_input('Decrição')
    i = st.selectbox('Status', ('Solicitado',)) # Pequeno ajuste para tupla válida

    st.write('Salve as informações antes do envio')
    
    if st.form_submit_button('Salvar'):
        # Criamos uma assinatura única (uma tupla) do que está preenchido AGORA
        dados_atuais = (str(b), c, d, e, f, g, str(h), i)
        
        # Se o usuário esquecer de digitar o nome da peça, nem deixa salvar vazio
        if not d.strip():
            st.error("Por favor, digite o 'Nome da Peça' antes de salvar.")
        
        # Bloqueia se os dados forem IDÊNTICOS ao clique imediatamente anterior
        elif dados_atuais == st.session_state.ultimo_salvo:
            st.warning('⚠️ Atenção: Esses dados já foram salvos! Altere os campos ou envie os dados para fazer um novo lançamento.')
        
        else:
            # Se mudou algo ou é o primeiro clique, salva normalmente
            st.session_state.jsoninput = adicionar_entrega(b, c, d, e, f, g, h, i)
            # Atualiza o "rastreador" com os dados que acabaram de ser salvos
            st.session_state.ultimo_salvo = dados_atuais
            st.success('Informações salvas localmente com sucesso!')

# Mostrar tabela com o que já foi salvo localmente nesta sessão (ajuda o usuário a ver o que já fez)
if not st.session_state.jsoninput.empty:
    st.write("📋 **Itens prontos para envio nesta sessão:**")
    st.dataframe(st.session_state.jsoninput, use_container_width=True)

if st.button('Enviar dados 📨'):
    if not st.session_state.jsoninput.empty:
        proxima_linha = len(sheet.col_values(1)) + 1
        
        set_with_dataframe(sheet,
                           st.session_state.jsoninput,
                           row=proxima_linha,
                           include_column_header=False)
        st.success('Dados enviados para o Google Sheets com sucesso!')
        
        # Limpa o estado e limpa a trava para permitir novos cadastros idênticos no futuro se quiser
        st.session_state.jsoninput = pd.DataFrame(columns=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
        st.session_state.ultimo_salvo = None
        
        # Recarrega a página para limpar a interface visualmente
        st.rerun()
    else:
        st.warning('Não há dados salvos para enviar. Clique em "Salvar" no formulário primeiro.')
