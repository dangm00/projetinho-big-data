import plotly.express as px
import pandas as pd

class Graficos:
    @staticmethod
    def pizza_trabalho(df):
        dias_trabalhados = df["TRABALHOU"].sum()
        dias_nao_trabalhados = len(df) - dias_trabalhados
        dados_pizza = pd.DataFrame({
            "Categoria": ["TRABALHOU", "NAO TRABALHADO"],
            "Dias": [dias_trabalhados, dias_nao_trabalhados]
        })
        fig = px.pie(
            dados_pizza,
            names="Categoria",
            values="Dias",
            title=f"🍕 Dias Trabalhados x Não Trabalhados — Total: {len(df)} dias",
            hole=0.3
        )
        fig.update_traces(textinfo='percent+label')
        return fig

    @staticmethod
    def linha_ganhos(df):
        ganhos_por_dia = df.groupby("DATA")["GANHOS"].sum().reset_index()
        fig = px.line(ganhos_por_dia, x="DATA", y="GANHOS", title="📈 Ganhos por Dia", markers=True)
        fig.update_layout(xaxis_title="Data", yaxis_title="Ganhos")
        return fig

    @staticmethod
    def barra_servicos(df):
        servicos_quantidade = df.groupby("SERVICO").size().reset_index(name="QTD")
        fig = px.bar(servicos_quantidade, x="SERVICO", y="QTD", text="QTD")
        fig.update_layout(xaxis_title="Serviço", yaxis_title="Quantidade")
        return fig

    @staticmethod
    def barra_mes(df):
        ganhos_por_mes = df.groupby("MES")["GANHOS"].sum().reset_index()
        fig = px.bar(ganhos_por_mes, x="MES", y="GANHOS", title="💰 Ganhos por Mês", text="GANHOS")
        fig.update_layout(xaxis_title="Mês", yaxis_title="Ganhos", xaxis_tickangle=-45)
        return fig

    @staticmethod
    def barra_regiao(df):
        regioes_quantidade = df.groupby("REGIAO").size().reset_index(name="QTD")
        fig = px.bar(regioes_quantidade, x="REGIAO", y="QTD", title="🌍 Quantidade de Serviços por Região", text="QTD")
        fig.update_layout(xaxis_title="Região", yaxis_title="Quantidade", xaxis_tickangle=-45)
        return fig
