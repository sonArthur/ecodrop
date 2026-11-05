"""
Sistema de recordes do EcoDrop.

Responsabilidades:
- Carregar o recorde salvo em disco.
- Comparar a pontuação atual com o recorde.
- Salvar uma nova pontuação máxima.
- Migrar os dados antigos para AppData.
- Tratar problemas de leitura e gravação sem
  impedir a execução do jogo.
"""

import json
from pathlib import Path

from src.settings_manager import get_user_data_dir


class RecordManager:
    """
    Gerencia o recorde geral de pontuação do EcoDrop.

    Os dados são armazenados em:
    %APPDATA%/EcoDrop/record.json
    """

    def __init__(self) -> None:
        """Inicializa o gerenciador e carrega o recorde."""

        # Local antigo utilizado durante o desenvolvimento.
        project_root = Path(__file__).resolve().parent.parent

        self.legacy_path = (
            project_root
            / "data"
            / "record.json"
        )

        # Novo local permanente no Windows.
        self.file_path = (
            get_user_data_dir()
            / "record.json"
        )

        # Carrega o recorde existente ou inicia em zero.
        self.best_score = self._load_record()

    def _read_record(self, path: Path) -> int:
        """
        Lê um recorde de determinado arquivo.

        Retorna zero se o arquivo não existir ou
        apresentar dados inválidos.
        """

        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)

            if not isinstance(data, dict):
                return 0

            score = data.get("best_score", 0)

            if (
                isinstance(score, bool)
                or not isinstance(score, int)
                or score < 0
            ):
                return 0

            return score

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

    def _load_record(self) -> int:
        """
        Carrega o recorde.

        Se ainda não existir um arquivo no AppData,
        tenta recuperar o recorde antigo da pasta data/.
        """

        if self.file_path.exists():
            return self._read_record(self.file_path)

        if self.legacy_path.is_file():

            legacy_score = self._read_record(
                self.legacy_path
            )

            # Migra o recorde sem apagar o arquivo antigo.
            self.best_score = legacy_score
            self._save_record()

            return legacy_score

        return 0

    def _save_record(self) -> bool:
        """Salva o recorde de forma atômica."""

        temporary_path = self.file_path.with_suffix(
            ".tmp"
        )

        data = {
            "best_score": self.best_score
        }

        try:

            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            temporary_path.write_text(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            temporary_path.replace(self.file_path)

            return True

        except OSError as error:

            print(
                "Aviso: não foi possível salvar "
                f"o recorde: {error}"
            )

            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass

            return False

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

        # Persiste a nova pontuação.
        self._save_record()

        return True
