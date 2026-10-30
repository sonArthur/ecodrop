"""
Conteúdo educativo do EcoDrop.

Este módulo reúne dicas curtas sobre os resíduos
apresentados durante as partidas.

As informações são educativas e gerais. A aceitação
dos materiais pode variar conforme a coleta local.
"""


# Dicas associadas aos nomes dos resíduos do jogo.
EDUCATIONAL_TIPS: dict[str, str] = {
    "Jornal": (
        "Papel para reciclagem deve ficar seco."
    ),

    "Caixa de papelão": (
        "Desmonte a caixa para economizar espaço."
    ),

    "Garrafa PET": (
        "Garrafas PET são exemplos de plástico reciclável."
    ),

    "Pote plástico": (
        "Embalagens vazias e limpas facilitam a reciclagem."
    ),

    "Garrafa de vidro": (
        "Garrafas são exemplos de vidro reciclável."
    ),

    "Pote de vidro": (
        "Potes de alimentos podem ser recicláveis."
    ),

    "Lata de alumínio": (
        "Latas de alumínio são materiais recicláveis."
    ),

    "Lata de conserva": (
        "Latas de alimentos podem ser recicladas."
    ),

    "Casca de banana": (
        "Resíduos orgânicos podem ser compostados."
    ),

    "Restos de frutas": (
        "Restos de frutas podem virar composto orgânico."
    ),
}


def get_education_tip(item_name: str) -> str:
    """
    Retorna uma dica educativa para o resíduo informado.

    Args:
        item_name: nome do resíduo exibido no jogo.

    Returns:
        Uma dica correspondente ao resíduo ou uma
        mensagem genérica caso ele não esteja cadastrado.
    """

    return EDUCATIONAL_TIPS.get(
        item_name,
        "Separe os resíduos e consulte as regras locais.",
    )
