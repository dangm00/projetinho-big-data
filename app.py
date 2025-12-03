import streamlit as st
from controllers.dashboard import Dashboard

caminho = r"C:\Users\Dan\Documents\projetinho\planilha_de_servicos.xlsx"
dash = Dashboard(caminho)

st.title("📊 Dashboard de Serviços")

# Sidebar: filtros
filtro_servico = st.sidebar.multiselect(
    "Filtrar por serviço:",
    sorted(dash.modelo.df["SERVICO"].unique()),
    default=sorted(dash.modelo.df["SERVICO"].unique())
)

filtro_datas = st.sidebar.date_input(
    "Filtrar por datas:",
    [dash.modelo.df["DATA"].min().date(), dash.modelo.df["DATA"].max().date()]
)

graficos, filtros_ativos, df_filtrado = dash.gerar_graficos(filtro_servico, filtro_datas)

st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)

if graficos["pizza"]:
    st.plotly_chart(graficos["pizza"], use_container_width=True)
else:
    st.info("🍕 Gráfico de pizza oculto enquanto algum filtro está ativo")

st.plotly_chart(graficos["linha"], use_container_width=True)
st.plotly_chart(graficos["servicos"], use_container_width=True)
st.plotly_chart(graficos["mes"], use_container_width=True)
st.plotly_chart(graficos["regiao"], use_container_width=True)
