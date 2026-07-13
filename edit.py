import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from gspread_pandas import Client

# Configuração da página
st.set_page_config(page_title='Editar Peças', layout='wide')

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
        df.insert(0, 'Linha na Planilha', df.index + 2)
        return df
    return pd.DataFrame()

df_inventario = carregar_dados()

st.title("✏️ Editar Peças")
st.subheader("Tabela Atual de Inventário")
st.dataframe(df_inventario, use_container_width=True)

st.divider()

st.subheader('Editar Dados da Peça')
st.markdown("*Nota: Preencha apenas os campos que deseja alterar. Deixe em branco os que quiser manter como estão.*")

with st.form('edit_form', clear_on_submit=True, border=True):
    linha_editar = st.number_input('Linha na Planilha para editar:', min_value=2, step=1)
    
    novo_valor = st.text_input('Novo Valor da Peça')
    nova_quantidade = st.text_input('Nova Quantidade')
    novo_status = st.selectbox('Novo Status', 
                               options=['', 'Disponível', 'Em uso', 'Manutenção', 'Falta', 'Outro'],
                               help="Deixe em branco se não quiser alterar o status.")
    
    if st.form_submit_button('Salvar Edições'):
        houve_alteracao = False
        try:
            # Índices das colunas no Google Sheets: 
            # 4: valor_peca | 5: quantidade | 8: status
            
            if novo_valor.strip() != "":
                sheet.update_cell(linha_editar, 4, novo_valor.strip())
                houve_alteracao = True
                
            if nova_quantidade.strip() != "":
                sheet.update_cell(linha_editar, 5, nova_quantidade.strip())
                houve_alteracao = True
                
            if novo_status.strip() != "":
                sheet.update_cell(linha_editar, 8, novo_status.strip())
                houve_alteracao = True
            
            if houve_alteracao:
                st.success(f'Linha {linha_editar} atualizada com sucesso!')
                st.rerun()
            else:
                st.warning('Nenhum dado foi preenchido. A linha permaneceu inalterada.')
                
        except Exception as e:
            st.error(f"Erro ao atualizar os dados: {e}")
