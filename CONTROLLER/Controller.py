from models.dados import Dados
from views.graficos import Graficos

class Dashboard:
    def __init__(self, caminho):
        self.modelo = Dados(caminho)
        self.view = Graficos()

    def gerar_graficos(self, servicos=None, datas=None):
        df = self.modelo.filtrar(servicos, datas)

        filtros_ativos = (
            servicos is not None or
            datas is not None
        )

        return {
            "pizza": self.view.grafico_pizza(df, filtros_ativos),
            "linha": self.view.grafico_linha(df),
            "servicos": self.view.grafico_servicos(df),
            "meses": self.view.grafico_meses(df),
            "regioes": self.view.grafico_regioes(df),
            "tabela": df
        }
