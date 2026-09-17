import requests
import pandas as pd
from func_list_prod import obter_codigos

# PARÂMETROS
TABELA = {
    7062: 'IPCA15 - Variação mensal, acumulada no ano, acumulada em 12 meses e peso mensal, para o índice geral, grupos, subgrupos, itens e subitens de produtos e serviços (a partir de fevereiro/2020)'
}

VARIAVEIS = {
    355: 'IPCA15 - Variação mensal',
    356: 'IPCA15 - Variação acumulada no ano',
    1120: 'IPCA15 - Variação acumulada em 12 meses'
}

C315 = obter_codigos('ibge') # Produtos
PERIODOS = -12
LOCALIDADES = 'N7'

def api_ibge_agregados(tabela, periodos, variaveis, localidades):
    url = (
        f"https://servicodados.ibge.gov.br/api/v3"
        f"/agregados/{tabela}"
        f"/periodos/{periodos}"
        f"/variaveis/{'|'.join(str(v) for v in variaveis)}"
        f"?localidades={localidades}"
        f"&classificacao=315[{','.join(str(codigo) for codigo in C315.values())}]"
    )
    response = requests.get(url)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        return None
    else:
        dados = response.json()
        tabela = TABELA.keys()
        variaveis = {v: VARIAVEIS[v] for v in variaveis}
        return dados

def extrair_dados(res):
    registros = []

    for variavel in res:
        for resultado in variavel['resultados']:
            categoria = resultado['classificacoes'][0]['categoria']
            produto = next(iter(categoria.values())).split('.', 1)[-1]

            for serie in resultado['series']:
                localidade = serie['localidade']['nome']
                for periodo, valor in serie['serie'].items():
                    registros.append({
                        'Produto': produto,
                        'Localidade': localidade,
                        'Variável': variavel['variavel'],
                        'Período': periodo,
                        'Valor': pd.to_numeric(valor, errors='coerce'),
                    })

    return pd.DataFrame(registros)

try:
    res = api_ibge_agregados(7062, PERIODOS, VARIAVEIS.keys(), LOCALIDADES)
    if res is None:
        raise RuntimeError('A API não retornou dados.')

    dados = extrair_dados(res)
    mensal = dados[
        (dados['Variável'] == 'IPCA15 - Variação mensal')
        & dados['Produto'].ne('')
    ]
    tabela_mensal = mensal.pivot(
        index=['Localidade', 'Produto'],
        columns='Período',
        values='Valor'
    )
    tabela_mensal = tabela_mensal.sort_index(axis=1)

    periodo_final = dados['Período'].max()
    acumulados = dados[
        dados['Variável'].isin([
            'IPCA15 - Variação acumulada no ano',
            'IPCA15 - Variação acumulada em 12 meses'
        ])
        & (dados['Período'] == periodo_final)
        & dados['Produto'].ne('')
    ].pivot(
        index=['Localidade', 'Produto'],
        columns='Variável',
        values='Valor'
    ).rename(columns={
        'IPCA15 - Variação acumulada no ano': 'Acumulado no ano',
        'IPCA15 - Variação acumulada em 12 meses': 'Acumulado 12 meses'
    })

    ordem_acumulados = ['Acumulado no ano', 'Acumulado 12 meses']
    tabela_final = tabela_mensal.join(
        acumulados.reindex(columns=ordem_acumulados),
        how='left'
    ).fillna(0)
    print(tabela_final.to_string())

    
except Exception as e:
    print(f"Erro ao processar os dados: {e}")