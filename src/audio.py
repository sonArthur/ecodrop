import pygame

from pathlib import Path


class AudioManager:
    """
    Gerencia os efeitos sonoros do EcoDrop.

    Responsabilidades:
    - Inicializar o mixer quando necessário.
    - Carregar os efeitos sonoros.
    - Reproduzir cada som conforme o evento.
    - Permitir que o jogo continue funcionando
      caso o áudio não esteja disponível.
    """

    def __init__(self) -> None:

        self.sounds = {}

        self.enabled = False

        # Caminho absoluto para os arquivos de áudio.
        project_root = Path(__file__).resolve().parent.parent

        sounds_dir = (
            project_root
            / "assets"
            / "sounds"
        )

        sound_files = {
            "start": "inicio.wav",
            "correct": "acerto.wav",
            "error": "erro.wav",
            "game_over": "fim_de_jogo.wav",
        }

        try:

            # Inicializa o mixer somente se necessário.
            if pygame.mixer.get_init() is None:

                pygame.mixer.init(
                    frequency=22050,
                    size=-16,
                    channels=1,
                    buffer=512,
                )

            # Carrega os arquivos de áudio.
            for sound_name, filename in sound_files.items():

                sound_path = sounds_dir / filename

                sound = pygame.mixer.Sound(
                    str(sound_path)
                )

                # Ajusta o volume individualmente.
                if sound_name == "start":
                    sound.set_volume(0.35)

                elif sound_name == "correct":
                    sound.set_volume(0.45)

                elif sound_name == "error":
                    sound.set_volume(0.40)

                elif sound_name == "game_over":
                    sound.set_volume(0.45)

                self.sounds[sound_name] = sound

            self.enabled = True

        except (pygame.error, OSError) as error:

            # A ausência de áudio não deve impedir o jogo.
            self.sounds.clear()

            self.enabled = False

            print(
                "Aviso: os efeitos sonoros não puderam "
                f"ser carregados: {error}"
            )

    def play(self, sound_name: str) -> None:
        """
        Reproduz um efeito sonoro pelo identificador.
        """

        if not self.enabled:
            return

        sound = self.sounds.get(sound_name)

        if sound is not None:
            sound.play()

    def play_start(self) -> None:
        """Reproduz o som de início da partida."""

        self.play("start")

    def play_correct(self) -> None:
        """Reproduz o som de acerto."""

        self.play("correct")

    def play_error(self) -> None:
        """Reproduz o som de erro."""

        self.play("error")

    def play_game_over(self) -> None:
        """Reproduz o som de fim de jogo."""

        self.play("game_over")
