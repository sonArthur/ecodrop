"""
Conteúdo do modo Lixo Eletrônico.

Este módulo centraliza:
- Categorias de destinação.
- Equipamentos e resíduos disponíveis.
- Categoria correta de cada item.
- Explicações educativas.

Cada categoria possui 8 itens para manter a distribuição
equilibrada durante as partidas.
"""


# ==================================================
# CATEGORIAS DE DESTINAÇÃO
# ==================================================

# IMPORTANTE:
# Os identificadores internos foram preservados para
# manter a compatibilidade com o restante do jogo.

ELECTRONIC_CATEGORIES = [
    (
        "reutilizar",
        "REUTILIZAR",
        (46, 160, 105),
    ),
    (
        "reparar",
        "REPARAR",
        (65, 145, 210),
    ),
    (
        "eletronicos",
        "ELETRÔNICOS",
        (150, 110, 195),
    ),
    (
        "pilhas_baterias",
        "PILHAS/BAT.",
        (225, 170, 45),
    ),
]


# ==================================================
# ITENS DO MODO
# ==================================================

# Cada item possui:
# 1. Nome apresentado ao jogador.
# 2. Categoria correta.
# 3. Explicação educativa apresentada durante a partida.


ELECTRONIC_ITEMS = [

    # ----------------------------------------------
    # REUTILIZAÇÃO
    # ----------------------------------------------

    (
        "Celular funcionando",
        "reutilizar",
        "Um aparelho funcional pode ser reutilizado ou doado. "
        "Antes da entrega, proteja seus dados pessoais.",
    ),

    (
        "Notebook funcionando",
        "reutilizar",
        "Equipamentos em boas condições podem ganhar "
        "uma nova vida por meio do reaproveitamento.",
    ),

    (
        "Teclado funcionando",
        "reutilizar",
        "Um teclado em boas condições pode continuar "
        "sendo utilizado ou ser doado.",
    ),

    (
        "Mouse funcionando",
        "reutilizar",
        "Periféricos funcionais podem ser reaproveitados "
        "por outras pessoas.",
    ),

    (
        "Monitor funcionando",
        "reutilizar",
        "Um monitor em boas condições pode continuar "
        "sendo utilizado por bastante tempo.",
    ),

    (
        "Carregador funcionando",
        "reutilizar",
        "Carregadores em boas condições podem ser "
        "reutilizados quando forem compatíveis com o aparelho.",
    ),

    (
        "Cabo USB funcionando",
        "reutilizar",
        "Cabos em boas condições podem continuar "
        "sendo utilizados ou doados.",
    ),

    (
        "Tablet funcionando",
        "reutilizar",
        "Tablets funcionais podem ser reutilizados, "
        "doados ou encaminhados para reaproveitamento.",
    ),


    # ----------------------------------------------
    # REPARO
    # ----------------------------------------------

    (
        "Notebook com defeito",
        "reparar",
        "Uma avaliação técnica pode identificar a "
        "possibilidade de conserto.",
    ),

    (
        "Teclado com falhas",
        "reparar",
        "O reparo pode prolongar a vida útil de "
        "periféricos de informática.",
    ),

    (
        "Monitor com cabo solto",
        "reparar",
        "Antes de descartar, avalie se o equipamento "
        "pode voltar a funcionar.",
    ),

    (
        "Celular com tela quebrada",
        "reparar",
        "Uma assistência técnica pode avaliar a "
        "possibilidade de substituição da tela.",
    ),

    (
        "Mouse com falhas",
        "reparar",
        "Um periférico com defeito pode ter componentes "
        "que permitem seu reparo.",
    ),

    (
        "Carregador com falha reparável",
        "reparar",
        "Uma avaliação especializada pode determinar "
        "se existe possibilidade segura de reparo.",
    ),

    (
        "Impressora com falha reparável",
        "reparar",
        "Antes de descartar uma impressora, avalie "
        "se o defeito pode ser corrigido.",
    ),

    (
        "Roteador com falha reparável",
        "reparar",
        "Equipamentos de rede podem ter sua vida útil "
        "prolongada por meio de reparos.",
    ),


    # ----------------------------------------------
    # COLETA DE RESÍDUOS ELETRÔNICOS
    # ----------------------------------------------

    (
        "Mouse sem conserto",
        "eletronicos",
        "Quando não existe possibilidade viável de reparo, "
        "o mouse deve ser encaminhado à coleta de eletrônicos.",
    ),

    (
        "Monitor sem reparo",
        "eletronicos",
        "Monitores sem possibilidade de recuperação devem "
        "seguir o sistema de coleta de eletroeletrônicos.",
    ),

    (
        "Carregador sem conserto",
        "eletronicos",
        "Carregadores sem possibilidade de reaproveitamento "
        "devem ser entregues em pontos de coleta apropriados.",
    ),

    (
        "Cabo USB sem conserto",
        "eletronicos",
        "Cabos danificados que não podem ser recuperados "
        "também fazem parte dos resíduos eletrônicos.",
    ),

    (
        "Placa eletrônica",
        "eletronicos",
        "Componentes eletrônicos devem receber "
        "destinação ambientalmente adequada.",
    ),

    (
        "Celular sem conserto",
        "eletronicos",
        "Celulares sem possibilidade de recuperação devem "
        "ser encaminhados à logística reversa.",
    ),

    (
        "Notebook sem conserto",
        "eletronicos",
        "Notebooks sem possibilidade de reaproveitamento "
        "devem ser encaminhados à coleta especializada.",
    ),

    (
        "Teclado sem conserto",
        "eletronicos",
        "Teclados sem condições de reparo devem receber "
        "destinação adequada como resíduos eletrônicos.",
    ),


    # ----------------------------------------------
    # PILHAS E BATERIAS
    # ----------------------------------------------

    (
        "Pilha AA usada",
        "pilhas_baterias",
        "Pilhas usadas devem ser entregues em "
        "pontos de coleta que recebem esse material.",
    ),

    (
        "Pilha AAA usada",
        "pilhas_baterias",
        "Pilhas AAA também precisam de destinação "
        "adequada e não devem ir para o lixo comum.",
    ),

    (
        "Pilha botão usada",
        "pilhas_baterias",
        "Pilhas pequenas utilizadas em relógios e "
        "outros equipamentos precisam de coleta específica.",
    ),

    (
        "Bateria de celular usada",
        "pilhas_baterias",
        "Baterias de celulares devem seguir os sistemas "
        "específicos de recebimento e destinação.",
    ),

    (
        "Bateria de notebook usada",
        "pilhas_baterias",
        "Baterias de notebooks também precisam "
        "de destinação apropriada.",
    ),

    (
        "Bateria recarregável usada",
        "pilhas_baterias",
        "Baterias recarregáveis devem ser encaminhadas "
        "a pontos de coleta apropriados.",
    ),

    (
        "Bateria de tablet usada",
        "pilhas_baterias",
        "Baterias de tablets devem ser destinadas "
        "por meio de sistemas adequados de coleta.",
    ),

    (
        "Bateria externa usada (power bank)",
        "pilhas_baterias",
        "Power banks possuem baterias internas e devem "
        "ser encaminhados a pontos de recebimento adequados.",
    ),
]


# ==================================================
# DADOS PARA O SISTEMA DO JOGO
# ==================================================

# O WasteItem e o game.py utilizam somente:
# nome e categoria.
#
# Por isso, transformamos os dados acima no formato:
#
# (nome, categoria)
#
# Mantemos a mesma estrutura utilizada anteriormente
# para não precisar modificar o game.py.

ELECTRONIC_WASTE_TYPES = [
    (name, category)
    for name, category, tip in ELECTRONIC_ITEMS
]


# ==================================================
# DICAS EDUCATIVAS
# ==================================================

# Relaciona o nome de cada item à sua explicação.

ELECTRONIC_TIPS = {
    name: tip
    for name, category, tip in ELECTRONIC_ITEMS
}


def get_electronic_tip(item_name: str) -> str:
    """
    Retorna a explicação educativa correspondente ao item.

    Parâmetro:
        item_name: nome do resíduo apresentado no jogo.

    Retorno:
        Explicação educativa ou mensagem genérica
        caso o item não seja encontrado.
    """

    return ELECTRONIC_TIPS.get(
        item_name,
        "Procure uma destinação ambientalmente adequada.",
    )
