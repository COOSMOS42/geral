import streamlit as st

pg = st.navigation([
    st.Page("controlador.py", title="Atualizar Status", icon="💾"),
    st.Page("consultas.py", title="Consultar Documentos", icon="🗃️")
    st.Page("remover.py", title="Remover Documentos", icon="🗑️")
])
pg.run()
