"""Estatísticas persistentes das partidas do EcoDrop.

Os resultados são armazenados separadamente para cada modalidade
em %APPDATA%/EcoDrop/statistics.json.

Apenas partidas concluídas são contabilizadas.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.settings_manager import get_user_data_dir


VALID_MODES = ("general", "electronic")


class StatisticsManager:
    """Registra e consulta o desempenho acumulado em cada modo."""

    def __init__(self, storage_path: str | Path | None = None) -> None:

        project_root = Path(__file__).resolve().parent.parent

        # Local utilizado durante o desenvolvimento.
        self.legacy_path = (
            project_root / "data" / "statistics.json"
        )

        if storage_path is not None:
            self.storage_path = Path(storage_path)
            self.migrate_legacy = False
        else:
            self.storage_path = (
                get_user_data_dir() / "statistics.json"
            )
            self.migrate_legacy = True

        self.data = self._load()

    @staticmethod
    def _default_mode_stats() -> dict[str, int]:
        return {
            "games_played": 0,
            "best_score": 0,
            "correct_classifications": 0,
            "incorrect_classifications": 0,
        }

    @classmethod
    def _default_data(cls) -> dict[str, Any]:
        return {
            "version": 1,
            "modes": {
                mode: cls._default_mode_stats()
                for mode in VALID_MODES
            },
        }

    @classmethod
    def _normalize_counter(cls, value: Any) -> int:
        """Aceita somente contadores inteiros e não negativos."""

        if isinstance(value, bool) or not isinstance(value, int):
            return 0

        return max(0, value)

    @classmethod
    def _normalize_data(cls, loaded: Any) -> dict[str, Any]:
        """Valida os dados carregados e mantém o formato esperado."""

        normalized = cls._default_data()

        if not isinstance(loaded, dict):
            return normalized

        stored_modes = loaded.get("modes", {})

        if not isinstance(stored_modes, dict):
            return normalized

        for mode in VALID_MODES:

            mode_data = stored_modes.get(mode, {})

            if not isinstance(mode_data, dict):
                continue

            for key in normalized["modes"][mode]:

                normalized["modes"][mode][key] = (
                    cls._normalize_counter(
                        mode_data.get(key, 0)
                    )
                )

        return normalized

    def _load(self) -> dict[str, Any]:
        """
        Carrega as estatísticas.

        Caso ainda não exista um arquivo no AppData, tenta migrar
        automaticamente o arquivo antigo da pasta data/.
        """

        source_path = self.storage_path

        if (
            not source_path.exists()
            and self.migrate_legacy
            and self.legacy_path.is_file()
        ):
            source_path = self.legacy_path

        if not source_path.exists():
            return self._default_data()

        try:

            loaded = json.loads(
                source_path.read_text(encoding="utf-8")
            )

        except (
            OSError,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ):

            return self._default_data()

        normalized = self._normalize_data(loaded)

        # Migra os dados antigos sem apagar o arquivo original.
        if source_path == self.legacy_path:

            self.data = normalized

            self._save()

        return normalized

    def _save(self) -> bool:
        """Salva os dados de forma atômica."""

        temporary_path = self.storage_path.with_suffix(
            self.storage_path.suffix + ".tmp"
        )

        try:

            self.storage_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            temporary_path.write_text(
                json.dumps(
                    self.data,
                    ensure_ascii=False,
                    indent=4,
                ) + "\n",
                encoding="utf-8",
            )

            temporary_path.replace(self.storage_path)

            return True

        except OSError as error:

            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass

            print(
                "Aviso: não foi possível salvar as estatísticas: "
                f"{error}"
            )

            return False

    def record_completed_game(
        self,
        mode: str,
        score: int,
        correct: int,
        incorrect: int,
    ) -> bool:
        """Registra o resultado de uma partida concluída."""

        if mode not in VALID_MODES:
            raise ValueError(
                f"Modalidade inválida: {mode!r}. "
                "Use 'general' ou 'electronic'."
            )

        values = (score, correct, incorrect)

        if any(
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 0
            for value in values
        ):
            raise ValueError(
                "Pontuação e classificações devem ser "
                "inteiros não negativos."
            )

        mode_stats = self.data["modes"][mode]

        mode_stats["games_played"] += 1

        mode_stats["best_score"] = max(
            mode_stats["best_score"],
            score,
        )

        mode_stats["correct_classifications"] += correct

        mode_stats["incorrect_classifications"] += incorrect

        return self._save()

    def get_mode_stats(
        self,
        mode: str,
    ) -> dict[str, int | float]:
        """Retorna estatísticas de um modo e calcula o aproveitamento."""

        if mode not in VALID_MODES:
            raise ValueError(
                f"Modalidade inválida: {mode!r}. "
                "Use 'general' ou 'electronic'."
            )

        stored = self.data["modes"][mode]

        correct = stored["correct_classifications"]
        incorrect = stored["incorrect_classifications"]

        total = correct + incorrect

        accuracy = (
            correct / total * 100.0
            if total
            else 0.0
        )

        return {
            **stored,
            "total_classifications": total,
            "accuracy_rate": accuracy,
        }
