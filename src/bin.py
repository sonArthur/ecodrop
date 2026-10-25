import pygame


class Bin:
    """
    Representa uma lixeira de reciclagem do EcoDrop.

    Cada lixeira possui:
    - Uma posição na tela.
    - Dimensões.
    - Uma categoria de resíduos.
    - Um nome para exibição.
    - Uma cor de identificação.
    - Detalhes visuais próprios.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        category: str,
        label: str,
        color: tuple[int, int, int],
    ) -> None:

        # Área principal da lixeira.
        # Mantemos as dimensões para preservar a lógica do jogo.
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height,
        )

        # Identificação interna da categoria.
        self.category = category

        # Nome apresentado ao jogador.
        self.label = label

        # Cor usada nos detalhes da lixeira.
        self.color = color

        # Fundo escuro da estrutura.
        self.body_color = (24, 43, 54)

        # Cor do painel frontal.
        self.panel_color = (31, 52, 63)

        # Cor dos detalhes claros.
        self.highlight_color = (172, 205, 195)

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
    ) -> None:
        """
        Desenha a lixeira com corpo, tampa, contorno,
        símbolo ambiental e nome da categoria.
        """

        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height

        # ==================================================
        # 1. SOMBRA
        # ==================================================

        shadow_rect = self.rect.move(
            0,
            5,
        )

        pygame.draw.rect(
            surface,
            (5, 13, 21),
            shadow_rect,
            border_radius=12,
        )

        # ==================================================
        # 2. CORPO PRINCIPAL
        # ==================================================

        body_rect = pygame.Rect(
            x + 5,
            y + 15,
            width - 10,
            height - 19,
        )

        pygame.draw.rect(
            surface,
            self.body_color,
            body_rect,
            border_radius=10,
        )

        # Painel frontal.
        panel_rect = pygame.Rect(
            x + 9,
            y + 24,
            width - 18,
            height - 32,
        )

        pygame.draw.rect(
            surface,
            self.panel_color,
            panel_rect,
            border_radius=7,
        )

        # ==================================================
        # 3. FAIXA DE IDENTIFICAÇÃO
        # ==================================================

        faixa_rect = pygame.Rect(
            x + 7,
            y + 17,
            width - 14,
            5,
        )

        pygame.draw.rect(
            surface,
            self.color,
            faixa_rect,
            border_radius=2,
        )

        # ==================================================
        # 4. TAMPA
        # ==================================================

        lid_rect = pygame.Rect(
            x + 1,
            y + 5,
            width - 2,
            15,
        )

        pygame.draw.rect(
            surface,
            self.color,
            lid_rect,
            border_radius=5,
        )

        # Borda da tampa.
        pygame.draw.rect(
            surface,
            self.highlight_color,
            lid_rect,
            width=1,
            border_radius=5,
        )

        # Alça da tampa.
        handle_rect = pygame.Rect(
            self.rect.centerx - 12,
            y + 8,
            24,
            4,
        )

        pygame.draw.rect(
            surface,
            (24, 43, 54),
            handle_rect,
            border_radius=2,
        )

        # ==================================================
        # 5. DETALHES DO CORPO
        # ==================================================

        # Pequenos detalhes verticais nas laterais.
        pygame.draw.line(
            surface,
            (47, 72, 82),
            (x + 13, y + 30),
            (x + 13, y + height - 10),
            2,
        )

        pygame.draw.line(
            surface,
            (47, 72, 82),
            (x + width - 13, y + 30),
            (x + width - 13, y + height - 10),
            2,
        )

        # Base inferior.
        base_rect = pygame.Rect(
            x + 9,
            y + height - 8,
            width - 18,
            4,
        )

        pygame.draw.rect(
            surface,
            (13, 28, 38),
            base_rect,
            border_radius=2,
        )

        # ==================================================
        # 6. SÍMBOLO AMBIENTAL
        # ==================================================

        icon_center = (
            x + 25,
            y + 57,
        )

        # Círculo de fundo do ícone.
        pygame.draw.circle(
            surface,
            (17, 35, 45),
            icon_center,
            13,
        )

        pygame.draw.circle(
            surface,
            self.color,
            icon_center,
            13,
            width=2,
        )

        # Folha estilizada.
        leaf_rect = pygame.Rect(
            icon_center[0] - 7,
            icon_center[1] - 6,
            13,
            10,
        )

        pygame.draw.ellipse(
            surface,
            (116, 214, 160),
            leaf_rect,
        )

        # Nervura da folha.
        pygame.draw.line(
            surface,
            (24, 91, 57),
            (
                icon_center[0] - 5,
                icon_center[1] + 3,
            ),
            (
                icon_center[0] + 4,
                icon_center[1] - 4,
            ),
            2,
        )

        # ==================================================
        # 7. NOME DA CATEGORIA
        # ==================================================

        # Reserva espaço à esquerda para o ícone.
        largura_disponivel = width - 47

        fonte_categoria = font

        # Reduz a fonte quando o nome for comprido.
        if fonte_categoria.size(self.label)[0] > largura_disponivel:

            fonte_categoria = pygame.font.Font(
                None,
                18,
            )

        texto = fonte_categoria.render(
            self.label,
            True,
            (245, 245, 245),
        )

        texto_rect = texto.get_rect(
            center=(
                x + 45 + largura_disponivel // 2,
                y + 58,
            )
        )

        surface.blit(
            texto,
            texto_rect,
        )

        # ==================================================
        # 8. CONTORNO EXTERNO
        # ==================================================

        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            width=2,
            border_radius=12,
        )
