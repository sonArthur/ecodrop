"""Persistência das preferências do jogador do EcoDrop."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS: dict[str, Any] = {
    "volume": 70,
    "sound_enabled": True,
    "show_education_tips": True,
    "fullscreen": False,
}


def get_user_data_dir() -> Path:
    """
    Retorna a pasta de dados persistentes do EcoDrop.

    No Windows, utiliza %APPDATA%.
    """

    appdata = os.environ.get("APPDATA")

    if appdata:
        base_dir = Path(appdata)
    else:
        # Alternativa caso a variável APPDATA não esteja disponível.
        base_dir = Path.home() / "AppData" / "Roaming"

    return base_dir / "EcoDrop"


class SettingsManager:
    """Carrega, valida e salva as configurações do jogador."""

    def __init__(self, file_path: str | Path | None = None) -> None:

        self.legacy_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "settings.json"
        )

        if file_path is not None:
            # Permite informar um caminho específico, útil para testes.
            self.file_path = Path(file_path)
            self.migrate_legacy = False
        else:
            self.file_path = get_user_data_dir() / "settings.json"
            self.migrate_legacy = True

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

        for key in (
            "sound_enabled",
            "show_education_tips",
            "fullscreen",
        ):
            value = raw.get(key, normalized[key])

            if isinstance(value, bool):
                normalized[key] = value

        return normalized

    def _read_file(self, path: Path) -> Any:
        """Lê um arquivo JSON sem interromper o jogo em caso de erro."""

        try:
            return json.loads(path.read_text(encoding="utf-8"))

        except (
            OSError,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ):
            return None

    def load(self) -> dict[str, Any]:
        """
        Carrega as configurações.

        Se ainda não existir um arquivo no AppData, tenta migrar
        as configurações antigas da pasta data/.
        """

        if self.file_path.exists():
            raw = self._read_file(self.file_path)

            self.values = self._normalize(raw)

            return self.values.copy()

        # Migração das configurações antigas.
        if self.migrate_legacy and self.legacy_path.is_file():

            raw = self._read_file(self.legacy_path)

            if isinstance(raw, dict):
                self.values = self._normalize(raw)

                # Salva no novo local sem apagar o arquivo antigo.
                self.save()

                return self.values.copy()

        self.values = DEFAULT_SETTINGS.copy()

        return self.values.copy()

    def save(self, settings: dict[str, Any] | None = None) -> bool:
        """Salva as preferências de forma atômica."""

        candidate = self.values if settings is None else settings

        self.values = self._normalize(candidate)

        temporary_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            temporary_path.write_text(
                json.dumps(
                    self.values,
                    ensure_ascii=False,
                    indent=4,
                ) + "\n",
                encoding="utf-8",
            )

            temporary_path.replace(self.file_path)

            return True

        except OSError as error:

            try:
                temporary_path.unlink(missing_ok=True)

            except OSError:
                pass

            print(
                "Aviso: não foi possível salvar as configurações: "
                f"{error}"
            )

            return False
