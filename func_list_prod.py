# Função de tabela central de correspondência de produtos entre IBGE e SEAB

PRODUTOS = {
    "Acém": {"ibge": 7300, "seab": 1665},
    "Carne de porco": {"ibge": 7287, "seab": 1635},
    "Contrafilé": {"ibge": 7291, "seab": 1645},
    "Costela": {"ibge": 7302, "seab": 1673},
    "Filé-mignon": {"ibge": 7292, "seab": None},
    "Frango inteiro": {"ibge": 107617, "seab": 1789},
    "Linguiça": {"ibge": 7339, "seab": 1771},
    "Milho (em grão)": {"ibge": 47618, "seab": None},
    "Ovo de galinha": {"ibge": 7355, "seab": 1791},
    "Picanha": {"ibge": 47621, "seab": 1691},
    "Peixe - sardinha": {"ibge": 7310, "seab": None},
    # "Banha de porco": {"ibge": 101499, "seab": None}, # Não há registro de variação recente
}

def obter_codigos(origem):
    return {
        produto: dados[origem.lower()]
        for produto, dados in PRODUTOS.items()
        if origem.lower() in dados
    }