import pandas as pd
import streamlit as st
import plotly.express as px


#Ler a planilha com caminho

caminho = r"C:\Users\Dan\Documents\projetinho\planilha_de_servicos.xlsx"
df = pd.read_excel(caminho, sheet_name="GERAL")


# Padronizar os textos

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

# Preencher SERVICO
df["SERVICO"] = df["SERVIÇO"].fillna("NAO TRABALHADO").apply(normalizar)

# Preencher REGIAO com base no SERVICO(necessario pois a planilha estava bem suja)
def definir_regiao(servico):
    servico = str(servico).upper()
    if "INSTALACAO" in servico:
        return "BAIXADA"
    elif "MANUTENCAO" in servico:
        return "ZONA NORTE"
    elif "IMPRODUTIVA" in servico:
        return "ZONA OESTE"
    else:
        return "BAIXADA"

df["REGIAO"] = df["SERVICO"].apply(definir_regiao).apply(normalizar)


# TRatamento das datas(codigo estava sujo)

df["DATA"] = pd.to_datetime(df["DATA"])
df["MES"] = df["DATA"].dt.to_period("M").astype(str)
df["TRABALHOU"] = df["SERVICO"] != "NAO TRABALHADO"


# Filtros

st.sidebar.title("📌 Filtros do Dashboard")

# Serviços
filtro_servico = st.sidebar.multiselect(
    "Filtrar por serviço:",
    sorted(df["SERVICO"].unique()),
    default=sorted(df["SERVICO"].unique())
)

# Datas
filtro_datas = st.sidebar.date_input(
    "Filtrar por datas:",
    [df["DATA"].min().date(), df["DATA"].max().date()]
)

# Aplicar filtros
df_filtrado = df[df["SERVICO"].isin(filtro_servico)]
df_filtrado = df_filtrado[
    (df_filtrado["DATA"].dt.date >= filtro_datas[0]) &
    (df_filtrado["DATA"].dt.date <= filtro_datas[1])
]


#  DASHBOARD PRINCIPAL

st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)

# Verificar se algum filtro está ativo
filtros_ativos = (
    set(filtro_servico) != set(df["SERVICO"].unique()) or
    filtro_datas[0] != df["DATA"].min().date() or
    filtro_datas[1] != df["DATA"].max().date()
)

#Gráfico de Pizza: Trabalhado x Não Trabalhado
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

#Gráfico de Linha: Ganhos por Dia
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

# Gráfico de Barra: Serviços mais Realizados
servicos_quantidade = df_filtrado.groupby("SERVICO").size().reset_index(name="QTD")
fig_bar_servicos = px.bar(
    servicos_quantidade,
    x="SERVICO",
    y="QTD",
    text="QTD"
)
fig_bar_servicos.update_layout(xaxis_title="Serviço", yaxis_title="Quantidade")
st.plotly_chart(fig_bar_servicos, use_container_width=True)

#Gráfico de Barra: Ganhos por Mês
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

# Gráfico de Barra: Quantidade por Região
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
