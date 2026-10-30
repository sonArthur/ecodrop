"""
Definições dos modos de jogo do EcoDrop.

Este módulo centraliza os identificadores e as informações
exibidas na tela de seleção dos modos.
"""

# Identificadores internos dos modos.
MODE_GENERAL = "general"
MODE_ELECTRONIC = "electronic"


# Informações apresentadas ao jogador.
GAME_MODES = {
    MODE_GENERAL: {
        "title": "RECICLAGEM GERAL",
        "status": "DISPONÍVEL",
        "description": [
            "Separe cinco categorias de resíduos.",
            "Acumule pontos e aumente seu combo.",
        ],
    },

    MODE_ELECTRONIC: {
        "title": "LIXO ELETRÔNICO",
        "status": "Disponivel",
        "description": [
            "Conheça o destino de equipamentos de TI.",
            "Aprenda sobre reparo e logística reversa.",
        ],
    },
}
