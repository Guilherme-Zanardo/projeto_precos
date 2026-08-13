# BIBLIOTECA
import requests
import pandas as pd
from pathlib import Path
from func_list_prod import obter_codigos

# IPCA-15 PRÉVIA - API SIDRA -> resultado

# PARÂMETROS
P = "last 13"
C315 = obter_codigos('ibge')

V = {
  "IPCA - Variação mensal": 355,
  "IPCA - Variação acumulada no ano": 356,
  "IPCA - Variação acumulada em 12 meses": 1120,
  # "IPCA - Peso mensal": 357,
}

NOMES = {
    "IPCA - Variação mensal": "Mensal",
    "IPCA - Variação acumulada no ano": "Acumulado ano",
    "IPCA - Variação acumulada em 12 meses": "12 meses",
}

# Tabela 1737: Série histórica com número-índice, variação mensal e acumuladas (3, 6, 12 meses e no ano) desde dezembro de 1979
# Tabela 7060: Variação mensal, acumulada no ano, em 12 meses e peso mensal por grupos, subgrupos e subitens (a partir de janeiro de 2020)
# Tabela 7061: Variação detalhada por subitem específico de produto ou serviço
# Tabela 7062: Prévia do IPCA (IPCA-15) por grupo

# GET
URL = f"https://apisidra.ibge.gov.br/values/t/7062/n1/all/v/{','.join(str(codigo) for codigo in V.values())}/p/{P}/c315/{','.join(str(codigo) for codigo in C315.values())}"
response = requests.get(URL)

try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Erro no request: {e}")
    resultado = None
else:
    resultado = response.json()
    legenda = resultado[0]
    dados = resultado[1:]

# TABELA MATRIZ TEMPORAL

df = pd.DataFrame(dados)
df["Produto"] = df["D4N"].str.split(".", n=1).str[-1] # Nome do produto
df["Valor"] = pd.to_numeric(df["V"], errors="coerce") # Valor númerico
periodo = df["D3N"].iloc[0]
# df[["Produto", "D2N", "D3N", "Valor"]] # Tabela antes do Pivot

# MENSAL
mensal = df[df["D2N"] == "IPCA15 - Variação mensal"]

tabela_meses = (
    mensal.pivot_table(
        index="Produto",
        columns="D3N",
        values="Valor",
        aggfunc="first"
    )
)

# Ordena os meses
ordem_periodos = (
    mensal[["D3C", "D3N"]]
    .drop_duplicates()
    .sort_values("D3C")["D3N"]
    .tolist()
)

tabela_meses = tabela_meses.reindex(columns=ordem_periodos)

# ÚLTIMO
ultimo_periodo = df["D3C"].max()

acumulados = (
    df[df["D3C"] == ultimo_periodo]
    .pivot_table(
        index="Produto",
        columns="D2N",
        values="Valor",
        aggfunc="first"
    )
)

acumulados = acumulados.rename(columns={
    "IPCA15 - Variação acumulada no ano": "Acumulado",
    "IPCA15 - Variação acumulada em 12 meses": "12 meses",
})

colunas_existentes = [
    c for c in ["Acumulado", "12 meses"]
    if c in acumulados.columns
]

matriz_temporal = (
    tabela_meses
    .join(acumulados[colunas_existentes], how="left")
    .reset_index()
).map(lambda x: f"{x:.2f}%" if isinstance(x, (int, float)) else x)


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
matriz_temporal =pd.DataFrame(matriz_temporal)
print(f"=========================================================================================================================================================")
print(matriz_temporal)
print(f"=========================================================================================================================================================")

# EXPORT EXCEL
# caminho_arquivo = Path(__file__).parent / "ipca-15.xlsx"
# matriz_temporal.to_excel(caminho_arquivo, index=False)