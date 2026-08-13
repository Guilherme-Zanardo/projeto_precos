# Função de tabela central de correspondência de produtos entre IBGE e SEAB

PRODUTOS = {
    "Ovo de galinha": {"ibge": 7355, "seab": 1791},
    "Contrafilé": {"ibge": 7291, "seab": 1645},
    "Acém": {"ibge": 7300, "seab": 1665},
    "Costela": {"ibge": 7302, "seab": 1673},
    "Carne de porco": {"ibge": 7287, "seab": 1635},
    "Linguiça": {"ibge": 7339, "seab": 1771},
    "Frango inteiro": {"ibge": 107617, "seab": 1789},
    "Sardinha": {"ibge": 7310, "seab": 1691},
    "Milho (em grão)": {"ibge": 47618, "seab": None}
}

def obter_codigos(origem):
    return {
        produto: dados[origem.lower()]
        for produto, dados in PRODUTOS.items()
        if origem.lower() in dados
    }