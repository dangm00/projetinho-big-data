import pandas as pd

class Dados:
    def __init__(self, caminho):
        self.df = pd.read_excel(caminho, sheet_name="GERAL")
        self.normalizar_textos()
        self.preencher_servico_regiao()
        self.tratar_datas()

    def normalizar_textos(self):
        def normalizar(texto):
            if isinstance(texto, str):
                texto = texto.upper()
                acentos = {
                    "Ç": "C", "Ã": "A", "Õ": "O", "Á": "A", "À": "A", "Â": "A",
                    "É": "E", "Ê": "E", "Í": "I", "Ó": "O", "Ô": "O", "Ú": "U"
                }
                for a, b in acentos.items():
                    texto = texto.replace(a, b)
                texto = texto.strip()
            return texto
        self.df["SERVICO"] = self.df["SERVIÇO"].fillna("NAO TRABALHADO").apply(normalizar)

    def preencher_servico_regiao(self):
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
        self.df["REGIAO"] = self.df["SERVICO"].apply(definir_regiao).apply(lambda x: x.upper())

    def tratar_datas(self):
        self.df["DATA"] = pd.to_datetime(self.df["DATA"])
        self.df["MES"] = self.df["DATA"].dt.to_period("M").astype(str)
        self.df["TRABALHOU"] = self.df["SERVICO"] != "NAO TRABALHADO"

    def filtrar(self, servicos=None, datas=None):
        df_filtrado = self.df
        if servicos:
            df_filtrado = df_filtrado[df_filtrado["SERVICO"].isin(servicos)]
        if datas:
            df_filtrado = df_filtrado[
                (df_filtrado["DATA"].dt.date >= datas[0]) &
                (df_filtrado["DATA"].dt.date <= datas[1])
            ]
        return df_filtrado
