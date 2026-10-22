import pygame

from src.game import EcoDropGame


def main() -> None:
    """
    Inicializa o Pygame e executa o EcoDrop.
    """

    pygame.init()

    try:
        game = EcoDropGame()
        game.run()

    finally:
        # Garante o encerramento do Pygame.
        pygame.quit()


if __name__ == "__main__":
    main()
