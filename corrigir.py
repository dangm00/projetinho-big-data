import pandas as pd
import unicodedata
import re
from difflib import get_close_matches
from collections import Counter

# --- CONFIGURAÇÃO ---
caminho = r"C:\\Users\Dan\\Documents\\projetinho\\planilha_de_servicos.xlsx"
aba = "GERAL"

# --- FUNÇÕES DE LIMPEZA ---
def strip_accents(text):
    """
    Remove acentos/diacríticos e transforma 'ç' -> 'c' etc.
    Retorna string ASCII.
    """
    if pd.isna(text):
        return text
    if not isinstance(text, str):
        text = str(text)
    # Normaliza e remove diacríticos
    nfkd = unicodedata.normalize('NFKD', text)
    only_ascii = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return only_ascii

def clean_string(text):
    """
    Normaliza: remove acentos, coloca em maiúsculas, remove múltiplos espaços,
    remove caracteres indesejados (mantém letras, números e espaços).
    """
    if pd.isna(text):
        return text
    s = strip_accents(text)
    s = s.upper().strip()
    # manter apenas letras, números e espaço
    s = re.sub(r'[^A-Z0-9 ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s

# --- LEITURA ---
df = pd.read_excel(caminho, sheet_name=aba)

# Substituir NaN conforme você pediu anteriormente
df["SERVIÇO"] = df["SERVIÇO"].fillna("NÃO TRABALHADO")
df["REGIAO"] = df["REGIAO"].fillna("BAIXADA")

# --- CRIA VERSÕES LIMPA/INTERMEDIÁRIAS ---
# 1) versão limpa sem acentos e em maiúsculas
df["SERVICO_CLEAN"] = df["SERVIÇO"].apply(clean_string)

# 2) obter lista de valores únicos e frequências (antes de agrupar)
unique_vals = df["SERVICO_CLEAN"].value_counts().to_dict()

# --- AGRUPAR VARIANTES PARECIDAS (fuzzy matching) ---
# Vamos criar grupos usando get_close_matches: valores muito parecidos serão mapeados
keys = list(unique_vals.keys())

# ordem por frequência para escolher "representante" do grupo
sorted_keys = sorted(keys, key=lambda k: -unique_vals.get(k,0))

mapping = {}  # map from original CLEAN -> canonical CLEAN

for k in sorted_keys:
    if k in mapping:
        continue
    # pega matches próximos (cutoff ajustável; 0.8 é razoável)
    matches = get_close_matches(k, keys, n=50, cutoff=0.82)
    # marcar todos os matches para o representante k
    for m in matches:
        mapping[m] = k

# Aplicar mapeamento para criar o rótulo final (padronizado)
df["SERVICO_PADRONIZADO"] = df["SERVICO_CLEAN"].map(mapping)

# Se quiser que os nomes finais fiquem em formato 'Título' sem acentos:
df["SERVICO_PADRONIZADO_TITULO"] = df["SERVICO_PADRONIZADO"].str.title()

# --- SALVAR MAPA DE CORREÇÃO PARA REVISÃO ---
# criar um DataFrame de mapeamento (original -> padronizado)
map_rows = []
for orig in sorted(unique_vals.keys()):
    map_rows.append({
        "SERVICO_CLEAN_ORIGINAL": orig,
        "FREQUENCIA": unique_vals.get(orig, 0),
        "SERVICO_PADRONIZADO": mapping.get(orig)
    })
map_df = pd.DataFrame(map_rows).sort_values(by="FREQUENCIA", ascending=False)

map_df.to_csv("mapa_de_correcao_servicos.csv", index=False, encoding='utf-8-sig')

# --- RESULTADOS E SAÍDA ---
# Exibir as 20 correções mais comuns no terminal
print("\n--- 20 principais termos originais e para o que foram padronizados ---\n")
print(map_df.head(20).to_string(index=False))

# Salvar DataFrame tratado em novo Excel
saida = "Planilha_tratada.xlsx"
df.to_excel(saida, index=False)

print(f"\nArquivo tratado salvo em: {saida}")
print("Mapa de correção salvo em: mapa_de_correcao_servicos.csv")

# Opcional: mostrar a contagem dos serviços padronizados
print("\n--- Contagem de SERVIÇO padronizado ---\n")
print(df["SERVICO_PADRONIZADO_TITULO"].value_counts().to_string())
