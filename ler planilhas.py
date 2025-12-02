import pandas as pd

# Caminho da planilha
caminho = r"C:\Users\Dan\Documents\projetinho\Planilha financeira DANIEL.xlsx"

# Ler a aba GERAL
df = pd.read_excel(caminho, sheet_name="GERAL")

# Substituir NaN em SERVIÇO por "NÃO TRABALHADO"
df["SERVIÇO"] = df["SERVIÇO"].fillna("NÃO TRABALHADO")

# Substituir NaN em REGIAO por "BAIXADA"
df["REGIAO"] = df["REGIAO"].fillna("BAIXADA")

# Mostrar tudo


print(df)




