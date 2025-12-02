import pandas as pd
import streamlit as st
import plotly.express as px


# ler planilha

caminho = r"C:\Users\Dan\Documents\projetinho\Planilha financeira DANIEL.xlsx"
df = pd.read_excel(caminho, sheet_name="GERAL")


# padronizarr os textos

def normalizar(texto):
    if isinstance(texto, str):
        texto = texto.upper()
        acentos = {
            "Ç": "C", "Ã": "A", "Õ": "O", "Á": "A", "À": "A", "Â": "A",
            "É": "E", "Ê": "E", "Í": "I",
            "Ó": "O", "Ô": "O", "Ú": "U"
        }
        for a, b in acentos.items():
            texto = texto.replace(a, b)
        texto = texto.strip()
    return texto

df["SERVICO"] = df["SERVIÇO"].fillna("NAO TRABALHADO").apply(normalizar)
df["REGIAO"]  = df["REGIAO"].fillna("BAIXADA").apply(normalizar)


# tratamento das datas

df["DATA"] = pd.to_datetime(df["DATA"])
df["MES"] = df["DATA"].dt.to_period("M").astype(str)
df["TRABALHOU"] = df["SERVICO"] != "NAO TRABALHADO"


#  FILTROS

st.sidebar.title("📌 Filtros do Dashboard")

# Serviços
filtro_servico = st.sidebar.multiselect(
    "Filtrar por serviço:",
    sorted(df["SERVICO"].unique()),
    default=sorted(df["SERVICO"].unique())
)

# filtro  de datas
filtro_datas = st.sidebar.date_input(
    "Filtrar por datas:",
    [df["DATA"].min().date(), df["DATA"].max().date()]
)

# adicionar filtros
df_filtrado = df[df["SERVICO"].isin(filtro_servico)]
df_filtrado = df_filtrado[
    (df_filtrado["DATA"].dt.date >= filtro_datas[0]) &
    (df_filtrado["DATA"].dt.date <= filtro_datas[1])
]


# dashboarding principal
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)


# grafico de  Pizza: Trabalhado x Não Trabalhado

# Verificar se algum filtro está ativo
filtros_ativos = (
    set(filtro_servico) != set(df["SERVICO"].unique()) or
    filtro_datas[0] != df["DATA"].min().date() or
    filtro_datas[1] != df["DATA"].max().date()
)

if not filtros_ativos:
    dias_trabalhados = df_filtrado["TRABALHOU"].sum()
    dias_nao_trabalhados = len(df_filtrado) - dias_trabalhados
    dados_pizza = pd.DataFrame({
        "Categoria": ["TRABALHOU", "NAO TRABALHADO"],
        "Dias": [dias_trabalhados, dias_nao_trabalhados]
    })

    fig_pizza = px.pie(
        dados_pizza,
        names="Categoria",
        values="Dias",
        title=f"🍕 Dias Trabalhados x Não Trabalhados — Total: {len(df_filtrado)} dias",
        hole=0.3
    )
    fig_pizza.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pizza, use_container_width=True)
else:
    st.info("🍕 Gráfico de pizza oculto enquanto algum filtro está ativo")


# grafico de Linha: Ganhos por dia

ganhos_por_dia = df_filtrado.groupby("DATA")["GANHOS"].sum().reset_index()
fig_linha = px.line(
    ganhos_por_dia,
    x="DATA",
    y="GANHOS",
    title="📈 Ganhos por Dia",
    markers=True
)
fig_linha.update_layout(xaxis_title="Data", yaxis_title="Ganhos")
st.plotly_chart(fig_linha, use_container_width=True)


# grafico de  Barra: Serviços mais realizados

servicos_quantidade = df_filtrado.groupby("SERVICO").size().reset_index(name="QTD")
fig_bar_servicos = px.bar(
    servicos_quantidade,
    x="SERVICO",
    y="QTD",
    title="👨‍🔧 Quantidade de Serviços Realizados",
    text="QTD"
)
fig_bar_servicos.update_layout(xaxis_title="Serviço", yaxis_title="Quantidade")
st.plotly_chart(fig_bar_servicos, use_container_width=True)


# grafico de barra: Ganhos por mês

ganhos_por_mes = df_filtrado.groupby("MES")["GANHOS"].sum().reset_index()
fig_bar_mes = px.bar(
    ganhos_por_mes,
    x="MES",
    y="GANHOS",
    title="💰 Ganhos por Mês",
    text="GANHOS"
)
fig_bar_mes.update_layout(
    xaxis_title="Mês",
    yaxis_title="Ganhos",
    xaxis_tickangle=-45,
)
st.plotly_chart(fig_bar_mes, use_container_width=True)


# grafico de  barra: Quantidade por Região

regioes_quantidade = df_filtrado.groupby("REGIAO").size().reset_index(name="QTD")
fig_bar_regioes = px.bar(
    regioes_quantidade,
    x="REGIAO",
    y="QTD",
    title="🌍 Quantidade de Serviços por Região",
    text="QTD"
)
fig_bar_regioes.update_layout(
    xaxis_title="Região",
    yaxis_title="Quantidade",
    xaxis_tickangle=-45,
)
st.plotly_chart(fig_bar_regioes, use_container_width=True)


