# BIBLIOTECA
import requests
import pandas as pd
from pathlib import Path
from func_list_prod import obter_codigos


# IPCA-15 PRÉVIA - API SIDRA -> resultado
# PARÂMETROS
P = "last 6"  # Mês
C315 = obter_codigos('ibge')  # Período

V = {
    "IPCA - Variação mensal": 355,
    "IPCA - Variação acumulada no ano": 356,
    "IPCA - Variação acumulada em 12 meses": 1120,
}

NOMES = {
    "IPCA - Variação mensal": "Mensal",
    "IPCA - Variação acumulada no ano": "Acumulado ano",
    "IPCA - Variação acumulada em 12 meses": "12 meses",
}

N71 = {
    "RM de Curitiba (PR)": 5501,
    "RM de São Paulo (SP)": 4901,
    "RM de Porto Alegre (RS)": 7401,
}

for n in N71.items(): # Iterar sobre os territórios - Gerar um print por território
    print(f'\n# TERRITÓRIO: {n[0].replace("RM de ", "")}')

    # GET
    URL = (
        f"https://apisidra.ibge.gov.br/values/t/7062"
        # f"/n1/all"
        f"/N71/{n[1]}"
        f"/v/{','.join(str(codigo) for codigo in V.values())}"
        f"/p/{P}"
        f"/c315/{','.join(str(codigo) for codigo in C315.values())}"
    )

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

        df["Produto"] = df["D4N"].str.split(".", n=1).str[-1]
        df["Território"] = df["D1N"].str.replace("RM de ", "", regex=False)
        df["Valor"] = pd.to_numeric(df["V"], errors="coerce")

        periodo = df["D3N"].iloc[0]

        # MENSAL
        mensal = df[df["D2N"] == "IPCA15 - Variação mensal"]

        tabela_meses = (
            mensal.pivot_table(
                index=["Território", "Produto"],
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
                index=["Território", "Produto"],
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
        )

        # Formatação dos valores
        matriz_temporal = matriz_temporal.map(
            lambda x: f"{x:.2f}%"
            if isinstance(x, (int, float))
            else x
        )

        # ORGANIZAÇÃO DAS COLUNAS
        matriz_temporal = matriz_temporal[
            ["Território", "Produto"]
            + ordem_periodos
            + colunas_existentes
        ]

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)

        matriz_temporal = pd.DataFrame(matriz_temporal)

        print("=" * 120)
        print(matriz_temporal)
        print("=" * 120)

        # EXPORT EXCEL
        # caminho_arquivo = Path(__file__).parent / "ipca-15.xlsx"
        # matriz_temporal.to_excel(caminho_arquivo, index=False)