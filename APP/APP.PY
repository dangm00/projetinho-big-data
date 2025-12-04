import streamlit as st
from controllers.dashboard import Dashboard

st.title("📊 Dashboard de Serviços — MVC")

caminho = r"C:\Users\Dan\Documents\projetinho\planilha_de_servicos.xlsx"
dash = Dashboard(caminho)

# Sidebar
df = dash.modelo.df

filtro_servico = st.sidebar.multiselect(
    "Filtrar por serviço:",
    sorted(df["SERVICO"].unique()),
    default=sorted(df["SERVICO"].unique())
)

filtro_datas = st.sidebar.date_input(
    "Filtrar por datas:",
    [df["DATA"].min().date(), df["DATA"].max().date()]
)

graficos = dash.gerar_graficos(
    servicos=filtro_servico,
    datas=filtro_datas
)

st.subheader("Dados Filtrados")
st.dataframe(graficos["tabela"])
