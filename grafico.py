import streamlit as st
import pandas as pd
import plotly.express as px

# ===== CARREGAR EXCEL =====
df = pd.read_excel(
    r"C:\Users\Dan\Documents\projeto big data\Planilha financeira DANIEL.xlsx",
    sheet_name="GERAL"
)

# Renomear colunas removendo os ":" finais
df.columns = [col.replace(":", "").strip() for col in df.columns]

# Converter DATA para datetime
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")

st.title("📊 Dashboard Financeiro – Calendário de Trabalho")

# ===== CARDs =====
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Ganhos Totais", f"R$ {df['GANHOS'].sum():,.2f}")

with col2:
    st.metric("💸 Despesas Totais", f"R$ {df['DESPESAS'].count()} despesas")

with col3:
    st.metric("🚗 Km Total (0,85)", f"{df['QUILOMETRAGEM R$0,85'].sum():,.0f} km")

# ===== GRÁFICO GANHOS POR DIA =====

fig_ganhos = px.line(
    df,
    x="DATA",
    y="GANHOS",
    title="Ganhos por Dia",
    markers=True
)

st.plotly_chart(fig_ganhos, use_container_width=True)

# ===== GRÁFICO DE QUILOMETRAGEM =====
fig_km = px.bar(
    df,
    x="DATA",
    y="QUILOMETRAGEM R$0,85",
    title="Quilometragem por Dia (R$ 0,85)",
)

st.plotly_chart(fig_km, use_container_width=True)

# ===== TABELA COMPLETA =====
st.subheader("📅 Tabela Completa de Registros")
st.dataframe(df)
