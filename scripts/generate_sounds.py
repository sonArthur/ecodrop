import math
import struct
import wave

from pathlib import Path


# ==================================================
# CONFIGURAÇÕES
# ==================================================

SAMPLE_RATE = 22050
AMPLITUDE = 9000

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOUNDS_DIR = PROJECT_ROOT / "assets" / "sounds"


# ==================================================
# GERAÇÃO DOS ARQUIVOS WAV
# ==================================================

def generate_sound(
    filename: str,
    notes: list[tuple[float, float]]
) -> None:
    """
    Gera um efeito sonoro com tons sintetizados.

    Args:
        filename: nome do arquivo WAV.
        notes: lista de pares (frequência, duração).
    """

    audio_data = bytearray()

    for index, (frequency, duration) in enumerate(notes):

        total_samples = int(
            SAMPLE_RATE * duration
        )

        attack_samples = max(
            1,
            int(SAMPLE_RATE * 0.008)
        )

        release_samples = max(
            1,
            int(SAMPLE_RATE * 0.025)
        )

        for sample_index in range(total_samples):

            time_position = (
                sample_index / SAMPLE_RATE
            )

            # Envelope para suavizar o começo e o final.
            attack = min(
                1.0,
                sample_index / attack_samples
            )

            release = min(
                1.0,
                (total_samples - sample_index)
                / release_samples
            )

            envelope = max(
                0.0,
                min(attack, release)
            )

            # Produz uma onda senoidal.
            value = (
                AMPLITUDE
                * envelope
                * math.sin(
                    2 * math.pi
                    * frequency
                    * time_position
                )
            )

            # Salva cada amostra em PCM de 16 bits.
            audio_data.extend(
                struct.pack(
                    "<h",
                    int(value)
                )
            )

        # Pequena pausa entre notas.
        if index < len(notes) - 1:

            silence_samples = int(
                SAMPLE_RATE * 0.025
            )

            audio_data.extend(
                b"\x00\x00" * silence_samples
            )

    # Grava o arquivo WAV em formato PCM.
    output_path = SOUNDS_DIR / filename

    with wave.open(
        str(output_path),
        "wb"
    ) as wav_file:

        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)

        wav_file.writeframes(
            bytes(audio_data)
        )

    print(f"Som criado: {output_path.name}")


# ==================================================
# EFEITOS SONOROS DO ECODROP
# ==================================================

def main() -> None:

    SOUNDS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Som curto e ascendente para iniciar a partida.
    generate_sound(
        "inicio.wav",
        [
            (523.25, 0.07),
            (659.25, 0.07),
            (783.99, 0.12),
        ]
    )

    # Duas notas ascendentes para indicar um acerto.
    generate_sound(
        "acerto.wav",
        [
            (659.25, 0.07),
            (880.00, 0.13),
        ]
    )

    # Notas descendentes para indicar um erro.
    generate_sound(
        "erro.wav",
        [
            (330.00, 0.10),
            (220.00, 0.18),
        ]
    )

    # Sequência descendente para o fim da partida.
    generate_sound(
        "fim_de_jogo.wav",
        [
            (392.00, 0.12),
            (329.63, 0.12),
            (261.63, 0.16),
            (196.00, 0.28),
        ]
    )


if __name__ == "__main__":
    main()