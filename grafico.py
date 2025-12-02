import pandas as pd
import streamlit as st
import plotly.express as px

# ====================================================
# 1. LEITURA DA PLANILHA
# ====================================================
caminho = r"C:\Users\Dan\Documents\projetinho\Planilha financeira DANIEL.xlsx"
df = pd.read_excel(caminho, sheet_name="GERAL")

# ====================================================
# 2. PADRONIZAÇÃO DE TEXTOS
# ====================================================
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

# ====================================================
# 3. TRATAMENTO DE DATAS
# ====================================================
df["DATA"] = pd.to_datetime(df["DATA"])
df["MES"] = df["DATA"].dt.to_period("M").astype(str)
df["TRABALHOU"] = df["SERVICO"] != "NAO TRABALHADO"

# ====================================================
# 4. SIDEBAR - FILTROS
# ====================================================
st.sidebar.title("📌 Filtros do Dashboard")

# Mês
filtro_mes = st.sidebar.selectbox(
    "Filtrar por mês:",
    sorted(df["MES"].unique())
)

# Serviço
filtro_servico = st.sidebar.multiselect(
    "Filtrar por serviço:",
    sorted(df["SERVICO"].unique()),
    default=sorted(df["SERVICO"].unique())
)

# Intervalo de datas
filtro_datas = st.sidebar.date_input(
    "Filtrar por datas:",
    [df["DATA"].min().date(), df["DATA"].max().date()]
)

# Botão aplicar filtros
if st.sidebar.button("Aplicar Filtros"):
    df_filtrado = df[df["MES"] == filtro_mes]
    df_filtrado = df_filtrado[df_filtrado["SERVICO"].isin(filtro_servico)]
    df_filtrado = df_filtrado[
        (df_filtrado["DATA"].dt.date >= filtro_datas[0]) &
        (df_filtrado["DATA"].dt.date <= filtro_datas[1])
    ]
else:
    df_filtrado = df.copy()

# ====================================================
# 5. DASHBOARD PRINCIPAL
# ====================================================
st.title("📊 Dashboard Financeiro – Daniel")
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)

# -------------------------
# 5.1 Pizza: Trabalhado x Não Trabalhado
# -------------------------
# Verifica se algum filtro está ativo
filtros_ativos = (
    filtro_mes != df["MES"].min() or
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

# -------------------------
# 5.2 Linha: Ganhos por dia
# -------------------------
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

# -------------------------
# 5.3 Barra: Serviços mais realizados
# -------------------------
servicos_quantidade = df_filtrado.groupby("SERVICO").size().reset_index(name="QTD")
fig_bar_servicos = px.bar(
    servicos_quantidade,
    x="SERVICO",
    y="QTD",
    title="🧰 Quantidade de Serviços Realizados",
    text="QTD"
)
fig_bar_servicos.update_layout(xaxis_title="Serviço", yaxis_title="Quantidade")
st.plotly_chart(fig_bar_servicos, use_container_width=True)

# -------------------------
# 5.4 Barra: Ganhos por mês
# -------------------------
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

st.success("✅ Dashboard carregado com sucesso!")
