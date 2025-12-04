import pandas as pd

class Dados:
    def __init__(self, caminho):
        self.df = pd.read_excel(caminho, sheet_name="GERAL")
        self.preparar_dados()

    def normalizar(self, texto):
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

    def definir_regiao(self, servico):
        servico = str(servico).upper()

        #  quando não trabalhado = SEM REGIAO
        if servico == "NAO TRABALHADO":
            return "SEM REGIAO"

        if "INSTALACAO" in servico:
            return "BAIXADA"
        elif "MANUTENCAO" in servico:
            return "ZONA NORTE"
        elif "IMPRODUTIVA" in servico:
            return "ZONA OESTE"
        else:
            return "BAIXADA"

    def preparar_dados(self):
        df = self.df

        df["SERVICO"] = df["SERVIÇO"].fillna("NAO TRABALHADO").apply(self.normalizar)
        df["REGIAO"] = df["SERVICO"].apply(self.definir_regiao).apply(self.normalizar)

        df["DATA"] = pd.to_datetime(df["DATA"])
        df["MES"] = df["DATA"].dt.to_period("M").astype(str)
        df["TRABALHOU"] = df["SERVICO"] != "NAO TRABALHADO"

        self.df = df

    def filtrar(self, servicos=None, datas=None):
        df = self.df.copy()

        if servicos:
            df = df[df["SERVICO"].isin(servicos)]

        if datas:
            df = df[
                (df["DATA"].dt.date >= datas[0]) &
                (df["DATA"].dt.date <= datas[1])
            ]

        return df

