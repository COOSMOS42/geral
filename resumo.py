import random
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def plot_gauge(
        indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=15, r=15, t=75, b=15, pad=12),
    )
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout='wide')

st.header("Resumo")
column_1, column_2, column_3, column_4, column_5, column_6 = st.columns(6)

column_7, column_8, column_9, column_10, column_11, column_12 = st.columns(6)

with column_1:
    plot_gauge(8, "#78FF0F", "", "PARCELA 01", 8)

with column_2:
    plot_gauge(8, "#78FF0F", "", "PARCELA 02", 8)

with column_3:
    plot_gauge(8, "#78FF0F", "", "PARCELA 03", 8)

with column_4:
    plot_gauge(7, "#78FF0F", "", "PARCELA 04", 8)

with column_5:
    plot_gauge(0, "#78FF0F", "", "PARCELA 05", 8)

with column_6:
    plot_gauge(0, "#78FF0F", "", "PARCELA 06", 8)

with column_7:
    plot_gauge(0, "#78FF0F", "", "PARCELA 07", 8)

with column_8:
    plot_gauge(0, "#78FF0F", "", "PARCELA 08", 8)

with column_9:
    plot_gauge(0, "#78FF0F", "", "PARCELA 09", 8)

with column_10:
    plot_gauge(0, "#78FF0F", "", "PARCECLA 10", 8)

with column_11:
    plot_gauge(0, "#78FF0F", "", "PARCELA 11", 8)

with column_12:
    plot_gauge(0, "#78FF0F", "", "PARCELA 12", 8)
