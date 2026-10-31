"""Perguntas educativas do modo Lixo Eletrônico.

Cada pergunta contém três alternativas, o índice da resposta correta
(equivale à posição na lista, começando em zero) e uma explicação.
"""

QUIZ_QUESTIONS = [
    {
        "id": "dados_celular",
        "question": "Antes de doar ou encaminhar um celular, o que fazer?",
        "options": [
            "Deixar as contas conectadas",
            "Proteger os dados e sair das contas",
            "Jogar o aparelho no lixo comum",
        ],
        "correct_index": 1,
        "explanation": (
            "Faça backup do que deseja guardar, saia das contas e apague "
            "seus dados pessoais antes de entregar o aparelho."
        ),
    },
    {
        "id": "pilhas_baterias",
        "question": "Onde devem ser entregues pilhas e baterias usadas?",
        "options": [
            "Em pontos de coleta que aceitem esse material",
            "Junto com restos de comida",
            "Em qualquer lixeira de recicláveis",
        ],
        "correct_index": 0,
        "explanation": (
            "Pilhas e baterias precisam de coleta apropriada. Procure um "
            "ponto de recebimento que aceite esse tipo de resíduo."
        ),
    },
    {
        "id": "reutilizacao",
        "question": "Um notebook antigo ainda funciona bem. Qual é uma boa opção?",
        "options": [
            "Descartá-lo imediatamente",
            "Misturá-lo ao lixo orgânico",
            "Reutilizá-lo ou doá-lo com segurança",
        ],
        "correct_index": 2,
        "explanation": (
            "A reutilização prolonga a vida útil do equipamento e pode "
            "evitar que um aparelho funcional vire resíduo antes da hora."
        ),
    },
    {
        "id": "reparo",
        "question": "Um aparelho apresenta defeito. O que considerar primeiro?",
        "options": [
            "Avaliar se o reparo é possível",
            "Quebrá-lo para ocupar menos espaço",
            "Descartá-lo em uma lixeira comum",
        ],
        "correct_index": 0,
        "explanation": (
            "Uma avaliação técnica pode indicar se o conserto é viável e "
            "se o equipamento pode continuar em uso."
        ),
    },
    {
        "id": "logistica_reversa",
        "question": "O que busca a logística reversa de eletrônicos?",
        "options": [
            "Aumentar o descarte no lixo comum",
            "Fazer o produto retornar a uma cadeia de coleta e destinação",
            "Impedir o reaproveitamento de materiais",
        ],
        "correct_index": 1,
        "explanation": (
            "A logística reversa organiza o retorno dos produtos após o uso "
            "para que tenham reaproveitamento ou destinação adequada."
        ),
    },
    {
        "id": "acessorios",
        "question": "O que fazer com cabos e carregadores sem uso?",
        "options": [
            "Queimá-los para reduzir o volume",
            "Deixá-los na rua",
            "Levá-los a um ponto que receba eletroeletrônicos",
        ],
        "correct_index": 2,
        "explanation": (
            "Cabos e carregadores também são resíduos eletroeletrônicos. "
            "Confira os materiais aceitos pelo ponto de recebimento."
        ),
    },
]
