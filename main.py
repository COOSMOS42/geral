import streamlit as st


with open("stylesmain.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

def paginainicial():

pg = st.navigation([
    st.Page(paginainicial, title="Página Inicial", icon="🪙"),
    st.Page("controlador.py", title="Atualizar Status", icon="💾"),
    st.Page("consultas.py", title="Consultar Documentos", icon="🗃️")

])
pg.run()
