from models.dados import Dados
from views.graficos import Graficos

class Dashboard:
    def __init__(self, caminho):
        self.modelo = Dados(caminho)
        self.view = Graficos()

    def gerar_graficos(self, servicos=None, datas=None):
        df_filtrado = self.modelo.filtrar(servicos, datas)
        filtros_ativos = (
            servicos is not None or
            datas is not None
        )
        return {
            "pizza": self.view.pizza_trabalho(df_filtrado) if not filtros_ativos else None,
            "linha": self.view.linha_ganhos(df_filtrado),
            "servicos": self.view.barra_servicos(df_filtrado),
            "mes": self.view.barra_mes(df_filtrado),
            "regiao": self.view.barra_regiao(df_filtrado)
        }, filtros_ativos, df_filtrado
    