import streamlit as st

pg = st.navigation([
    st.Page("controlador.py", title="Lançamentos"),
    st.Page("edit.py", title="Editar Peças"),
    st.Page("remover.py", title="Remover Peças")
])
pg.run()
