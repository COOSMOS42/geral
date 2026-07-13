import streamlit as st

pg = st.navigation([
    st.Page("edit.py", title="Editar Peças"),
    st.Page("remover.py", title="Remover Peças")
])
pg.run()
