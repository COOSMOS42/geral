import streamlit as st

def paginainicial():
    st.title("Second page")
    
pg = st.navigation([
    st.Page(paginainicial, title="Página Inicial", icon="🪙"),
    st.Page("controlador.py", title="Atualizar Status", icon="💾"),
    st.Page("consultas.py", title="Consultar Documentos", icon="🗃️")

])
pg.run()
