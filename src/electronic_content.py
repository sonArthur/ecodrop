"""
Conteúdo do modo Lixo Eletrônico.

Este módulo centraliza:
- Categorias de destinação.
- Equipamentos e resíduos disponíveis.
- Categoria correta de cada item.
- Explicações educativas.
"""


# ==================================================
# CATEGORIAS DE DESTINAÇÃO
# ==================================================

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
# nome, categoria e explicação educativa.

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

    # ----------------------------------------------
    # COLETA DE ELETRÔNICOS
    # ----------------------------------------------

    (
        "Mouse sem funcionar",
        "eletronicos",
        "Periféricos sem possibilidade de uso devem "
        "ser encaminhados à coleta de eletrônicos.",
    ),

    (
        "Monitor sem reparo",
        "eletronicos",
        "Monitores devem seguir o sistema de "
        "logística reversa de eletroeletrônicos.",
    ),

    (
        "Carregador danificado",
        "eletronicos",
        "Carregadores devem ser entregues em pontos "
        "de recebimento de eletroeletrônicos.",
    ),

    (
        "Cabo USB sem uso",
        "eletronicos",
        "Cabos e acessórios também fazem parte dos "
        "resíduos eletroeletrônicos.",
    ),

    (
        "Placa eletrônica",
        "eletronicos",
        "Componentes eletrônicos devem receber "
        "destinação ambientalmente adequada.",
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
        "Bateria de celular usada",
        "pilhas_baterias",
        "Baterias devem seguir os sistemas "
        "específicos de recebimento e destinação.",
    ),

    (
        "Bateria de notebook usada",
        "pilhas_baterias",
        "Baterias de notebooks também precisam "
        "de destinação apropriada.",
    ),
]


# ==================================================
# DADOS PARA O SISTEMA DO JOGO
# ==================================================

# O WasteItem utiliza somente nome e categoria.
# Por isso, criamos uma lista no formato esperado.

ELECTRONIC_WASTE_TYPES = [
    (name, category)
    for name, category, tip in ELECTRONIC_ITEMS
]


# ==================================================
# DICAS EDUCATIVAS
# ==================================================

ELECTRONIC_TIPS = {
    name: tip
    for name, category, tip in ELECTRONIC_ITEMS
}


def get_electronic_tip(item_name: str) -> str:
    """
    Retorna a explicação educativa de um item.

    Caso o nome não seja encontrado, retorna
    uma mensagem genérica.
    """

    return ELECTRONIC_TIPS.get(
        item_name,
        "Procure uma destinação ambientalmente adequada.",
    )
