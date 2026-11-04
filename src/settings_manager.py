"""Persistência das preferências do jogador do EcoDrop."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS: dict[str, Any] = {
    "volume": 70,
    "sound_enabled": True,
    "show_education_tips": True,
    "fullscreen": False,
}


class SettingsManager:
    """Carrega, valida e salva as configurações em data/settings.json."""

    def __init__(self, file_path: str | Path = "data/settings.json") -> None:
        self.file_path = Path(file_path)
        self.values: dict[str, Any] = DEFAULT_SETTINGS.copy()

    @staticmethod
    def _normalize(raw: Any) -> dict[str, Any]:
        """Valida os dados lidos, usando padrões para valores inválidos."""

        normalized = DEFAULT_SETTINGS.copy()
        if not isinstance(raw, dict):
            return normalized

        volume = raw.get("volume", normalized["volume"])
        if isinstance(volume, (int, float)) and not isinstance(volume, bool):
            normalized["volume"] = max(0, min(100, round(volume)))

        for key in ("sound_enabled", "show_education_tips", "fullscreen"):
            value = raw.get(key, normalized[key])
            if isinstance(value, bool):
                normalized[key] = value

        return normalized

    def load(self) -> dict[str, Any]:
        """Lê o arquivo; se não existir ou estiver inválido, usa os padrões."""

        try:
            raw = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            raw = None

        self.values = self._normalize(raw)
        return self.values.copy()

    def save(self, settings: dict[str, Any] | None = None) -> bool:
        """Salva as preferências de forma atômica; retorna sucesso ou falha."""

        candidate = self.values if settings is None else settings
        self.values = self._normalize(candidate)

        temporary_path = self.file_path.with_suffix(self.file_path.suffix + ".tmp")

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path.write_text(
                json.dumps(self.values, ensure_ascii=False, indent=4) + "\n",
                encoding="utf-8",
            )
            temporary_path.replace(self.file_path)
            return True
        except OSError:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
            return False
