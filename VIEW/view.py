import plotly.express as px
import pandas as pd
import streamlit as st

class Graficos:

    def grafico_pizza(self, df, filtros_ativos):
        if filtros_ativos:
            st.info("🍕 Gráfico de pizza oculto enquanto algum filtro está ativo")
            return

        dias_trabalhados = df["TRABALHOU"].sum()
        dias_nao = len(df) - dias_trabalhados

        dados = pd.DataFrame({
            "Categoria": ["TRABALHOU", "NAO TRABALHADO"],
            "Dias": [dias_trabalhados, dias_nao]
        })

        fig = px.pie(
            dados, names="Categoria", values="Dias",
            title=f"🍕 Dias Trabalhados x Não Trabalhados — Total: {len(df)} dias",
            hole=0.3
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    def grafico_linha(self, df):
        ganhos = df.groupby("DATA")["GANHOS"].sum().reset_index()
        fig = px.line(ganhos, x="DATA", y="GANHOS", markers=True,
                      title="📈 Ganhos por Dia")
        st.plotly_chart(fig, use_container_width=True)

    def grafico_servicos(self, df):
        quantidade = df.groupby("SERVICO").size().reset_index(name="QTD")
        fig = px.bar(quantidade, x="SERVICO", y="QTD", text="QTD",
                     title="🧰 Quantidade por Serviço")
        st.plotly_chart(fig, use_container_width=True)

    def grafico_meses(self, df):
        ganhos = df.groupby("MES")["GANHOS"].sum().reset_index()
        fig = px.bar(ganhos, x="MES", y="GANHOS", text="GANHOS",
                     title="💰 Ganhos por Mês")
        st.plotly_chart(fig, use_container_width=True)

    def grafico_regioes(self, df):
        regioes = df.groupby("REGIAO").size().reset_index(name="QTD")
        fig = px.bar(regioes, x="REGIAO", y="QTD", text="QTD",
                     title="🌍 Quantidade por Região")
        st.plotly_chart(fig, use_container_width=True)
