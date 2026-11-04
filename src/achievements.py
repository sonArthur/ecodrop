"""Gerenciamento persistente das conquistas do EcoDrop.

As conquistas são salvas localmente em data/achievements.json.
O progresso desse sistema é independente da pontuação do questionário.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ACHIEVEMENT_DEFINITIONS = [
    {
        "id": "primeiros_passos",
        "title": "Primeiros Passos",
        "description": "Classifique corretamente 10 resíduos ao longo das partidas.",
        "target": 10,
    },
    {
        "id": "combo_de_ouro",
        "title": "Combo de Ouro",
        "description": "Alcance uma sequência de 5 classificações corretas.",
        "target": 5,
    },
    {
        "id": "mestre_da_reciclagem",
        "title": "Mestre da Reciclagem",
        "description": "Faça 1.000 pontos ou mais em uma única partida.",
        "target": 1000,
    },
    {
        "id": "especialista_eletronicos",
        "title": "Especialista em Eletrônicos",
        "description": "Conclua todas as perguntas do desafio de conhecimento.",
        "target": 1,
    },
]


class AchievementManager:
    """Registra, desbloqueia e consulta as conquistas do jogador."""

    def __init__(self, storage_path: str | Path | None = None) -> None:
        project_root = Path(__file__).resolve().parent.parent
        self.storage_path = (
            Path(storage_path)
            if storage_path is not None
            else project_root / "data" / "achievements.json"
        )

        self.data: dict[str, Any] = self._load()

    @staticmethod
    def _default_data() -> dict[str, Any]:
        return {
            "correct_classifications": 0,
            "best_combo": 0,
            "best_round_score": 0,
            "quiz_completed": False,
            "unlocked": {},
        }

    def _load(self) -> dict[str, Any]:
        """Carrega os dados e recupera valores padrão se o arquivo não existir."""

        if not self.storage_path.exists():
            return self._default_data()

        try:
            loaded = json.loads(self.storage_path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                return self._default_data()

            data = self._default_data()
            data["correct_classifications"] = max(
                0, int(loaded.get("correct_classifications", 0))
            )
            data["best_combo"] = max(0, int(loaded.get("best_combo", 0)))
            data["best_round_score"] = max(
                0, int(loaded.get("best_round_score", 0))
            )
            data["quiz_completed"] = bool(loaded.get("quiz_completed", False))

            unlocked = loaded.get("unlocked", {})
            if isinstance(unlocked, dict):
                valid_ids = {item["id"] for item in ACHIEVEMENT_DEFINITIONS}
                data["unlocked"] = {
                    key: value
                    for key, value in unlocked.items()
                    if key in valid_ids and isinstance(value, str)
                }

            return data

        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            # Um arquivo inválido não deve impedir a inicialização do jogo.
            return self._default_data()

    def _save(self) -> bool:
        """Salva atomicamente para reduzir o risco de arquivo incompleto."""

        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path = self.storage_path.with_suffix(".tmp")
            temporary_path.write_text(
                json.dumps(self.data, ensure_ascii=False, indent=4),
                encoding="utf-8",
            )
            temporary_path.replace(self.storage_path)
            return True
        except OSError as error:
            print(f"Não foi possível salvar as conquistas: {error}")
            return False

    def _unlock(self, achievement_id: str, newly_unlocked: list[str]) -> None:
        """Desbloqueia uma conquista apenas uma vez."""

        if achievement_id in self.data["unlocked"]:
            return

        self.data["unlocked"][achievement_id] = (
            datetime.now().astimezone().isoformat(timespec="seconds")
        )
        newly_unlocked.append(achievement_id)

    def record_correct_classification(self, combo: int, score: int) -> list[dict[str, str]]:
        """Atualiza estatísticas após um acerto e devolve novos desbloqueios."""

        self.data["correct_classifications"] += 1
        self.data["best_combo"] = max(self.data["best_combo"], int(combo))
        self.data["best_round_score"] = max(
            self.data["best_round_score"], int(score)
        )

        newly_unlocked_ids: list[str] = []

        if self.data["correct_classifications"] >= 10:
            self._unlock("primeiros_passos", newly_unlocked_ids)

        if self.data["best_combo"] >= 5:
            self._unlock("combo_de_ouro", newly_unlocked_ids)

        if self.data["best_round_score"] >= 1000:
            self._unlock("mestre_da_reciclagem", newly_unlocked_ids)

        self._save()
        return self._format_new_unlocks(newly_unlocked_ids)

    def record_quiz_completed(self) -> bool:
        """Registra a conclusão integral do questionário opcional."""

        self.data["quiz_completed"] = True
        newly_unlocked_ids: list[str] = []
        self._unlock("especialista_eletronicos", newly_unlocked_ids)
        self._save()
        return bool(newly_unlocked_ids)

    @staticmethod
    def _format_new_unlocks(ids: list[str]) -> list[dict[str, str]]:
        definitions = {item["id"]: item for item in ACHIEVEMENT_DEFINITIONS}
        return [
            {"id": item_id, "title": definitions[item_id]["title"]}
            for item_id in ids
        ]

    @property
    def unlocked_count(self) -> int:
        return len(self.data["unlocked"])

    def get_achievement_cards(self) -> list[dict[str, Any]]:
        """Devolve os dados prontos para a tela de conquistas."""

        cards = []
        for definition in ACHIEVEMENT_DEFINITIONS:
            achievement_id = definition["id"]
            unlocked = achievement_id in self.data["unlocked"]

            if achievement_id == "primeiros_passos":
                progress = (
                    f"{min(self.data['correct_classifications'], 10)}/10 acertos"
                )
            elif achievement_id == "combo_de_ouro":
                progress = f"{min(self.data['best_combo'], 5)}/5 em sequência"
            elif achievement_id == "mestre_da_reciclagem":
                progress = f"{min(self.data['best_round_score'], 1000)}/1.000 pontos"
            else:
                progress = "Concluído" if self.data["quiz_completed"] else "Pendente"

            cards.append(
                {
                    **definition,
                    "unlocked": unlocked,
                    "progress": progress,
                }
            )

        return cards
