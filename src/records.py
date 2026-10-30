"""
Sistema de recordes do EcoDrop.

Responsabilidades:
- Carregar o recorde salvo em disco.
- Comparar a pontuação atual com o recorde.
- Salvar uma nova pontuação máxima.
- Tratar problemas de leitura e gravação sem
  impedir a execução do jogo.
"""

import json

from pathlib import Path


class RecordManager:
    """
    Gerencia o recorde de pontuação do EcoDrop.

    Os dados são armazenados em JSON na pasta data/.
    """

    def __init__(self) -> None:
        """
        Inicializa o gerenciador e carrega o recorde.
        """

        # Localiza a raiz do projeto a partir deste arquivo.
        project_root = Path(__file__).resolve().parent.parent

        # Caminho do arquivo que armazenará o recorde.
        self.file_path = (
            project_root
            / "data"
            / "record.json"
        )

        # Carrega o recorde existente ou inicia em zero.
        self.best_score = self._load_record()

    def _load_record(self) -> int:
        """
        Lê o recorde salvo no arquivo JSON.

        Returns:
            A maior pontuação salva ou zero, caso
            o arquivo ainda não exista ou seja inválido.
        """

        try:
            content = self.file_path.read_text(
                encoding="utf-8"
            )

            data = json.loads(content)

            score = data.get(
                "best_score",
                0
            )

            # Evita aceitar valores negativos, textos
            # ou booleanos como pontuações válidas.
            if (
                isinstance(score, bool)
                or not isinstance(score, int)
                or score < 0
            ):
                return 0

            return score

        except FileNotFoundError:
            # Primeira execução: ainda não existe recorde.
            return 0

        except (
            json.JSONDecodeError,
            OSError,
            AttributeError,
            TypeError,
            ValueError,
        ) as error:

            print(
                "Aviso: não foi possível carregar "
                f"o recorde: {error}"
            )

            return 0

    def update(self, score: int) -> bool:
        """
        Atualiza o recorde quando a pontuação for maior.

        Args:
            score: pontuação obtida pelo jogador.

        Returns:
            True se a pontuação estabeleceu um novo
            recorde durante a execução atual; False
            caso contrário.
        """

        # Não aceita pontuações inválidas.
        if (
            isinstance(score, bool)
            or not isinstance(score, int)
            or score < 0
        ):
            return False

        # Só grava quando a pontuação supera o recorde.
        if score <= self.best_score:
            return False

        # Atualiza o recorde em memória.
        self.best_score = score

        try:
            # Cria a pasta de dados se necessário.
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Grava primeiro em um arquivo temporário.
            # Depois substitui o arquivo do recorde.
            temporary_path = self.file_path.with_suffix(
                ".tmp"
            )

            data = {
                "best_score": self.best_score
            }

            temporary_path.write_text(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

            temporary_path.replace(
                self.file_path
            )

        except OSError as error:

            # O jogo continua funcionando mesmo se não
            # conseguir gravar o arquivo no computador.
            print(
                "Aviso: não foi possível salvar "
                f"o recorde: {error}"
            )

        return True
