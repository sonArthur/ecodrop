import pygame


class WasteItem:
    """
    Representa um resíduo que aparece durante a partida.

    A categoria fica armazenada internamente para que
    o jogo possa verificar se o jogador acertou a lixeira.

    O desenho do objeto não revela sua categoria.
    """

    def __init__(
        self,
        name: str,
        category: str,
        x: int,
        y: int,
        fall_speed: float = 2.8,
        width: int = 132,
        height: int = 54
    ) -> None:

        self.name = name
        self.category = category

        # Guardamos as posições como números decimais.
        # Isso permite adicionar movimentos suaves futuramente.
        self.x = float(x)
        self.y = float(y)

        self.speed = float(fall_speed)

        # Área ocupada pelo resíduo na tela.
        self.rect = pygame.Rect(
            0,
            0,
            width,
            height
        )

        self._sync_rect()

    def _sync_rect(self) -> None:
        """
        Sincroniza o retângulo visual com a posição do objeto.
        """

        self.rect.center = (
            round(self.x),
            round(self.y)
        )

    def move_to_x(self, x: int) -> None:
        """
        Posiciona o resíduo no centro da coluna selecionada.
        """

        self.x = float(x)
        self._sync_rect()

    def update(self) -> None:
        """
        Atualiza a posição vertical do resíduo.

        O objeto desce a cada atualização do jogo.
        """

        self.y += self.speed
        self._sync_rect()

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font
    ) -> None:
        """
        Desenha o resíduo sem revelar sua categoria.
        """

        # Sombra.
        shadow_rect = self.rect.move(0, 4)

        pygame.draw.rect(
            surface,
            (5, 12, 22),
            shadow_rect,
            border_radius=12
        )

        # Cartão do resíduo.
        pygame.draw.rect(
            surface,
            (31, 48, 63),
            self.rect,
            border_radius=12
        )

        # Contorno neutro, igual para todas as categorias.
        pygame.draw.rect(
            surface,
            (110, 135, 150),
            self.rect,
            width=2,
            border_radius=12
        )

        # Nome do resíduo.
        texto = font.render(
            self.name,
            True,
            (245, 245, 245)
        )

        # Reduzimos a fonte caso um nome seja muito comprido.
        if texto.get_width() > self.rect.width - 12:
            fonte_menor = pygame.font.Font(None, 20)

            texto = fonte_menor.render(
                self.name,
                True,
                (245, 245, 245)
            )

        texto_rect = texto.get_rect(
            center=self.rect.center
        )

        surface.blit(texto, texto_rect)
