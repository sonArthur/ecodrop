import pygame


class WasteItem:
    """
    Representa um resíduo que poderá ser reciclado no EcoDrop.

    Cada resíduo possui:
    - Nome.
    - Categoria de reciclagem.
    - Nome da categoria para exibição.
    - Posição na tela.
    - Dimensões.
    - Cor de identificação.
    """

    def __init__(
        self,
        name: str,
        category: str,
        category_label: str,
        x: int,
        y: int,
        color: tuple[int, int, int],
        width: int = 230,
        height: int = 100
    ) -> None:

        # Nome do resíduo.
        self.name = name

        # Identificador interno da categoria.
        # Será utilizado posteriormente na classificação.
        self.category = category

        # Nome da categoria apresentado ao jogador.
        self.category_label = category_label

        # Posição e dimensões do resíduo.
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        # Cor visual do resíduo.
        self.color = color

    def draw(
        self,
        surface: pygame.Surface,
        name_font: pygame.font.Font,
        category_font: pygame.font.Font,
        symbol_font: pygame.font.Font
    ) -> None:
        """
        Desenha a representação visual do resíduo.

        Args:
            surface: superfície onde o objeto será desenhado.
            name_font: fonte utilizada no nome do resíduo.
            category_font: fonte utilizada na categoria.
            symbol_font: fonte utilizada na identificação visual.
        """

        # Sombra para destacar o objeto do fundo.
        shadow_rect = self.rect.move(0, 5)

        pygame.draw.rect(
            surface,
            (5, 12, 22),
            shadow_rect,
            border_radius=14
        )

        # Fundo do cartão do resíduo.
        pygame.draw.rect(
            surface,
            (25, 44, 62),
            self.rect,
            border_radius=14
        )

        # Contorno colorido da categoria.
        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            width=2,
            border_radius=14
        )

        # Círculo que identifica visualmente a categoria.
        centro_circulo = (
            self.rect.x + 43,
            self.rect.centery
        )

        pygame.draw.circle(
            surface,
            self.color,
            centro_circulo,
            25
        )

        # Abreviação da categoria.
        abreviacoes = {
            "papel": "PA",
            "plastico": "PL",
            "vidro": "VI",
            "metal": "ME",
            "organico": "OR"
        }

        simbolo = abreviacoes.get(
            self.category,
            "?"
        )

        texto_simbolo = symbol_font.render(
            simbolo,
            True,
            (255, 255, 255)
        )

        surface.blit(
            texto_simbolo,
            texto_simbolo.get_rect(
                center=centro_circulo
            )
        )

        # Nome do resíduo.
        texto_nome = name_font.render(
            self.name,
            True,
            (245, 245, 245)
        )

        surface.blit(
            texto_nome,
            (self.rect.x + 82, self.rect.y + 29)
        )

        # Categoria do resíduo.
        texto_categoria = category_font.render(
            self.category_label,
            True,
            self.color
        )

        surface.blit(
            texto_categoria,
            (self.rect.x + 82, self.rect.y + 57)
        )
