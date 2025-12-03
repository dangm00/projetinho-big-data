import pandas as pd

# Caminho da planilha
caminho = r"C:\Users\Dan\Documents\projetinho\planilha_de_servicos.xlsx"

# Ler a aba GERAL
df = pd.read_excel(caminho, sheet_name="GERAL")

# Substituir NaN em SERVIÇO por "NÃO TRABALHADO"
df["SERVIÇO"] = df["SERVIÇO"].fillna("NÃO TRABALHADO")

# Preencher a REGIAO com base no SERVIÇO,fiz assim por que estava muito sujo
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

df["REGIAO"] = df["SERVIÇO"].apply(definir_regiao)

# Mostrar o DataFrame completo
print(df)





