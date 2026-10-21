# Função de tabela central de correspondência de produtos entre IBGE e SEAB

PRODUTOS = {
    "Arroz": {"ibge": 7173, "seab": None},
    "Carnes": {"ibge": 7283, "seab": None},
    "Fígado": {"ibge": 7285, "seab": None},
    "Carne de porco": {"ibge": 7287, "seab": None},
    "Contrafilé": {"ibge": 7291, "seab": None},
    "Alcatra": {"ibge": 7294, "seab": None},
    "Costela": {"ibge": 7302, "seab": None},
    "Picanha": {"ibge": 47621, "seab": None},
    "Presunto": {"ibge": 7336, "seab": None},
    "Salsicha": {"ibge": 12304, "seab": None},
    "Linguiça": {"ibge": 7339, "seab": None},
    "Mortadela": {"ibge": 7341, "seab": None},
    "Salame": {"ibge": 12305, "seab": None},
    "Carne de porco salgada e defumada": {"ibge": 7347, "seab": None},
    "Aves e ovos": {"ibge": 7349, "seab": None},
    "Frango inteiro": {"ibge": 107617, "seab": None},
    "Frango em pedaços": {"ibge": 107618, "seab": None},
    "Ovo de galinha": {"ibge": 7355, "seab": None},
    "Combustíveis (veículos)": {"ibge": 7656, "seab": None},
    "Gasolina": {"ibge": 7657, "seab": None},
    "Etanol": {"ibge": 7658, "seab": None},
    "Óleo diesel": {"ibge": 7659, "seab": None},
}

def obter_codigos(origem):
    return {
        produto: dados[origem.lower()]
        for produto, dados in PRODUTOS.items()
        if origem.lower() in dados
    }