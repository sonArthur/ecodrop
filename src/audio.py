"""
Gerenciador centralizado dos efeitos sonoros do EcoDrop.

O volume principal é multiplicado pelo volume-base de cada efeito.
Assim, ajustar ou silenciar o áudio não apaga as diferenças de intensidade
definidas para cada som.
"""

from pathlib import Path

import pygame


class AudioManager:
    """Carrega, controla e reproduz os efeitos sonoros do jogo."""

    BASE_VOLUMES = {
        "start": 0.35,
        "correct": 0.45,
        "error": 0.40,
        "game_over": 0.45,
    }

    SOUND_FILES = {
        "start": "inicio.wav",
        "correct": "acerto.wav",
        "error": "erro.wav",
        "game_over": "fim_de_jogo.wav",
    }

    def __init__(self) -> None:
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.enabled = True
        self.master_volume = 1.0
        self.available = False

        project_root = Path(__file__).resolve().parent.parent
        sounds_dir = project_root / "assets" / "sounds"

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(
                    frequency=22050,
                    size=-16,
                    channels=1,
                    buffer=512,
                )

            for sound_name, filename in self.SOUND_FILES.items():
                sound_path = sounds_dir / filename
                self.sounds[sound_name] = pygame.mixer.Sound(
                    str(sound_path)
                )

            self.available = True
            self._apply_volume()

        except (pygame.error, OSError) as error:
            self.sounds.clear()
            self.available = False
            print(
                "Aviso: os efeitos sonoros não puderam "
                f"ser carregados: {error}"
            )

    def _apply_volume(self) -> None:
        """Aplica volume principal × volume-base em cada efeito."""

        effective_master = (
            self.master_volume
            if self.enabled and self.available
            else 0.0
        )

        for sound_name, sound in self.sounds.items():
            base_volume = self.BASE_VOLUMES.get(sound_name, 1.0)
            sound.set_volume(
                max(0.0, min(1.0, base_volume * effective_master))
            )

    def set_volume(self, volume: float) -> None:
        """Define o volume principal no intervalo de 0.0 a 1.0."""

        try:
            normalized = float(volume)
        except (TypeError, ValueError):
            normalized = self.master_volume

        self.master_volume = max(0.0, min(1.0, normalized))
        self._apply_volume()

    def set_enabled(self, enabled: bool) -> None:
        """Liga ou desliga os efeitos sem alterar o volume escolhido."""

        self.enabled = bool(enabled) and self.available
        self._apply_volume()

    def play(self, sound_name: str) -> None:
        """Reproduz um efeito se o áudio estiver habilitado e disponível."""

        if not self.available or not self.enabled or self.master_volume <= 0:
            return

        sound = self.sounds.get(sound_name)
        if sound is not None:
            sound.play()

    def play_start(self) -> None:
        self.play("start")

    def play_correct(self) -> None:
        self.play("correct")

    def play_error(self) -> None:
        self.play("error")

    def play_game_over(self) -> None:
        self.play("game_over")
