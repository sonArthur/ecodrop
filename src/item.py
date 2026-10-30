import pygame


class WasteItem:
    """
    Representa um resíduo durante a partida.

    Funcionalidades:
    - Movimento horizontal suave.
    - Movimento vertical de queda.
    - Animação de entrada.
    - Animação de saída.
    - Ilustração própria para cada resíduo.
    - Categoria armazenada internamente.
    """

    HORIZONTAL_SPEED = 16.0

    FADE_IN_FRAMES = 10
    FADE_OUT_FRAMES = 12

    def __init__(
        self,
        name: str,
        category: str,
        x: int,
        y: int,
        fall_speed: float = 2.8,
        width: int = 132,
        height: int = 54,
    ) -> None:

        # Informações internas do resíduo.
        self.name = name
        self.category = category

        # Posição atual.
        self.x = float(x)
        self.y = float(y)

        # Destino horizontal.
        self.target_x = float(x)

        # Velocidade da queda.
        self.speed = float(fall_speed)

        # Área ocupada pelo objeto.
        self.rect = pygame.Rect(
            0,
            0,
            width,
            height,
        )

        # Estado inicial da animação.
        self.animation_state = "entering"
        self.animation_frame = 0

        self.opacity = 0
        self.finished = False

        self._sync_rect()

    # ==================================================
    # POSIÇÃO E MOVIMENTAÇÃO
    # ==================================================

    def _sync_rect(self) -> None:
        """
        Sincroniza o retângulo visual com a posição atual.
        """

        self.rect.center = (
            round(self.x),
            round(self.y),
        )

    def move_to_x(self, x: int) -> None:
        """
        Define a posição horizontal desejada.
        """

        if self.animation_state == "exiting":
            return

        self.target_x = float(x)

    def start_exit(self) -> None:
        """
        Inicia a animação de desaparecimento.
        """

        if self.animation_state == "exiting":
            return

        self.animation_state = "exiting"
        self.animation_frame = 0

    def update(self) -> None:
        """
        Atualiza a movimentação e as animações.
        """

        if self.finished:
            return

        # ----------------------------------------------
        # ANIMAÇÃO DE SAÍDA
        # ----------------------------------------------

        if self.animation_state == "exiting":

            self.animation_frame += 1

            progresso = min(
                1.0,
                self.animation_frame / self.FADE_OUT_FRAMES,
            )

            self.opacity = round(
                255 * (1.0 - progresso)
            )

            if progresso >= 1.0:

                self.opacity = 0
                self.finished = True

            self._sync_rect()
            return

        # ----------------------------------------------
        # MOVIMENTO HORIZONTAL
        # ----------------------------------------------

        distancia_x = self.target_x - self.x

        if abs(distancia_x) <= self.HORIZONTAL_SPEED:

            self.x = self.target_x

        elif distancia_x > 0:

            self.x += self.HORIZONTAL_SPEED

        else:

            self.x -= self.HORIZONTAL_SPEED

        # ----------------------------------------------
        # MOVIMENTO VERTICAL
        # ----------------------------------------------

        self.y += self.speed

        # ----------------------------------------------
        # ANIMAÇÃO DE ENTRADA
        # ----------------------------------------------

        if self.animation_state == "entering":

            self.animation_frame += 1

            progresso = min(
                1.0,
                self.animation_frame / self.FADE_IN_FRAMES,
            )

            self.opacity = round(
                255 * progresso
            )

            if progresso >= 1.0:

                self.animation_state = "active"
                self.opacity = 255

        self._sync_rect()

    # ==================================================
    # ILUSTRAÇÕES DOS RESÍDUOS
    # ==================================================

    def _draw_icon(
        self,
        surface: pygame.Surface,
    ) -> None:
        """
        Desenha uma ilustração de acordo com o nome
        do resíduo.

        A ilustração não exibe o nome da categoria.
        """

        name = self.name.lower()

        # ----------------------------------------------
        # JORNAL
        # ----------------------------------------------

        if name == "jornal":

            # Folha de fundo.
            pygame.draw.rect(
                surface,
                (192, 199, 198),
                (10, 11, 25, 34),
                border_radius=2,
            )

            # Folha principal.
            pygame.draw.rect(
                surface,
                (245, 244, 232),
                (6, 8, 25, 34),
                border_radius=2,
            )

            # Manchete.
            pygame.draw.rect(
                surface,
                (62, 76, 83),
                (10, 12, 17, 5),
            )

            # Linhas que representam o texto.
            for y in (21, 25, 29, 33, 37):

                pygame.draw.line(
                    surface,
                    (112, 123, 126),
                    (10, y),
                    (26, y),
                    1,
                )

        # ----------------------------------------------
        # CAIXA DE PAPELÃO
        # ----------------------------------------------

        elif name == "caixa de papelão":

            # Lado esquerdo da caixa.
            pygame.draw.polygon(
                surface,
                (173, 119, 68),
                [
                    (7, 17),
                    (22, 23),
                    (22, 43),
                    (7, 36),
                ],
            )

            # Lado direito.
            pygame.draw.polygon(
                surface,
                (132, 87, 49),
                [
                    (22, 23),
                    (38, 16),
                    (38, 36),
                    (22, 43),
                ],
            )

            # Parte superior.
            pygame.draw.polygon(
                surface,
                (211, 158, 98),
                [
                    (7, 17),
                    (22, 9),
                    (38, 16),
                    (22, 23),
                ],
            )

            # Abas superiores.
            pygame.draw.line(
                surface,
                (117, 77, 43),
                (14, 13),
                (29, 20),
                2,
            )

            pygame.draw.line(
                surface,
                (117, 77, 43),
                (29, 20),
                (29, 27),
                2,
            )

        # ----------------------------------------------
        # GARRAFA PET
        # ----------------------------------------------

        elif name == "garrafa pet":

            azul = (102, 195, 220)

            # Corpo da garrafa.
            pygame.draw.rect(
                surface,
                azul,
                (12, 19, 20, 25),
                border_radius=5,
            )

            # Ombros.
            pygame.draw.polygon(
                surface,
                azul,
                [
                    (12, 22),
                    (15, 16),
                    (19, 13),
                    (25, 13),
                    (29, 17),
                    (32, 22),
                ],
            )

            # Gargalo.
            pygame.draw.rect(
                surface,
                (130, 215, 231),
                (17, 10, 10, 9),
                border_radius=2,
            )

            # Tampa.
            pygame.draw.rect(
                surface,
                (235, 107, 89),
                (17, 7, 10, 4),
                border_radius=1,
            )

            # Anéis do corpo.
            for y in (28, 34, 40):

                pygame.draw.line(
                    surface,
                    (57, 139, 169),
                    (14, y),
                    (30, y),
                    1,
                )

        # ----------------------------------------------
        # POTE PLÁSTICO
        # ----------------------------------------------

        elif name == "pote plástico":

            azul = (94, 183, 213)

            # Corpo do recipiente.
            pygame.draw.polygon(
                surface,
                azul,
                [
                    (11, 20),
                    (34, 20),
                    (30, 43),
                    (15, 43),
                ],
            )

            # Tampa.
            pygame.draw.ellipse(
                surface,
                (159, 222, 234),
                (8, 13, 29, 9),
            )

            # Borda da tampa.
            pygame.draw.arc(
                surface,
                (52, 132, 165),
                (8, 13, 29, 9),
                0,
                3.14,
                2,
            )

            # Linha decorativa.
            pygame.draw.line(
                surface,
                (51, 135, 166),
                (14, 30),
                (31, 30),
                2,
            )

        # ----------------------------------------------
        # GARRAFA DE VIDRO
        # ----------------------------------------------

        elif name == "garrafa de vidro":

            verde = (91, 184, 136)

            # Corpo.
            pygame.draw.rect(
                surface,
                verde,
                (12, 21, 20, 23),
                border_radius=4,
            )

            # Ombros.
            pygame.draw.polygon(
                surface,
                verde,
                [
                    (12, 23),
                    (14, 17),
                    (18, 14),
                    (26, 14),
                    (30, 18),
                    (32, 23),
                ],
            )

            # Gargalo.
            pygame.draw.rect(
                surface,
                (112, 202, 153),
                (17, 10, 10, 9),
                border_radius=2,
            )

            # Tampa.
            pygame.draw.rect(
                surface,
                (219, 190, 107),
                (17, 7, 10, 4),
                border_radius=1,
            )

            # Reflexo do vidro.
            pygame.draw.line(
                surface,
                (200, 244, 211),
                (16, 24),
                (16, 37),
                2,
            )

        # ----------------------------------------------
        # POTE DE VIDRO
        # ----------------------------------------------

        elif name == "pote de vidro":

            vidro = (126, 190, 171)

            # Corpo do pote.
            pygame.draw.rect(
                surface,
                vidro,
                (10, 18, 25, 26),
                border_radius=4,
            )

            # Gargalo.
            pygame.draw.rect(
                surface,
                (150, 211, 189),
                (14, 13, 17, 7),
                border_radius=2,
            )

            # Tampa.
            pygame.draw.rect(
                surface,
                (205, 180, 111),
                (12, 10, 21, 5),
                border_radius=2,
            )

            # Reflexo.
            pygame.draw.line(
                surface,
                (218, 248, 229),
                (15, 23),
                (15, 37),
                2,
            )

        # ----------------------------------------------
        # LATAS
        # ----------------------------------------------

        elif name in (
            "lata de alumínio",
            "lata de conserva",
        ):

            if name == "lata de alumínio":

                corpo = (171, 191, 201)
                detalhe = (102, 129, 142)

            else:

                corpo = (191, 151, 111)
                detalhe = (124, 91, 62)

            # Corpo cilíndrico.
            pygame.draw.rect(
                surface,
                corpo,
                (12, 15, 20, 27),
            )

            # Tampa superior.
            pygame.draw.ellipse(
                surface,
                (220, 226, 224),
                (12, 11, 20, 9),
            )

            # Parte inferior.
            pygame.draw.ellipse(
                surface,
                detalhe,
                (12, 36, 20, 8),
            )

            # Reflexo lateral.
            pygame.draw.line(
                surface,
                (242, 244, 239),
                (16, 19),
                (16, 35),
                2,
            )

            # Abertura superior.
            pygame.draw.ellipse(
                surface,
                detalhe,
                (18, 13, 9, 4),
                1,
            )

        # ----------------------------------------------
        # CASCA DE BANANA
        # ----------------------------------------------

        elif name == "casca de banana":

            amarelo = (246, 200, 51)
            contorno = (180, 137, 28)

            pygame.draw.polygon(
                surface,
                amarelo,
                [
                    (8, 15),
                    (13, 10),
                    (20, 12),
                    (27, 18),
                    (33, 26),
                    (31, 33),
                    (27, 39),
                    (21, 42),
                    (16, 38),
                    (21, 32),
                    (24, 27),
                    (20, 22),
                    (15, 18),
                    (10, 20),
                ],
            )

            # Detalhes da casca.
            pygame.draw.line(
                surface,
                contorno,
                (13, 13),
                (21, 17),
                2,
            )

            pygame.draw.line(
                surface,
                contorno,
                (21, 17),
                (27, 24),
                2,
            )

            # Pequeno cabo.
            pygame.draw.line(
                surface,
                (101, 127, 62),
                (8, 15),
                (5, 12),
                3,
            )

        # ----------------------------------------------
        # RESTOS DE FRUTAS
        # ----------------------------------------------

        elif name == "restos de frutas":

            # Pedaço vermelho.
            pygame.draw.circle(
                surface,
                (211, 83, 77),
                (15, 28),
                9,
            )

            # Pedaço amarelo.
            pygame.draw.circle(
                surface,
                (244, 191, 61),
                (28, 31),
                8,
            )

            # Pedaço roxo.
            pygame.draw.circle(
                surface,
                (145, 106, 179),
                (27, 19),
                7,
            )

            # Folhas verdes.
            pygame.draw.ellipse(
                surface,
                (80, 170, 103),
                (18, 8, 12, 6),
            )

            pygame.draw.line(
                surface,
                (46, 122, 70),
                (20, 11),
                (29, 12),
                1,
            )

        # ----------------------------------------------
        # CELULAR
        # ----------------------------------------------

        elif name.startswith("celular"):

            pygame.draw.rect(
                surface,
                (35, 43, 55),
                (14, 5, 20, 44),
                border_radius=4,
            )
            pygame.draw.rect(
                surface,
                (91, 174, 190),
                (17, 10, 14, 32),
                border_radius=2,
            )
            pygame.draw.circle(surface, (220, 230, 232), (24, 46), 1)
            pygame.draw.line(surface, (190, 224, 225), (19, 14), (29, 14), 1)

        # ----------------------------------------------
        # NOTEBOOK
        # ----------------------------------------------

        elif name.startswith("notebook"):

            pygame.draw.rect(
                surface,
                (54, 68, 82),
                (8, 7, 31, 27),
                border_radius=3,
            )
            pygame.draw.rect(
                surface,
                (92, 164, 181),
                (11, 10, 25, 20),
                border_radius=1,
            )
            pygame.draw.polygon(
                surface,
                (178, 190, 198),
                [(5, 36), (42, 36), (37, 44), (10, 44)],
            )
            pygame.draw.line(surface, (95, 111, 122), (10, 39), (37, 39), 1)

        # ----------------------------------------------
        # TECLADO
        # ----------------------------------------------

        elif name.startswith("teclado"):

            pygame.draw.rect(
                surface,
                (57, 68, 80),
                (5, 17, 39, 25),
                border_radius=4,
            )
            for row_y in (22, 28, 34):
                for column_x in (11, 19, 27, 35):
                    pygame.draw.rect(
                        surface,
                        (190, 205, 211),
                        (column_x, row_y, 4, 3),
                        border_radius=1,
                    )

        # ----------------------------------------------
        # MONITOR
        # ----------------------------------------------

        elif name.startswith("monitor"):

            pygame.draw.rect(
                surface,
                (48, 59, 72),
                (5, 8, 40, 29),
                border_radius=4,
            )
            pygame.draw.rect(
                surface,
                (91, 161, 176),
                (9, 12, 32, 20),
                border_radius=2,
            )
            pygame.draw.line(surface, (168, 183, 188), (25, 37), (25, 44), 3)
            pygame.draw.line(surface, (168, 183, 188), (16, 45), (34, 45), 3)

        # ----------------------------------------------
        # MOUSE
        # ----------------------------------------------

        elif name.startswith("mouse"):

            pygame.draw.ellipse(
                surface,
                (75, 91, 106),
                (13, 8, 25, 39),
            )
            pygame.draw.ellipse(
                surface,
                (181, 197, 202),
                (13, 8, 25, 39),
                2,
            )
            pygame.draw.line(surface, (190, 207, 211), (25, 10), (25, 25), 2)
            pygame.draw.line(surface, (190, 207, 211), (25, 12), (25, 18), 2)

        # ----------------------------------------------
        # CARREGADOR
        # ----------------------------------------------

        elif name.startswith("carregador"):

            pygame.draw.rect(
                surface,
                (205, 214, 216),
                (13, 15, 21, 24),
                border_radius=4,
            )
            pygame.draw.line(surface, (210, 218, 220), (19, 15), (19, 8), 3)
            pygame.draw.line(surface, (210, 218, 220), (28, 15), (28, 8), 3)
            pygame.draw.circle(surface, (90, 111, 123), (23, 27), 3, 1)

        # ----------------------------------------------
        # CABO USB
        # ----------------------------------------------

        elif name.startswith("cabo usb"):

            pygame.draw.arc(
                surface,
                (119, 167, 180),
                (10, 8, 30, 36),
                0.2,
                3.0,
                4,
            )
            pygame.draw.rect(surface, (190, 202, 207), (7, 8, 10, 8), border_radius=2)
            pygame.draw.rect(surface, (190, 202, 207), (32, 37, 10, 8), border_radius=2)
            pygame.draw.line(surface, (86, 108, 120), (10, 10), (10, 14), 1)
            pygame.draw.line(surface, (86, 108, 120), (35, 39), (35, 43), 1)

        # ----------------------------------------------
        # PLACA ELETRÔNICA
        # ----------------------------------------------

        elif name.startswith("placa eletrônica"):

            pygame.draw.rect(
                surface,
                (48, 119, 91),
                (5, 9, 40, 36),
                border_radius=3,
            )
            pygame.draw.rect(surface, (35, 67, 61), (17, 17, 15, 15))
            pygame.draw.rect(surface, (193, 174, 105), (8, 13, 6, 5))
            pygame.draw.rect(surface, (193, 174, 105), (34, 31, 7, 8))
            pygame.draw.line(surface, (193, 174, 105), (14, 20), (18, 20), 2)
            pygame.draw.line(surface, (193, 174, 105), (32, 24), (38, 24), 2)
            pygame.draw.line(surface, (193, 174, 105), (24, 32), (24, 40), 2)

        # ----------------------------------------------
        # PILHA E BATERIAS
        # ----------------------------------------------

        elif name.startswith("pilha"):

            pygame.draw.rect(
                surface,
                (190, 197, 199),
                (14, 12, 20, 33),
                border_radius=4,
            )
            pygame.draw.rect(surface, (225, 183, 63), (14, 12, 20, 9), border_radius=3)
            pygame.draw.rect(surface, (91, 105, 114), (21, 8, 7, 4), border_radius=1)
            pygame.draw.line(surface, (112, 126, 132), (17, 27), (31, 27), 2)

        elif name.startswith("bateria"):

            pygame.draw.rect(
                surface,
                (61, 75, 88),
                (8, 16, 32, 27),
                border_radius=4,
            )
            pygame.draw.rect(surface, (187, 198, 198), (18, 12, 12, 4), border_radius=1)
            pygame.draw.rect(surface, (92, 174, 130), (12, 21, 24, 17), border_radius=2)
            pygame.draw.line(surface, (236, 241, 230), (19, 29), (29, 29), 2)
            pygame.draw.line(surface, (236, 241, 230), (24, 24), (24, 34), 2)

        # ----------------------------------------------
        # SÍMBOLO GENÉRICO
        # ----------------------------------------------

        else:

            pygame.draw.circle(
                surface,
                (129, 163, 177),
                (22, 27),
                14,
            )

            pygame.draw.circle(
                surface,
                (220, 235, 238),
                (22, 27),
                14,
                2,
            )

    # ==================================================
    # DESENHO DO RESÍDUO
    # ==================================================

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
    ) -> None:
        """
        Desenha o cartão do resíduo, sua ilustração
        e seu nome, mantendo a transparência da animação.
        """

        if self.finished or self.opacity <= 0:
            return

        width = self.rect.width
        height = self.rect.height

        # Superfície temporária com suporte à transparência.
        item_surface = pygame.Surface(
            (width, height),
            pygame.SRCALPHA,
        )

        # ----------------------------------------------
        # SOMBRA
        # ----------------------------------------------

        shadow_rect = pygame.Rect(
            0,
            4,
            width,
            height - 2,
        )

        pygame.draw.rect(
            item_surface,
            (5, 12, 22),
            shadow_rect,
            border_radius=12,
        )

        # ----------------------------------------------
        # FUNDO
        # ----------------------------------------------

        item_rect = pygame.Rect(
            0,
            0,
            width,
            height,
        )

        pygame.draw.rect(
            item_surface,
            (31, 48, 63),
            item_rect,
            border_radius=12,
        )

        # ----------------------------------------------
        # CONTORNO
        # ----------------------------------------------

        pygame.draw.rect(
            item_surface,
            (110, 135, 150),
            item_rect,
            width=2,
            border_radius=12,
        )

        # ----------------------------------------------
        # ILUSTRAÇÃO
        # ----------------------------------------------

        self._draw_icon(
            item_surface
        )

        # ----------------------------------------------
        # NOME DO RESÍDUO
        # ----------------------------------------------

        # Área disponível para o texto, à direita do ícone.
        largura_texto = width - 49

        # Usa uma fonte um pouco menor se o nome não couber.
        label_font = font

        if label_font.size(self.name)[0] > largura_texto:

            label_font = pygame.font.Font(
                None,
                20,
            )

        # Divide o nome em linhas para evitar que
        # o texto ultrapasse os limites do cartão.
        palavras = self.name.split()

        linhas = []
        linha_atual = ""

        for palavra in palavras:

            if linha_atual:

                candidato = (
                    linha_atual + " " + palavra
                )

            else:

                candidato = palavra

            if (
                label_font.size(candidato)[0]
                <= largura_texto
            ):

                linha_atual = candidato

            else:

                if linha_atual:
                    linhas.append(linha_atual)

                linha_atual = palavra

        if linha_atual:
            linhas.append(linha_atual)

        altura_linha = 17

        altura_total = (
            len(linhas) * altura_linha
        )

        inicio_y = (
            height - altura_total
        ) // 2

        centro_x = (
            45 + width - 4
        ) // 2

        for index, linha in enumerate(linhas):

            texto = label_font.render(
                linha,
                True,
                (245, 245, 245),
            )

            texto_rect = texto.get_rect(
                center=(
                    centro_x,
                    inicio_y
                    + index * altura_linha
                    + altura_linha // 2,
                )
            )

            item_surface.blit(
                texto,
                texto_rect,
            )

        # ----------------------------------------------
        # APLICAR TRANSPARÊNCIA
        # ----------------------------------------------

        item_surface.set_alpha(
            self.opacity
        )

        surface.blit(
            item_surface,
            self.rect.topleft,
        )
