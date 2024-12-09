import streamlit as st
import pandas as pd
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
sheet = client.open(spreadsheetname).worksheet("glosas")

val = sheet.get_all_values()
# fr é a variavel da planilha do google sheets
fr = pd.DataFrame(val)
#separa a primeira linha da planilha google sheets
cab = fr.iloc[0]
#fazendo com que a planilha seja lida a partir da primeira linha
fr = fr[1:]
#seta as colunas
fr.columns = cab
st.set_page_config(page_title='Sistema de Cadastramento de Entregas',
                   layout='wide')

#with open("styles2.css") as f:
#    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

#lista das entrega feitas atravez do formulario, as entregas vão se acumulando nessa lista até o resete de site
if 'jsoninput' not in st.session_state:
    st.session_state.jsoninput = None


#adiciona um entrega a lista acima
# dia 07/11 foi alterado de Destinatário para Status pois não faz sentido manter como destinario se com status eu tenho mais informações
def adicionar_entrega(Data, Parcela, Documento, Status, Glosa, Observação):
    entrega = {
        'data': Data,
        'parcela': Parcela,
        'documento': Documento,
        'status' : Status,
        'glosa' : Glosa,
        'observação' : Observação
    }

    st.session_state.jsoninput = pd.concat(
        [st.session_state.jsoninput,
         pd.DataFrame(entrega, index=[0])],
        ignore_index=True)

    return st.session_state.jsoninput


# Carregando as entregas ao iniciar a aplicação
st.header('Adicionar Glosa')    
   
# formulário para preenchimento dos dados que serão inputados na lista cache
with st.form('Preencha os dados', clear_on_submit=True, border=True):
    st.subheader('Data')
    data = st.date_input('Data de envio',
                         datetime.now().date(),
                         format='DD/MM/YYYY')
    a = str(data)
    dataformat = f'{a[-2:]}/{a[5:7]}/{a[:4]}'

    st.subheader('Documento')
    parcela = st.selectbox('Escolha a Parcela', ('I', 'II', 'III',
                                                 'IV', 'V','VI', 'VII', 'VIII', 'IX', 'X', 'XI',
                                                 'XII') )
    documento = st.selectbox('Qual o documento referido?', ('Virgílio Távora I', 'Virgílio Távora II', 'Virgílio Távora III', 'Demócrito Dummar I', 'Demócrito Dummar II', 'Demócrito Dummar III', 'Blanchard Girão', 'Bonaparte Viana') )
    pardoc = parcela + " " + documento

    status = st.selectbox('Status da Glosa', ('Aguardando resposta', 'Em análise', 'Relatório de Desglosa', 'Pago'))

    st.subheader('Glosa')
    glosa = st.text_input('Qual o Valor da Glosa?')
    
    st.subheader('Observação')
    obs = st.text_input('Alguma observação?')

    st.subheader('Adicionar Glosa')

    if st.form_submit_button('Adicionar'):
        st.session_state.jsoninput = adicionar_entrega(
            dataformat, parcela, documento, status, glosa, obs)

st.subheader('Salvar')

#cria um datafreame para que os dados contidos na lista jsoninput sejam alocadas para a planilha d google sheets
st.session_state.jsoninput = pd.DataFrame(st.session_state.jsoninput)

if st.button('Enviar para Google Sheets'):
    # Buscar os dados já existentes no Google Sheets
    existing_data = pd.DataFrame(sheet.get_all_records(""))

    # Remover duplicatas antes de enviar
    if not existing_data.empty:
        new_data = st.session_state.jsoninput[
            ~st.session_state.jsoninput.isin(existing_data.to_dict('list')).all(axis=1)
        ]
    else:
        new_data = st.session_state.jsoninput

    # Verificar se há novos dados para enviar
    if not new_data.empty:
        set_with_dataframe(sheet,
                           new_data,
                           row=len(sheet.col_values(1)) + 1,
                           include_column_header=False)
        st.success('Dados enviados com sucesso!')
    else:
        st.info('Nenhum dado novo para enviar.')


st.subheader('Lista')
with st.expander('Mostrar Lista'):
    st.dataframe(fr, use_container_width=True, height=800)
