import streamlit as st
import pandas as pd
import time
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

'''
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
'''

# 2. LEITURA E TRATAMENTO DOS DADOS DA PLANILHA
val = sheet.get_all_values()
df_inventario = pd.DataFrame(val)

# Define a primeira linha como o cabeçalho das colunas
cabecalho = df_inventario.iloc[0]
df_inventario = df_inventario[1:]
df_inventario.columns = cabecalho

# Formulário de Busca por Subsistema
with st.form('busca_subsistema', clear_on_submit=False, border=True):
    st.subheader('Consultar Itens por Status')
    
    # Criando uma caixa de texto para o usuário digitar o status
    lista_cr = ['Solicitado', 'Disponível', 'Em uso', 'Manutenção', 'Falta', 'Outro', 'Em análise', 'Comprado', 'Aguardando chegada']
    status_procurado = st.selectbox('Selecione o Status:', (lista_cr))

    if st.form_submit_button('Pesquisar'):
        progress_text = "Buscando dados no inventário, aguarde..."
        my_bar = st.progress(0, text=progress_text)
        
        # Efeito visual de carregamento que você tinha no código original
        for percent_complete in range(100):
            time.sleep(0.005)
            my_bar.progress(percent_complete + 1, text=progress_text)

        # !!! IMPORTANTE: Certifique-se de que a coluna na sua planilha se chama exatamente 'status' !!!
        # O .str.contains(..., case=False) ajuda a encontrar mesmo se o usuário digitar em maiúsculo ou minúsculo
        if status_procurado:
            df_filtrado = df_inventario[df_inventario['status'].str.contains(status_procurado, case=False, na=False)]
            
            my_bar.empty() # Remove a barra de progresso
            
            # Mostra o resultado
            if not df_filtrado.empty:
                st.success(f"Foram encontrados {len(df_filtrado)} itens para o status '{status_procurado}'.")
                st.dataframe(df_filtrado, use_container_width=True)
            else:
                st.warning(f"Nenhum item encontrado para o status '{status_procurado}'.")
        else:
            my_bar.empty()
            st.info("Por favor, digite um status para pesquisar.")

st.title("✏️ Editar Peças")

'''
st.subheader("Tabela Atual de Inventário")
st.dataframe(df_inventario, use_container_width=True)
'''

st.divider()

st.subheader('Editar Dados da Peça')
st.markdown("*Nota: Preencha apenas os campos que deseja alterar. Deixe em branco os que quiser manter como estão.*")

with st.form('edit_form', clear_on_submit=True, border=True):
    linha_editar = st.number_input('Linha na Planilha para editar:', min_value=1, step=1)
#    linha_editar = linha + 1
    
    novo_valor = st.text_input('Novo Valor da Peça')
    nova_quantidade = st.text_input('Nova Quantidade')
    novo_status = st.selectbox('Novo Status', 
                               options=['', 'Disponível', 'Em uso', 'Manutenção', 'Falta', 'Outro', 'Em análise', 'Comprado', 'Aguardando chegada'],
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
