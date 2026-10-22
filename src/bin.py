import pygame


class Bin:
    """
    Representa uma lixeira de reciclagem no jogo EcoDrop.

    Cada lixeira possui:
    - Uma posição na tela.
    - Uma largura e uma altura.
    - Uma categoria de resíduos.
    - Um nome para exibição.
    - Uma cor de identificação.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        category: str,
        label: str,
        color: tuple[int, int, int]
    ) -> None:
        # Define a área ocupada pela lixeira.
        self.rect = pygame.Rect(x, y, width, height)

        # Identificador usado futuramente na classificação dos resíduos.
        self.category = category

        # Texto apresentado ao jogador.
        self.label = label

        # Cor utilizada para identificar a categoria.
        self.color = color

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font
    ) -> None:
        """
        Desenha a lixeira na superfície informada.

        Args:
            surface: superfície onde a lixeira será desenhada.
            font: fonte utilizada para exibir o nome da categoria.
        """

        # Desenha uma sombra para dar profundidade ao elemento.
        shadow_rect = self.rect.move(0, 5)

        pygame.draw.rect(
            surface,
            (5, 12, 22),
            shadow_rect,
            border_radius=12
        )

        # Desenha o corpo da lixeira.
        pygame.draw.rect(
            surface,
            (25, 44, 62),
            self.rect,
            border_radius=12
        )

        # Cria uma faixa colorida de identificação.
        faixa = pygame.Rect(
            self.rect.x + 5,
            self.rect.y + 5,
            self.rect.width - 10,
            10
        )

        pygame.draw.rect(
            surface,
            self.color,
            faixa,
            border_radius=5
        )

        # Desenha o contorno da lixeira com a cor da categoria.
        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            width=2,
            border_radius=12
        )

        # Renderiza o nome da categoria.
        texto = font.render(
            self.label,
            True,
            (245, 245, 245)
        )

        # Centraliza o texto dentro da lixeira.
        texto_rect = texto.get_rect(
            center=(
                self.rect.centerx,
                self.rect.centery + 5
            )
        )

        surface.blit(texto, texto_rect)
