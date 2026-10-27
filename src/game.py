import random
import pygame

from src.audio import AudioManager
from src.bin import Bin
from src.effects import ParticleBurst
from src.item import WasteItem


class EcoDropGame:
    """
    Controla o funcionamento principal do EcoDrop.

    Estados disponíveis:
        MENU: menu principal.
        INSTRUCTIONS: tela de instruções.
        PLAYING: partida em andamento.
        GAME_OVER: fim da partida.
    """

    # ==================================================
    # CONSTANTES
    # ==================================================

    MENU = "menu"
    INSTRUCTIONS = "instructions"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    WIDTH = 800
    HEIGHT = 600
    FPS = 60

    BACKGROUND = (10, 20, 35)
    GREEN = (52, 211, 153)
    WHITE = (245, 245, 245)
    GRAY = (150, 165, 180)
    RED = (235, 90, 90)

    # ==================================================
    # INICIALIZAÇÃO
    # ==================================================

    def __init__(self) -> None:
        """
        Inicializa a janela, o áudio, as fontes,
        o cenário, as lixeiras e os dados do jogo.
        """

        # ----------------------------------------------
        # JANELA
        # ----------------------------------------------

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "EcoDrop | Son Games"
        )

        self.clock = pygame.time.Clock()

        # ----------------------------------------------
        # CENÁRIO
        # ----------------------------------------------

        # O cenário é criado uma única vez e reutilizado.
        self.background_surface = self._create_background()

        # ----------------------------------------------
        # FONTES
        # ----------------------------------------------

        self.font_title = pygame.font.Font(None, 68)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_normal = pygame.font.Font(None, 25)
        self.font_small = pygame.font.Font(None, 19)
        self.font_item = pygame.font.Font(None, 24)
        self.font_bin = pygame.font.Font(None, 23)
        self.font_button = pygame.font.Font(None, 29)

        # ----------------------------------------------
        # ÁUDIO
        # ----------------------------------------------

        self.audio = AudioManager()

        # ----------------------------------------------
        # CATEGORIAS DAS LIXEIRAS
        # ----------------------------------------------

        bin_data = [
            ("papel", "PAPEL", (49, 130, 206)),
            ("plastico", "PLÁSTICO", (220, 66, 66)),
            ("vidro", "VIDRO", (46, 160, 100)),
            ("metal", "METAL", (225, 170, 45)),
            ("organico", "ORGÂNICOS", (133, 94, 66)),
        ]

        self.bins = []

        for index, (category, label, color) in enumerate(
            bin_data
        ):
            x = 28 + index * 152

            bin_object = Bin(
                x=x,
                y=460,
                width=136,
                height=95,
                category=category,
                label=label,
                color=color,
            )

            self.bins.append(bin_object)

        # Centro horizontal de cada coluna.
        self.lane_centers = [
            bin_object.rect.centerx
            for bin_object in self.bins
        ]

        # ----------------------------------------------
        # DESTAQUE DA COLUNA SELECIONADA
        # ----------------------------------------------

        self.lane_glow_surface = pygame.Surface(
            (108, 310),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            self.lane_glow_surface,
            (52, 211, 153, 24),
            self.lane_glow_surface.get_rect(),
            border_radius=18,
        )

        # ----------------------------------------------
        # RESÍDUOS DISPONÍVEIS
        # ----------------------------------------------

        self.waste_types = [
            ("Jornal", "papel"),
            ("Caixa de papelão", "papel"),
            ("Garrafa PET", "plastico"),
            ("Pote plástico", "plastico"),
            ("Garrafa de vidro", "vidro"),
            ("Pote de vidro", "vidro"),
            ("Lata de alumínio", "metal"),
            ("Lata de conserva", "metal"),
            ("Casca de banana", "organico"),
            ("Restos de frutas", "organico"),
        ]

        # ----------------------------------------------
        # ESTADO INICIAL
        # ----------------------------------------------

        self.state = self.MENU
        self.running = True

        self._reset_round()

    # ==================================================
    # CRIAÇÃO DO CENÁRIO
    # ==================================================

    def _create_background(self) -> pygame.Surface:
        """
        Cria um cenário com degradê, elementos decorativos
        e uma área de chão.
        """

        background = pygame.Surface(
            (self.WIDTH, self.HEIGHT)
        )

        # ----------------------------------------------
        # DEGRADÊ
        # ----------------------------------------------

        cor_superior = (9, 18, 34)
        cor_inferior = (16, 45, 49)

        for y in range(self.HEIGHT):

            progresso = y / max(
                1,
                self.HEIGHT - 1,
            )

            cor_atual = tuple(
                int(
                    cor_superior[index]
                    + (
                        cor_inferior[index]
                        - cor_superior[index]
                    ) * progresso
                )
                for index in range(3)
            )

            pygame.draw.line(
                background,
                cor_atual,
                (0, y),
                (self.WIDTH, y),
            )

        # ----------------------------------------------
        # PONTOS DECORATIVOS
        # ----------------------------------------------

        for index in range(34):

            x = (index * 73 + 41) % self.WIDTH
            y = (index * 47 + 71) % 425

            raio = 1 + (index % 2)

            pygame.draw.circle(
                background,
                (29, 65, 73),
                (x, y),
                raio,
            )

        # ----------------------------------------------
        # FORMAS DECORATIVAS AO FUNDO
        # ----------------------------------------------

        pygame.draw.circle(
            background,
            (15, 48, 54),
            (110, 305),
            72,
            width=2,
        )

        pygame.draw.circle(
            background,
            (17, 52, 56),
            (700, 280),
            94,
            width=2,
        )

        pygame.draw.circle(
            background,
            (20, 57, 58),
            (700, 280),
            75,
            width=1,
        )

        # ----------------------------------------------
        # CHÃO
        # ----------------------------------------------

        pygame.draw.rect(
            background,
            (10, 29, 38),
            pygame.Rect(
                0,
                448,
                self.WIDTH,
                self.HEIGHT - 448,
            ),
        )

        pygame.draw.line(
            background,
            (33, 83, 72),
            (0, 448),
            (self.WIDTH, 448),
            2,
        )

        pygame.draw.line(
            background,
            (19, 51, 53),
            (0, 454),
            (self.WIDTH, 454),
            1,
        )

        # ----------------------------------------------
        # VEGETAÇÃO À ESQUERDA
        # ----------------------------------------------

        pygame.draw.line(
            background,
            (28, 79, 60),
            (12, 570),
            (47, 472),
            4,
        )

        pygame.draw.ellipse(
            background,
            (28, 91, 63),
            pygame.Rect(17, 490, 26, 13),
        )

        pygame.draw.ellipse(
            background,
            (35, 104, 69),
            pygame.Rect(31, 472, 25, 13),
        )

        pygame.draw.ellipse(
            background,
            (30, 85, 61),
            pygame.Rect(5, 525, 25, 13),
        )

        # ----------------------------------------------
        # VEGETAÇÃO À DIREITA
        # ----------------------------------------------

        pygame.draw.line(
            background,
            (28, 79, 60),
            (788, 570),
            (753, 472),
            4,
        )

        pygame.draw.ellipse(
            background,
            (28, 91, 63),
            pygame.Rect(758, 490, 26, 13),
        )

        pygame.draw.ellipse(
            background,
            (35, 104, 69),
            pygame.Rect(744, 472, 25, 13),
        )

        pygame.draw.ellipse(
            background,
            (30, 85, 61),
            pygame.Rect(770, 525, 25, 13),
        )

        return background

    # ==================================================
    # REINICIALIZAÇÃO DA PARTIDA
    # ==================================================

    def _reset_round(self) -> None:
        """
        Reinicializa as informações de uma partida.
        """

        self.score = 0
        self.lives = 3
        self.combo = 0

        self.items_processed = 0
        self.level = 1

        self.fall_speed = 2.8

        self.current_item = None
        self.transition_item = None

        self.current_lane = 2
        self.spawn_timer = 0

        # Feedback visual.
        self.feedback_text = ""
        self.feedback_color = self.WHITE
        self.feedback_timer = 0

        # Destaques temporários.
        self.highlighted_bins = {}

        # Animações de partículas.
        self.effects = []

    # ==================================================
    # INICIAR PARTIDA
    # ==================================================

    def _start_game(self) -> None:
        """
        Inicia uma nova partida.
        """

        self._reset_round()

        self.state = self.PLAYING

        self.audio.play_start()

        self._spawn_item()

    # ==================================================
    # CRIAR RESÍDUOS
    # ==================================================

    def _spawn_item(self) -> None:
        """
        Cria um resíduo em uma coluna aleatória.
        """

        name, category = random.choice(
            self.waste_types
        )

        self.current_lane = random.randrange(
            len(self.bins)
        )

        lane_x = self.lane_centers[
            self.current_lane
        ]

        self.current_item = WasteItem(
            name=name,
            category=category,
            x=lane_x,
            y=175,
            fall_speed=self.fall_speed,
        )

        self.spawn_timer = 0

    # ==================================================
    # MOVIMENTAÇÃO ENTRE COLUNAS
    # ==================================================

    def _move_lane(self, direction: int) -> None:
        """
        Solicita o movimento horizontal suave.

        direction:
            -1 = esquerda.
             1 = direita.
        """

        new_lane = max(
            0,
            min(
                len(self.bins) - 1,
                self.current_lane + direction,
            ),
        )

        if new_lane == self.current_lane:
            return

        self.current_lane = new_lane

        if self.current_item is not None:

            lane_x = self.lane_centers[
                self.current_lane
            ]

            self.current_item.move_to_x(
                lane_x
            )

    # ==================================================
    # EVENTOS DO TECLADO
    # ==================================================

    def _handle_events(self) -> None:
        """
        Processa os eventos da janela e do teclado.
        """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type != pygame.KEYDOWN:
                continue

            # ------------------------------------------
            # MENU
            # ------------------------------------------

            if self.state == self.MENU:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    self._start_game()

                elif event.key in (
                    pygame.K_i,
                    pygame.K_h,
                    pygame.K_F1,
                ):
                    self.state = self.INSTRUCTIONS

            # ------------------------------------------
            # INSTRUÇÕES
            # ------------------------------------------

            elif self.state == self.INSTRUCTIONS:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                    pygame.K_ESCAPE,
                ):
                    self.state = self.MENU

            # ------------------------------------------
            # PARTIDA
            # ------------------------------------------

            elif self.state == self.PLAYING:

                if event.key == pygame.K_ESCAPE:

                    self.state = self.MENU

                    self.current_item = None
                    self.transition_item = None

                    self.highlighted_bins.clear()
                    self.effects.clear()

                elif event.key == pygame.K_LEFT:

                    self._move_lane(-1)

                elif event.key == pygame.K_RIGHT:

                    self._move_lane(1)

            # ------------------------------------------
            # FIM DE JOGO
            # ------------------------------------------

            elif self.state == self.GAME_OVER:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_r,
                ):
                    self._start_game()

                elif event.key == pygame.K_ESCAPE:

                    self.state = self.MENU

                    self.current_item = None
                    self.transition_item = None

                    self.highlighted_bins.clear()
                    self.effects.clear()

    # ==================================================
    # ATUALIZAÇÃO DA LÓGICA
    # ==================================================

    def _update(self) -> None:
        """
        Atualiza as animações, os feedbacks e a partida.
        """

        # ----------------------------------------------
        # PARTÍCULAS
        # ----------------------------------------------

        for effect in self.effects:
            effect.update()

        self.effects = [
            effect
            for effect in self.effects
            if not effect.finished
        ]

        # ----------------------------------------------
        # ANIMAÇÃO DE SAÍDA DO RESÍDUO
        # ----------------------------------------------

        transition_item = self.transition_item

        if transition_item is not None:

            transition_item.update()

            if transition_item.finished:
                self.transition_item = None

        # ----------------------------------------------
        # FEEDBACK VISUAL
        # ----------------------------------------------

        if self.feedback_timer > 0:

            self.feedback_timer -= 1

            if self.feedback_timer == 0:
                self.highlighted_bins.clear()

        # ----------------------------------------------
        # LÓGICA DA PARTIDA
        # ----------------------------------------------

        if self.state != self.PLAYING:
            return

        # Se não existir resíduo, aguarda o próximo.
        if self.current_item is None:

            self.spawn_timer += 1

            if self.spawn_timer >= 45:
                self._spawn_item()

            return

        # Atualiza o movimento do resíduo.
        self.current_item.update()

        # Verifica se alcançou a região das lixeiras.
        if (
            self.current_item.rect.bottom
            >= self.bins[0].rect.top
        ):
            self._resolve_item()

    # ==================================================
    # CLASSIFICAR RESÍDUOS
    # ==================================================

    def _resolve_item(self) -> None:
        """
        Verifica a classificação do resíduo e atualiza
        os pontos, as vidas, o feedback e as animações.
        """

        if self.current_item is None:
            return

        item = self.current_item

        # ----------------------------------------------
        # COLUNA EM QUE O RESÍDUO REALMENTE ESTÁ
        # ----------------------------------------------

        landed_lane = min(
            range(len(self.lane_centers)),
            key=lambda index: abs(
                item.x - self.lane_centers[index]
            ),
        )

        target_bin = self.bins[landed_lane]

        # ----------------------------------------------
        # LIXEIRA CORRETA
        # ----------------------------------------------

        correct_lane = next(
            index
            for index, bin_object in enumerate(self.bins)
            if bin_object.category == item.category
        )

        correct_bin = self.bins[correct_lane]

        # ----------------------------------------------
        # ACERTO
        # ----------------------------------------------

        if item.category == target_bin.category:

            self.highlighted_bins = {
                landed_lane: self.GREEN
            }

            self.combo += 1

            points = 100 * self.combo

            self.score += points

            self.feedback_text = (
                f"Correto! {item.name} -> "
                f"{target_bin.label} (+{points})"
            )

            self.feedback_color = self.GREEN

            self.audio.play_correct()

        # ----------------------------------------------
        # ERRO
        # ----------------------------------------------

        else:

            self.highlighted_bins = {
                landed_lane: self.RED,
                correct_lane: self.GREEN,
            }

            self.lives -= 1
            self.combo = 0

            self.feedback_text = (
                f"Incorreto! {item.name} vai em "
                f"{correct_bin.label}."
            )

            self.feedback_color = self.RED

            # Evita sobrepor o som de erro ao de fim de jogo.
            if self.lives > 0:
                self.audio.play_error()

        # ----------------------------------------------
        # ANIMAÇÃO DE PARTÍCULAS
        # ----------------------------------------------

        self.effects.append(
            ParticleBurst(
                x=item.rect.centerx,
                y=item.rect.centery,
                color=self.feedback_color,
                particle_count=18,
            )
        )

        # ----------------------------------------------
        # TEMPORIZADORES
        # ----------------------------------------------

        self.feedback_timer = 45

        self.items_processed += 1

        # ----------------------------------------------
        # PROGRESSÃO DA DIFICULDADE
        # ----------------------------------------------

        self.level = (
            self.items_processed // 5
        ) + 1

        self.fall_speed = min(
            5.0,
            2.8 + 0.25 * (self.level - 1),
        )

        # ----------------------------------------------
        # ANIMAÇÃO DE SAÍDA
        # ----------------------------------------------

        item.start_exit()

        self.transition_item = item

        self.current_item = None

        self.spawn_timer = 0

        # ----------------------------------------------
        # FIM DE JOGO
        # ----------------------------------------------

        if self.lives <= 0:

            self.state = self.GAME_OVER

            self.audio.play_game_over()

    # ==================================================
    # TEXTO
    # ==================================================

    def _draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        center: tuple[int, int] | None = None,
        topleft: tuple[int, int] | None = None,
    ) -> None:
        """
        Desenha textos centralizados ou em uma posição fixa.
        """

        text_surface = font.render(
            text,
            True,
            color,
        )

        if center is not None:

            rect = text_surface.get_rect(
                center=center
            )

        elif topleft is not None:

            rect = text_surface.get_rect(
                topleft=topleft
            )

        else:

            rect = text_surface.get_rect()

        self.screen.blit(
            text_surface,
            rect,
        )

    # ==================================================
    # MENU PRINCIPAL
    # ==================================================

    def _draw_menu(self) -> None:
        """
        Desenha o menu principal.
        """

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        self._draw_text(
            "EcoDrop",
            self.font_title,
            self.GREEN,
            center=(400, 135),
        )

        self._draw_text(
            "Tetris da Reciclagem",
            self.font_subtitle,
            self.WHITE,
            center=(400, 195),
        )

        self._draw_text(
            "Separe os resíduos e ajude o meio ambiente!",
            self.font_normal,
            self.GRAY,
            center=(400, 255),
        )

        # Botão visual para iniciar.
        button = pygame.Rect(
            285,
            315,
            230,
            62,
        )

        pygame.draw.rect(
            self.screen,
            (25, 65, 65),
            button,
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            self.GREEN,
            button,
            width=2,
            border_radius=12,
        )

        self._draw_text(
            "JOGAR",
            self.font_button,
            self.WHITE,
            center=button.center,
        )

        self._draw_text(
            "Pressione ENTER ou ESPAÇO",
            self.font_normal,
            self.GRAY,
            center=(400, 415),
        )

        self._draw_text(
            "Use as setas durante a partida",
            self.font_small,
            self.GRAY,
            center=(400, 455),
        )

        self._draw_text(
            "Pressione I para consultar as instruções",
            self.font_small,
            self.GREEN,
            center=(400, 490),
        )

        self._draw_text(
            "Son Games | Projeto em desenvolvimento",
            self.font_small,
            self.GRAY,
            center=(400, 570),
        )

    # ==================================================
    # TELA DE INSTRUÇÕES
    # ==================================================

    def _draw_instructions(self) -> None:
        """
        Apresenta os controles, o objetivo e as regras
        básicas do EcoDrop.
        """

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        self._draw_text(
            "COMO JOGAR",
            self.font_title,
            self.GREEN,
            center=(400, 75),
        )

        self._draw_text(
            "Aprenda as regras do EcoDrop",
            self.font_subtitle,
            self.WHITE,
            center=(400, 120),
        )

        # ----------------------------------------------
        # CARTÃO DE CONTROLES
        # ----------------------------------------------

        controles_rect = pygame.Rect(
            65,
            160,
            320,
            115,
        )

        pygame.draw.rect(
            self.screen,
            (20, 39, 52),
            controles_rect,
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            (49, 130, 206),
            controles_rect,
            width=2,
            border_radius=12,
        )

        self._draw_text(
            "CONTROLES",
            self.font_normal,
            (100, 180, 255),
            center=(225, 185),
        )

        self._draw_text(
            "ESQUERDA / DIREITA",
            self.font_small,
            self.WHITE,
            center=(225, 220),
        )

        self._draw_text(
            "Escolha a coluna da lixeira",
            self.font_small,
            self.GRAY,
            center=(225, 247),
        )

        # ----------------------------------------------
        # CARTÃO DE OBJETIVO
        # ----------------------------------------------

        objetivo_rect = pygame.Rect(
            415,
            160,
            320,
            115,
        )

        pygame.draw.rect(
            self.screen,
            (20, 39, 52),
            objetivo_rect,
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            self.GREEN,
            objetivo_rect,
            width=2,
            border_radius=12,
        )

        self._draw_text(
            "OBJETIVO",
            self.font_normal,
            self.GREEN,
            center=(575, 185),
        )

        self._draw_text(
            "Separe os resíduos corretamente",
            self.font_small,
            self.WHITE,
            center=(575, 220),
        )

        self._draw_text(
            "Observe o nome de cada objeto",
            self.font_small,
            self.GRAY,
            center=(575, 247),
        )

        # ----------------------------------------------
        # CARTÃO DE PONTUAÇÃO
        # ----------------------------------------------

        pontos_rect = pygame.Rect(
            65,
            300,
            210,
            125,
        )

        pygame.draw.rect(
            self.screen,
            (20, 39, 52),
            pontos_rect,
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            self.GREEN,
            pontos_rect,
            width=2,
            border_radius=12,
        )

        self._draw_text(
            "PONTUAÇÃO",
            self.font_normal,
            self.GREEN,
            center=(170, 325),
        )

        self._draw_text(
            "Primeiro acerto: +100",
            self.font_small,
            self.WHITE,
            center=(170, 360),
        )

        self._draw_text(
            "Combo aumenta os pontos",
            self.font_small,
            self.GRAY,
            center=(170, 389),
        )

        # ----------------------------------------------
        # CARTÃO DE ERROS
        # ----------------------------------------------

        erros_rect = pygame.Rect(
            295,
            300,
            210,
            125,
        )

        pygame.draw.rect(
            self.screen,
            (20, 39, 52),
            erros_rect,
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            self.RED,
            erros_rect,
            width=2,
            border_radius=12,
        )

        self._draw_text(
            "ATENÇÃO",
            self.font_normal,
            self.RED,
            center=(400, 325),
        )

        self._draw_text(
            "Erro: perde uma vida",
            self.font_small,
            self.WHITE,
            center=(400, 360),
        )

        self._draw_text(
            "Combo volta a zero",
            self.font_small,
            self.GRAY,
            center=(400, 389),
        )

        # ----------------------------------------------
        # CARTÃO DE DIFICULDADE
        # ----------------------------------------------

        dificuldade_rect = pygame.Rect(
            525,
            300,
            210,
            125,
        )

        pygame.draw.rect(
            self.screen,
            (20, 39, 52),
            dificuldade_rect,
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            (225, 170, 45),
            dificuldade_rect,
            width=2,
            border_radius=12,
        )

        self._draw_text(
            "DESAFIO",
            self.font_normal,
            (245, 195, 80),
            center=(630, 325),
        )

        self._draw_text(
            "A cada 5 resíduos",
            self.font_small,
            self.WHITE,
            center=(630, 360),
        )

        self._draw_text(
            "A queda fica mais rápida",
            self.font_small,
            self.GRAY,
            center=(630, 389),
        )

        # ----------------------------------------------
        # CATEGORIAS
        # ----------------------------------------------

        self._draw_text(
            "CATEGORIAS",
            self.font_small,
            self.WHITE,
            center=(400, 457),
        )

        categorias = [
            ("PAPEL", (49, 130, 206)),
            ("PLÁSTICO", (220, 66, 66)),
            ("VIDRO", (46, 160, 100)),
            ("METAL", (225, 170, 45)),
            ("ORGÂNICOS", (133, 94, 66)),
        ]

        for index, (nome, cor) in enumerate(categorias):

            x = 100 + index * 150

            pygame.draw.circle(
                self.screen,
                cor,
                (x, 490),
                5,
            )

            self._draw_text(
                nome,
                self.font_small,
                self.WHITE,
                center=(x, 510),
            )

        # ----------------------------------------------
        # RETORNO AO MENU
        # ----------------------------------------------

        self._draw_text(
            "ENTER ou ESC para voltar ao menu",
            self.font_normal,
            self.GREEN,
            center=(400, 555),
        )

    # ==================================================
    # TELA DA PARTIDA
    # ==================================================

    def _draw_game(self) -> None:
        """
        Desenha o cenário e os elementos da partida.
        """

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        # ----------------------------------------------
        # PAINEL DE INFORMAÇÕES
        # ----------------------------------------------

        self._draw_text(
            "EcoDrop",
            self.font_normal,
            self.GREEN,
            topleft=(24, 22),
        )

        self._draw_text(
            f"Pontos: {self.score}",
            self.font_small,
            self.WHITE,
            topleft=(190, 26),
        )

        self._draw_text(
            f"Vidas: {self.lives}",
            self.font_small,
            self.WHITE,
            topleft=(355, 26),
        )

        self._draw_text(
            f"Combo: x{self.combo}",
            self.font_small,
            self.WHITE,
            topleft=(480, 26),
        )

        self._draw_text(
            f"Nível: {self.level}",
            self.font_small,
            self.WHITE,
            topleft=(650, 26),
        )

        pygame.draw.line(
            self.screen,
            (40, 57, 72),
            (24, 62),
            (776, 62),
            1,
        )

        # ----------------------------------------------
        # INSTRUÇÃO DURANTE A PARTIDA
        # ----------------------------------------------

        self._draw_text(
            "Use as setas para escolher a lixeira correta",
            self.font_normal,
            self.GRAY,
            center=(400, 88),
        )

        # ----------------------------------------------
        # FEEDBACK
        # ----------------------------------------------

        if self.feedback_timer > 0:

            self._draw_text(
                self.feedback_text,
                self.font_small,
                self.feedback_color,
                center=(400, 124),
            )

        # ----------------------------------------------
        # DESTAQUE DA COLUNA
        # ----------------------------------------------

        lane_x = self.lane_centers[
            self.current_lane
        ]

        self.screen.blit(
            self.lane_glow_surface,
            (
                lane_x
                - self.lane_glow_surface.get_width() // 2,
                145,
            ),
        )

        # ----------------------------------------------
        # LINHAS DAS COLUNAS
        # ----------------------------------------------

        for lane_x in self.lane_centers:

            pygame.draw.line(
                self.screen,
                (25, 40, 54),
                (lane_x, 145),
                (lane_x, 455),
                2,
            )

        # ----------------------------------------------
        # RESÍDUO ATUAL
        # ----------------------------------------------

        if self.current_item is not None:

            self.current_item.draw(
                self.screen,
                self.font_item,
            )

        # ----------------------------------------------
        # RESÍDUO EM ANIMAÇÃO DE SAÍDA
        # ----------------------------------------------

        if self.transition_item is not None:

            self.transition_item.draw(
                self.screen,
                self.font_item,
            )

        # ----------------------------------------------
        # LIXEIRAS
        # ----------------------------------------------

        for bin_object in self.bins:

            bin_object.draw(
                self.screen,
                self.font_bin,
            )

        # ----------------------------------------------
        # DESTAQUES DAS LIXEIRAS
        # ----------------------------------------------

        for (
            lane_index,
            highlight_color,
        ) in self.highlighted_bins.items():

            bin_rect = self.bins[lane_index].rect

            highlight_rect = bin_rect.inflate(
                10,
                10,
            )

            pygame.draw.rect(
                self.screen,
                highlight_color,
                highlight_rect,
                width=4,
                border_radius=15,
            )

        # ----------------------------------------------
        # RODAPÉ
        # ----------------------------------------------

        self._draw_text(
            "ESC: voltar ao menu",
            self.font_small,
            self.GRAY,
            center=(400, 583),
        )

    # ==================================================
    # TELA DE FIM DE JOGO
    # ==================================================

    def _draw_game_over(self) -> None:
        """
        Desenha a tela de fim de jogo.
        """

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        panel = pygame.Rect(
            100,
            125,
            600,
            350,
        )

        pygame.draw.rect(
            self.screen,
            (20, 36, 52),
            panel,
            border_radius=18,
        )

        pygame.draw.rect(
            self.screen,
            self.GREEN,
            panel,
            width=2,
            border_radius=18,
        )

        self._draw_text(
            "FIM DE JOGO",
            self.font_title,
            self.GREEN,
            center=(400, 195),
        )

        self._draw_text(
            f"Pontuação final: {self.score}",
            self.font_subtitle,
            self.WHITE,
            center=(400, 270),
        )

        self._draw_text(
            f"Resíduos classificados: {self.items_processed}",
            self.font_normal,
            self.GRAY,
            center=(400, 320),
        )

        self._draw_text(
            "ENTER ou R para jogar novamente",
            self.font_normal,
            self.WHITE,
            center=(400, 380),
        )

        self._draw_text(
            "ESC para voltar ao menu",
            self.font_small,
            self.GRAY,
            center=(400, 425),
        )

        self._draw_text(
            "Son Games",
            self.font_small,
            self.GRAY,
            center=(400, 560),
        )

    # ==================================================
    # DESENHO DAS TELAS E DAS PARTÍCULAS
    # ==================================================

    def _draw(self) -> None:
        """
        Desenha o estado atual do jogo e as partículas.
        """

        if self.state == self.MENU:

            self._draw_menu()

        elif self.state == self.INSTRUCTIONS:

            self._draw_instructions()

        elif self.state == self.PLAYING:

            self._draw_game()

        elif self.state == self.GAME_OVER:

            self._draw_game_over()

        # As partículas ficam por cima da interface.
        for effect in self.effects:

            effect.draw(
                self.screen
            )

        pygame.display.flip()

    # ==================================================
    # LOOP PRINCIPAL
    # ==================================================

    def run(self) -> None:
        """
        Executa o ciclo principal do jogo.
        """

        while self.running:

            self._handle_events()

            self._update()

            self._draw()

            self.clock.tick(
                self.FPS
            )
