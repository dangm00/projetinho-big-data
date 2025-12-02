import pandas as pd
import streamlit as st

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
        texto = texto.replace("Ç", "C")
        texto = texto.replace("Ã", "A").replace("Õ", "O").replace("Á", "A")
        texto = texto.replace("É", "E").replace("Ê", "E")
        texto = texto.replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
        texto = texto.replace("Â", "A").replace("Ô", "O")
        texto = texto.strip()
    return texto

df["SERVICO"] = df["SERVIÇO"].fillna("NAO TRABALHADO").apply(normalizar)
df["REGIAO"] = df["REGIAO"].fillna("BAIXADA").apply(normalizar)

# ====================================================
# 3. TRATAMENTO DE DATAS
# ====================================================
df["DATA"] = pd.to_datetime(df["DATA"])
df["MES"] = df["DATA"].dt.to_period("M").astype(str)

# ====================================================
# 4. CRIAÇÃO DAS MÉTRICAS DO DASHBOARD
# ====================================================

# 4.1 Dias trabalhados vs não trabalhados
df["TRABALHOU"] = df["SERVICO"] != "NAO TRABALHADO"
dias_trabalhados = df["TRABALHOU"].sum()
dias_nao_trabalhados = len(df) - dias_trabalhados

# 4.2 Ganhos por dia
ganhos_por_dia = df.groupby("DATA")["GANHOS"].sum()

# 4.3 Serviços mais realizados
servicos_quantidade = df.groupby("SERVICO").size().reset_index(name="QTD")

# 4.4 Ganhos por mês
ganhos_por_mes = df.groupby("MES")["GANHOS"].sum().reset_index()

# ====================================================
# 5. STREAMLIT – DASHBOARD
# ====================================================

st.title("📊 Dashboard Financeiro – Daniel")

st.subheader("Dados Originais Tratados")
st.dataframe(df)

# -------------------------
# 1. Pizza: Trabalhado x Não Trabalhado
# -------------------------
st.subheader("🍕 Dias Trabalhados x Não Trabalhados")
st.write("Mostra quantos dias você realmente trabalhou no mês.")

st.pyplot(
    df["TRABALHOU"]
    .value_counts()
    .rename({True: "TRABALHOU", False: "NAO TRABALHOU"})
    .plot.pie(autopct="%1.1f%%")
    .figure
)

# -------------------------
# 2. Linha: Ganhos por dia
# -------------------------
st.subheader("📈 Ganhos por Dia")
st.line_chart(ganhos_por_dia)

# -------------------------
# 3. Barra: Serviços mais realizados
# -------------------------
st.subheader("🧰 Serviços Realizados")
st.bar_chart(servicos_quantidade.set_index("SERVICO"))

# -------------------------
# 4. Barra: Ganhos por mês
# -------------------------
st.subheader("💰 Ganhos por Mês")
st.bar_chart(ganhos_por_mes.set_index("MES"))

st.success("Dashboard carregado com sucesso!")
