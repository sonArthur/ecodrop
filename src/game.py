import random
import pygame

from src.audio import AudioManager
from src.bin import Bin
from src.effects import ParticleBurst
from src.education import get_education_tip
from src.electronic_content import (
    ELECTRONIC_CATEGORIES,
    ELECTRONIC_WASTE_TYPES,
    get_electronic_tip,
)
from src.item import WasteItem
from src.modes import GAME_MODES, MODE_ELECTRONIC, MODE_GENERAL
from src.records import RecordManager
from src.quiz_content import QUIZ_QUESTIONS

class EcoDropGame:
    """
    Controla o funcionamento principal do EcoDrop.

    Estados:
        MENU: menu principal.
        INSTRUCTIONS: tela de instruções.
        PLAYING: partida em andamento.
        GAME_OVER: fim da partida.
    """

    # ==================================================
    # CONSTANTES
    # ==================================================

    MENU = "menu"
    MODE_SELECT = "mode_select"
    EWASTE_PREVIEW = "ewaste_preview"
    INSTRUCTIONS = "instructions"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    QUIZ = "quiz"
    QUIZ_RESULT = "quiz_result"

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
        """Inicializa os recursos e configura o jogo."""

        # --------------------------------------------------
        # JANELA
        # --------------------------------------------------

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "EcoDrop | Son Games"
        )

        self.clock = pygame.time.Clock()

        # --------------------------------------------------
        # FONTES
        # --------------------------------------------------

        self.font_title = pygame.font.Font(None, 68)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_normal = pygame.font.Font(None, 25)
        self.font_small = pygame.font.Font(None, 19)
        self.font_item = pygame.font.Font(None, 24)
        self.font_bin = pygame.font.Font(None, 23)
        self.font_button = pygame.font.Font(None, 29)

        # --------------------------------------------------
        # CENÁRIO
        # --------------------------------------------------

        self.background_surface = self._create_background()

        # --------------------------------------------------
        # ÁUDIO
        # --------------------------------------------------

        self.audio = AudioManager()

        # --------------------------------------------------
        # SISTEMA DE RECORDES
        # --------------------------------------------------

        self.records = RecordManager()

        # Indica se a partida atual estabeleceu um recorde.
        self.new_record = False

        # --------------------------------------------------
        # BOTÕES DO MENU
        # --------------------------------------------------

        self.play_button_rect = pygame.Rect(
            285, 300, 230, 58
        )

        self.instructions_button_rect = pygame.Rect(
            285, 375, 230, 52
        )

        # ==============================================
        # BOTÕES DA SELEÇÃO DE MODOS
        # ==============================================

        # Cartão do modo Reciclagem Geral.
        self.general_mode_rect = pygame.Rect(
            55,
            195,
            330,
            230,
        )

        # Cartão do modo Lixo Eletrônico.
        self.electronic_mode_rect = pygame.Rect(
            415,
            195,
            330,
            230,
        )

        # Botão para retornar à tela anterior.
        self.mode_back_button_rect = pygame.Rect(
            300,
            455,
            200,
            48,
        )

        # Botão opcional do desafio, exibido somente no fim
        # de uma partida do modo Lixo Eletrônico.
        self.quiz_start_button_rect = pygame.Rect(
            175, 465, 450, 42
        )

        # Áreas interativas da tela do questionário.
        self.quiz_option_rects = [
            pygame.Rect(125, 270 + index * 54, 550, 44)
            for index in range(3)
        ]
        self.quiz_continue_button_rect = pygame.Rect(
            285, 500, 230, 42
        )
        self.quiz_result_button_rect = pygame.Rect(
            285, 455, 230, 46
        )

        # Modo selecionado inicialmente.
        self.selected_mode = MODE_GENERAL

            # --------------------------------------------------
            # LIXEIRAS
            # --------------------------------------------------

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
            bin_object = Bin(
                x=28 + index * 152,
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

        # --------------------------------------------------
        # DESTAQUE DA COLUNA
        # --------------------------------------------------

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

        # --------------------------------------------------
        # RESÍDUOS DISPONÍVEIS
        # --------------------------------------------------

        # A categoria fica armazenada internamente.
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

        # --------------------------------------------------
        # ESTADO INICIAL
        # --------------------------------------------------

        self.state = self.MENU
        self.running = True

        self._reset_round()

    # ==================================================
    # CRIAÇÃO DO CENÁRIO
    # ==================================================

    def _create_background(self) -> pygame.Surface:
        """Cria o cenário decorativo do EcoDrop."""

        background = pygame.Surface(
            (self.WIDTH, self.HEIGHT)
        )

        # Degradê vertical.
        cor_superior = (9, 18, 34)
        cor_inferior = (16, 45, 49)

        for y in range(self.HEIGHT):

            progresso = y / (self.HEIGHT - 1)

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

        # Pontos decorativos.
        for index in range(34):

            x = (index * 73 + 41) % self.WIDTH
            y = (index * 47 + 71) % 425

            pygame.draw.circle(
                background,
                (29, 65, 73),
                (x, y),
                1 + index % 2,
            )

        # Círculos decorativos ao fundo.
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

        # Chão.
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

        # Vegetação decorativa à esquerda.
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

        # Vegetação decorativa à direita.
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
        """Reinicializa os dados da partida atual."""

        self.score = 0
        self.lives = 3
        self.combo = 0

        self.items_processed = 0
        self.level = 1

        self.fall_speed = 2.8

        # Resíduos.
        self.current_item = None
        self.transition_item = None

        self.current_lane = 2
        self.spawn_timer = 0

        # Feedback visual.
        self.feedback_text = ""
        self.feedback_color = self.WHITE
        self.feedback_timer = 0

        # Destaques temporários das lixeiras.
        self.highlighted_bins = {}

        # Animações de partículas.
        self.effects = []

        # Indicador de recorde da partida atual.
        self.new_record = False

        # Estado do desafio opcional (separado da pontuação da partida).
        self.quiz_questions = []
        self.quiz_question_index = 0
        self.current_question = None
        self.quiz_correct_answers = 0
        self.quiz_answered = False
        self.quiz_selected_index = None
        self.quiz_feedback = ""
        self.quiz_was_correct = False

    # ==================================================
    # CONFIGURAR A MODALIDADE
    # ==================================================

    def _configure_mode(self, mode: str) -> None:
        """Configura lixeiras, categorias e resíduos do modo escolhido."""

        if mode == MODE_ELECTRONIC:
            # Quatro estações específicas para resíduos eletrônicos.
            bin_data = ELECTRONIC_CATEGORIES
            bin_width = 170
            bin_gap = 20
            first_x = 30
            self.waste_types = list(ELECTRONIC_WASTE_TYPES)

        else:
            # Mantém exatamente as cinco categorias da modalidade original.
            bin_data = [
                ("papel", "PAPEL", (49, 130, 206)),
                ("plastico", "PLÁSTICO", (220, 66, 66)),
                ("vidro", "VIDRO", (46, 160, 100)),
                ("metal", "METAL", (225, 170, 45)),
                ("organico", "ORGÂNICOS", (133, 94, 66)),
            ]
            bin_width = 136
            bin_gap = 16
            first_x = 28
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

        self.bins = []

        for index, (category, label, color) in enumerate(bin_data):
            bin_object = Bin(
                x=first_x + index * (bin_width + bin_gap),
                y=460,
                width=bin_width,
                height=95,
                category=category,
                label=label,
                color=color,
            )
            self.bins.append(bin_object)

        # O centro de cada estação determina a coluna de movimentação.
        self.lane_centers = [
            bin_object.rect.centerx
            for bin_object in self.bins
        ]

        # Ajusta o destaque visual à largura das colunas da modalidade.
        glow_width = 142 if mode == MODE_ELECTRONIC else 108
        self.lane_glow_surface = pygame.Surface(
            (glow_width, 310),
            pygame.SRCALPHA,
        )
        pygame.draw.rect(
            self.lane_glow_surface,
            (52, 211, 153, 24),
            self.lane_glow_surface.get_rect(),
            border_radius=18,
        )

        self.selected_mode = mode

    # ==================================================
    # DESAFIO EDUCATIVO OPCIONAL
    # ==================================================

    def _start_quiz(self) -> None:
        """Inicia o questionário opcional depois do fim da partida."""

        # O questionário foi criado para aprofundar o modo eletrônico.
        if self.selected_mode != MODE_ELECTRONIC:
            return

        # Cada pergunta aparece uma vez, em ordem aleatória.
        self.quiz_questions = random.sample(
            QUIZ_QUESTIONS,
            k=len(QUIZ_QUESTIONS),
        )
        self.quiz_question_index = 0
        self.quiz_correct_answers = 0
        self._load_quiz_question()
        self.state = self.QUIZ

    def _load_quiz_question(self) -> None:
        """Carrega a pergunta atual e limpa o feedback anterior."""

        self.current_question = self.quiz_questions[
            self.quiz_question_index
        ]
        self.quiz_answered = False
        self.quiz_selected_index = None
        self.quiz_feedback = ""
        self.quiz_was_correct = False

    def _answer_quiz(self, selected_index: int) -> None:
        """Verifica uma alternativa sem alterar pontos ou recordes da partida."""

        if self.current_question is None or self.quiz_answered:
            return

        options = self.current_question["options"]
        if not 0 <= selected_index < len(options):
            return

        self.quiz_selected_index = selected_index
        correct_index = self.current_question["correct_index"]
        self.quiz_was_correct = selected_index == correct_index
        explanation = self.current_question["explanation"]

        if self.quiz_was_correct:
            self.quiz_correct_answers += 1
            self.quiz_feedback = f"Resposta correta! {explanation}"
        else:
            correct_option = options[correct_index]
            self.quiz_feedback = (
                f"A resposta correta era: {correct_option}. {explanation}"
            )

        # O questionário não retira vidas nem altera a pontuação/recorde.
        self.quiz_answered = True

    def _continue_after_quiz(self) -> None:
        """Avança para a próxima pergunta ou mostra o resultado final."""

        if not self.quiz_answered:
            return

        self.quiz_question_index += 1

        if self.quiz_question_index < len(self.quiz_questions):
            self._load_quiz_question()
        else:
            self.current_question = None
            self.state = self.QUIZ_RESULT

    def _cancel_quiz(self) -> None:
        """Fecha o desafio e retorna à tela de fim de jogo."""

        self.current_question = None
        self.state = self.GAME_OVER

    # ==================================================
    # INICIAR PARTIDA
    # ==================================================

    def _start_game(self, mode: str = MODE_GENERAL) -> None:
        """Inicia uma partida com a configuração da modalidade escolhida."""

        # Prepara as estações e os itens específicos do modo.
        self._configure_mode(mode)

        # Reinicializa pontuação, vidas, efeitos e dificuldade.
        self._reset_round()

        self.state = self.PLAYING
        self.audio.play_start()
        self._spawn_item()

    # ==================================================
    # CRIAR RESÍDUOS
    # ==================================================

    def _spawn_item(self) -> None:
        """Cria um resíduo em uma coluna aleatória."""

        name, category = random.choice(
            self.waste_types
        )

        self.current_lane = random.randrange(
            len(self.bins)
        )

        lane_x = self.lane_centers[
            self.current_lane
        ]

        # Os nomes dos eletrônicos são maiores; por isso, o cartão
        # recebe mais largura nessa modalidade para facilitar a leitura.
        if self.selected_mode == MODE_ELECTRONIC:
            item_width = 160
            item_height = 60
        else:
            item_width = 132
            item_height = 54

        self.current_item = WasteItem(
            name=name,
            category=category,
            x=lane_x,
            y=175,
            fall_speed=self.fall_speed,
            width=item_width,
            height=item_height,
        )

        self.spawn_timer = 0

    # ==================================================
    # MOVIMENTAÇÃO
    # ==================================================

    def _move_lane(self, direction: int) -> None:
        """
        Define a coluna de destino do resíduo.

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
    # EVENTOS DO TECLADO E MOUSE
    # ==================================================

    def _handle_events(self) -> None:
        """
        Processa os eventos da janela, do teclado e do mouse.
        """

        for event in pygame.event.get():

            # ==============================================
            # FECHAR A JANELA
            # ==============================================

            if event.type == pygame.QUIT:

                self.running = False

                continue

            # ==============================================
            # CLIQUES DO MOUSE
            # ==============================================

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Considera apenas o botão esquerdo.
                if event.button == 1:

                    # --------------------------------------
                    # MENU PRINCIPAL
                    # --------------------------------------

                    if self.state == self.MENU:

                        # Jogar abre a seleção de modos.
                        if self.play_button_rect.collidepoint(
                            event.pos
                        ):

                            self.state = self.MODE_SELECT

                        # Instruções continua funcionando.
                        elif self.instructions_button_rect.collidepoint(
                            event.pos
                        ):

                            self.state = self.INSTRUCTIONS

                    # --------------------------------------
                    # SELEÇÃO DE MODOS
                    # --------------------------------------

                    elif self.state == self.MODE_SELECT:

                        # Iniciar Reciclagem Geral.
                        if self.general_mode_rect.collidepoint(
                            event.pos
                        ):

                            self._start_game(
                                MODE_GENERAL
                            )

                        # Abrir apresentação do modo eletrônico.
                        elif self.electronic_mode_rect.collidepoint(
                            event.pos
                        ):

                            self._start_game(
                                MODE_ELECTRONIC
                            )

                        # Voltar ao menu.
                        elif self.mode_back_button_rect.collidepoint(
                            event.pos
                        ):

                            self.state = self.MENU

                    # --------------------------------------
                    # APRESENTAÇÃO DO MODO ELETRÔNICO
                    # --------------------------------------

                    elif self.state == self.EWASTE_PREVIEW:

                        if self.mode_back_button_rect.collidepoint(
                            event.pos
                        ):

                            self.state = self.MODE_SELECT

                    # Desafio opcional disponível depois da partida.
                    elif self.state == self.GAME_OVER:

                        if (
                            self.selected_mode == MODE_ELECTRONIC
                            and self.quiz_start_button_rect.collidepoint(event.pos)
                        ):
                            self._start_quiz()

                    # Respostas do questionário opcional.
                    elif self.state == self.QUIZ:

                        if not self.quiz_answered:
                            for index, option_rect in enumerate(
                                self.quiz_option_rects
                            ):
                                if option_rect.collidepoint(event.pos):
                                    self._answer_quiz(index)
                                    break
                        elif self.quiz_continue_button_rect.collidepoint(
                            event.pos
                        ):
                            self._continue_after_quiz()

                    elif self.state == self.QUIZ_RESULT:

                        if self.quiz_result_button_rect.collidepoint(event.pos):
                            self.state = self.GAME_OVER

                # O clique já foi processado.
                continue

            # ==============================================
            # EVENTOS DO TECLADO
            # ==============================================

            if event.type != pygame.KEYDOWN:
                continue

            # ----------------------------------------------
            # MENU PRINCIPAL
            # ----------------------------------------------

            if self.state == self.MENU:

                # Enter ou Espaço abre a seleção de modos.
                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):

                    self.state = self.MODE_SELECT

                elif event.key in (
                    pygame.K_i,
                    pygame.K_h,
                    pygame.K_F1,
                ):

                    self.state = self.INSTRUCTIONS

            # ----------------------------------------------
            # SELEÇÃO DE MODOS
            # ----------------------------------------------

            elif self.state == self.MODE_SELECT:

                # Tecla 1 inicia Reciclagem Geral.
                if event.key in (
                    pygame.K_1,
                    pygame.K_KP1,
                ):

                    self._start_game(
                        MODE_GENERAL
                    )

                # Tecla 2 abre o modo eletrônico.
                elif event.key in (
                    pygame.K_2,
                    pygame.K_KP2,
                ):

                    self._start_game(
                        MODE_ELECTRONIC
                    )

                # Voltar ao menu.
                elif event.key == pygame.K_ESCAPE:

                    self.state = self.MENU

            # ----------------------------------------------
            # APRESENTAÇÃO DO MODO ELETRÔNICO
            # ----------------------------------------------

            elif self.state == self.EWASTE_PREVIEW:

                # Retornar à seleção dos modos.
                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                    pygame.K_ESCAPE,
                ):

                    self.state = self.MODE_SELECT

            # ----------------------------------------------
            # INSTRUÇÕES
            # ----------------------------------------------

            elif self.state == self.INSTRUCTIONS:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                    pygame.K_ESCAPE,
                ):

                    self.state = self.MENU

            # ----------------------------------------------
            # PARTIDA
            # ----------------------------------------------

            elif self.state == self.PLAYING:

                # Voltar ao menu.
                if event.key == pygame.K_ESCAPE:

                    self.state = self.MENU

                    self.current_item = None
                    self.transition_item = None

                    self.highlighted_bins.clear()
                    self.effects.clear()

                # Mover à esquerda.
                elif event.key == pygame.K_LEFT:

                    self._move_lane(-1)

                # Mover à direita.
                elif event.key == pygame.K_RIGHT:

                    self._move_lane(1)

            # ----------------------------------------------
            # DESAFIO EDUCATIVO
            # ----------------------------------------------

            elif self.state == self.QUIZ:

                if event.key == pygame.K_ESCAPE:
                    self._cancel_quiz()

                elif not self.quiz_answered and event.key in (
                    pygame.K_1, pygame.K_KP1,
                    pygame.K_2, pygame.K_KP2,
                    pygame.K_3, pygame.K_KP3,
                ):
                    key_to_index = {
                        pygame.K_1: 0, pygame.K_KP1: 0,
                        pygame.K_2: 1, pygame.K_KP2: 1,
                        pygame.K_3: 2, pygame.K_KP3: 2,
                    }
                    self._answer_quiz(key_to_index[event.key])

                elif self.quiz_answered and event.key in (
                    pygame.K_RETURN, pygame.K_SPACE,
                ):
                    self._continue_after_quiz()

            elif self.state == self.QUIZ_RESULT:

                if event.key in (
                    pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE,
                ):
                    self.state = self.GAME_OVER

            # ----------------------------------------------
            # FIM DE JOGO
            # ----------------------------------------------

            elif self.state == self.GAME_OVER:

                # Reiniciar o modo jogável.
                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_r,
                ):

                    self._start_game(
                        self.selected_mode
                    )

                # Abrir o desafio opcional apenas no modo eletrônico.
                elif (
                    event.key == pygame.K_q
                    and self.selected_mode == MODE_ELECTRONIC
                ):
                    self._start_quiz()

                # Voltar ao menu.
                elif event.key == pygame.K_ESCAPE:

                    self.state = self.MENU

                    self.current_item = None
                    self.transition_item = None

                    self.highlighted_bins.clear()
                    self.effects.clear()

        # ==================================================
        # ATUALIZAR A LÓGICA E AS ANIMAÇÕES
        # ==================================================

    def _update(self) -> None:
        """Atualiza as animações, o feedback e a partida."""

        # Atualizar partículas.
        for effect in self.effects:
            effect.update()

        # Remover partículas concluídas.
        self.effects = [
            effect
            for effect in self.effects
            if not effect.finished
        ]

        # Atualizar a animação de saída do resíduo.
        transition_item = self.transition_item

        if transition_item is not None:

            transition_item.update()

            if transition_item.finished:
                self.transition_item = None

        # Atualizar o tempo do feedback.
        if self.feedback_timer > 0:

            self.feedback_timer -= 1

            if self.feedback_timer == 0:
                self.highlighted_bins.clear()

        # A queda só acontece durante a partida.
        if self.state != self.PLAYING:
            return

        # Aguardar para criar o próximo resíduo.
        if self.current_item is None:

            self.spawn_timer += 1

            if self.spawn_timer >= 45:
                self._spawn_item()

            return

        # Atualizar o movimento.
        self.current_item.update()

        # Verificar a chegada à região das lixeiras.
        if (
            self.current_item.rect.bottom
            >= self.bins[0].rect.top
        ):
            self._resolve_item()

        # ==================================================
        # CLASSIFICAR RESÍDUOS
        # ==================================================

    def _resolve_item(self) -> None:
        """Classifica o resíduo e atualiza a partida."""

        if self.current_item is None:
            return

        item = self.current_item

        # Encontrar a coluna mais próxima do resíduo.
        landed_lane = min(
            range(len(self.lane_centers)),
            key=lambda index: abs(
                item.x - self.lane_centers[index]
            ),
        )

        target_bin = self.bins[landed_lane]

        # Localizar a lixeira correta.
        correct_lane = next(
            index
            for index, bin_object in enumerate(self.bins)
            if bin_object.category == item.category
        )

        correct_bin = self.bins[correct_lane]

        # ------------------------------------------
        # ACERTO
        # ------------------------------------------

        if item.category == target_bin.category:

            self.highlighted_bins = {
                landed_lane: self.GREEN
            }

            self.combo += 1

            points = 100 * self.combo

            self.score += points

            # Exibir uma dica educativa correspondente à modalidade.
            if self.selected_mode == MODE_ELECTRONIC:
                education_tip = get_electronic_tip(item.name)
            else:
                education_tip = get_education_tip(item.name)

            self.feedback_text = (
                f"Correto! +{points} | {education_tip}"
            )

            self.feedback_color = self.GREEN

            self.audio.play_correct()

        # ------------------------------------------
        # ERRO
        # ------------------------------------------

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

            # Evitar sobrepor os sons no fim de jogo.
            if self.lives > 0:
                self.audio.play_error()

        # ------------------------------------------
        # ATUALIZAR O RECORDE
        # ------------------------------------------

        # O recorde é salvo quando a pontuação atual
        # supera o máximo já registrado.
        if self.records.update(self.score):
            self.new_record = True

        # ------------------------------------------
        # CRIAR PARTÍCULAS
        # ------------------------------------------

        self.effects.append(
            ParticleBurst(
                x=item.rect.centerx,
                y=item.rect.centery,
                color=self.feedback_color,
                particle_count=18,
            )
        )

        # Dois segundos de feedback a 60 FPS.
        self.feedback_timer = 120

        self.items_processed += 1

        # ------------------------------------------
        # PROGRESSÃO DE DIFICULDADE
        # ------------------------------------------

        self.level = (
            self.items_processed // 5
        ) + 1

        self.fall_speed = min(
            5.0,
            2.8 + 0.25 * (self.level - 1),
        )

        # ------------------------------------------
        # ANIMAÇÃO DE SAÍDA
        # ------------------------------------------

        item.start_exit()

        self.transition_item = item

        self.current_item = None

        self.spawn_timer = 0

        # ------------------------------------------
        # FIM DA PARTIDA
        # ------------------------------------------

        if self.lives <= 0:

            self.state = self.GAME_OVER

            self.audio.play_game_over()

        # ==================================================
        # DESENHAR TEXTOS
        # ==================================================

    def _draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        center: tuple[int, int] | None = None,
        topleft: tuple[int, int] | None = None,
    ) -> None:
        """Desenha um texto centralizado ou em posição fixa."""

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
        # BOTÕES DO MENU
        # ==================================================

    def _draw_wrapped_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        center: tuple[int, int],
        max_width: int,
        line_spacing: int = 22,
        max_lines: int = 3,
    ) -> None:
        """Desenha um texto em múltiplas linhas dentro de uma largura."""

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            candidate = f"{current_line} {word}".strip()
            if font.size(candidate)[0] <= max_width:
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        lines = lines[:max_lines]
        if len(words) and len(lines) == max_lines:
            rendered_words = " ".join(lines).split()
            if len(rendered_words) < len(words):
                last = lines[-1]
                while last and font.size(last + "...")[0] > max_width:
                    last = last.rsplit(" ", 1)[0] if " " in last else ""
                lines[-1] = (last + "...") if last else "..."

        start_y = center[1] - ((len(lines) - 1) * line_spacing) // 2
        for index, line in enumerate(lines):
            self._draw_text(
                line,
                font,
                color,
                center=(center[0], start_y + index * line_spacing),
            )

    def _draw_menu_button(
        self,
        rect: pygame.Rect,
        label: str,
        hovered: bool,
        border_color: tuple[int, int, int],
    ) -> None:
        """Desenha um botão com resposta visual ao mouse."""

        if hovered:

            background_color = (38, 75, 79)

        else:

            background_color = (20, 39, 52)

        pygame.draw.rect(
            self.screen,
            background_color,
            rect,
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            border_color,
            rect,
            width=2,
            border_radius=12,
        )

        self._draw_text(
            label,
            self.font_button,
            self.WHITE,
            center=rect.center,
        )

        # ==================================================
        # MENU PRINCIPAL
        # ==================================================

    def _draw_menu(self) -> None:
        """Desenha o menu principal interativo."""

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        self._draw_text(
            "EcoDrop",
            self.font_title,
            self.GREEN,
            center=(400, 110),
        )

        self._draw_text(
            "Tetris da Reciclagem",
            self.font_subtitle,
            self.WHITE,
            center=(400, 170),
        )

        self._draw_text(
            "Separe os resíduos e ajude o meio ambiente!",
            self.font_normal,
            self.GRAY,
            center=(400, 220),
        )

        # Recorde persistente.
        self._draw_text(
            f"RECORDE: {self.records.best_score}",
            self.font_normal,
            self.GREEN,
            center=(400, 265),
        )

        # Detectar a posição do mouse.
        mouse_position = pygame.mouse.get_pos()

        self._draw_menu_button(
            rect=self.play_button_rect,
            label="JOGAR",
            hovered=self.play_button_rect.collidepoint(
                mouse_position
            ),
            border_color=self.GREEN,
        )

        self._draw_menu_button(
            rect=self.instructions_button_rect,
            label="INSTRUÇÕES",
            hovered=self.instructions_button_rect.collidepoint(
                mouse_position
            ),
            border_color=(49, 130, 206),
        )

        self._draw_text(
            "Clique em um botão ou use o teclado",
            self.font_small,
            self.GRAY,
            center=(400, 460),
        )

        self._draw_text(
            "ENTER / ESPAÇO: jogar | I: instruções",
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
    # SELEÇÃO DE MODOS
    # ==================================================

    def _draw_mode_select(self) -> None:
        """
        Desenha a tela de seleção dos modos do EcoDrop.
        """

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        self._draw_text(
            "ESCOLHA O MODO",
            self.font_title,
            self.GREEN,
            center=(400, 85),
        )

        self._draw_text(
            "Escolha a experiência que deseja jogar",
            self.font_subtitle,
            self.WHITE,
            center=(400, 135),
        )

        mouse_position = pygame.mouse.get_pos()

        # ----------------------------------------------
        # CARTÃO: RECICLAGEM GERAL
        # ----------------------------------------------

        general_hovered = (
            self.general_mode_rect.collidepoint(
                mouse_position
            )
        )

        general_background = (
            (34, 69, 72)
            if general_hovered
            else (20, 39, 52)
        )

        pygame.draw.rect(
            self.screen,
            general_background,
            self.general_mode_rect,
            border_radius=16,
        )

        pygame.draw.rect(
            self.screen,
            self.GREEN,
            self.general_mode_rect,
            width=3,
            border_radius=16,
        )

        self._draw_text(
            GAME_MODES[MODE_GENERAL]["title"],
            self.font_subtitle,
            self.GREEN,
            center=(220, 235),
        )

        self._draw_text(
            GAME_MODES[MODE_GENERAL]["status"],
            self.font_normal,
            self.WHITE,
            center=(220, 275),
        )

        for index, description in enumerate(
            GAME_MODES[MODE_GENERAL]["description"]
        ):

            self._draw_text(
                description,
                self.font_small,
                self.GRAY,
                center=(220, 320 + index * 30),
            )

        # ----------------------------------------------
        # CARTÃO: LIXO ELETRÔNICO
        # ----------------------------------------------

        electronic_hovered = (
            self.electronic_mode_rect.collidepoint(
                mouse_position
            )
        )

        electronic_background = (
            (43, 57, 79)
            if electronic_hovered
            else (20, 39, 52)
        )

        pygame.draw.rect(
            self.screen,
            electronic_background,
            self.electronic_mode_rect,
            border_radius=16,
        )

        pygame.draw.rect(
            self.screen,
            (49, 130, 206),
            self.electronic_mode_rect,
            width=3,
            border_radius=16,
        )

        self._draw_text(
            GAME_MODES[MODE_ELECTRONIC]["title"],
            self.font_subtitle,
            (100, 180, 255),
            center=(580, 235),
        )

        self._draw_text(
            GAME_MODES[MODE_ELECTRONIC]["status"],
            self.font_normal,
            self.WHITE,
            center=(580, 275),
        )

        for index, description in enumerate(
            GAME_MODES[MODE_ELECTRONIC]["description"]
        ):

            self._draw_text(
                description,
                self.font_small,
                self.GRAY,
                center=(580, 320 + index * 30),
            )

        # ----------------------------------------------
        # BOTÃO VOLTAR
        # ----------------------------------------------

        back_hovered = (
            self.mode_back_button_rect.collidepoint(
                mouse_position
            )
        )

        back_background = (
            (42, 58, 69)
            if back_hovered
            else (20, 39, 52)
        )

        pygame.draw.rect(
            self.screen,
            back_background,
            self.mode_back_button_rect,
            border_radius=10,
        )

        pygame.draw.rect(
            self.screen,
            self.GRAY,
            self.mode_back_button_rect,
            width=1,
            border_radius=10,
        )

        self._draw_text(
            "VOLTAR",
            self.font_normal,
            self.WHITE,
            center=self.mode_back_button_rect.center,
        )

        self._draw_text(
            "1: Reciclagem Geral | 2: Lixo Eletrônico",
            self.font_small,
            self.GRAY,
            center=(400, 535),
        )

        # ==================================================
    # APRESENTAÇÃO DO MODO ELETRÔNICO
    # ==================================================

    def _draw_ewaste_preview(self) -> None:
        """
        Apresenta os objetivos do futuro modo Lixo Eletrônico.
        """

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        self._draw_text(
            "LIXO ELETRÔNICO",
            self.font_title,
            (100, 180, 255),
            center=(400, 90),
        )

        self._draw_text(
            "Uma nova experiência educativa está sendo preparada.",
            self.font_subtitle,
            self.WHITE,
            center=(400, 145),
        )

        # Painel principal.
        panel = pygame.Rect(
            100,
            190,
            600,
            240,
        )

        pygame.draw.rect(
            self.screen,
            (20, 39, 52),
            panel,
            border_radius=16,
        )

        pygame.draw.rect(
            self.screen,
            (49, 130, 206),
            panel,
            width=2,
            border_radius=16,
        )

        # Conteúdo previsto.
        messages = [
            "Avaliar equipamentos que ainda podem ser reutilizados.",
            "Identificar equipamentos que podem passar por reparo.",
            "Encaminhar eletrônicos para destinação apropriada.",
            "Separar pilhas e baterias em pontos que as aceitem.",
            "Proteger os dados antes de destinar dispositivos.",
        ]

        for index, message in enumerate(messages):

            self._draw_text(
                message,
                self.font_small,
                self.WHITE,
                center=(400, 225 + index * 36),
            )

        self._draw_text(
            "MODO EM DESENVOLVIMENTO",
            self.font_normal,
            (100, 180, 255),
            center=(400, 470),
        )

        self._draw_text(
            "Pressione ENTER ou ESC para voltar à seleção",
            self.font_small,
            self.GREEN,
            center=(400, 520),
        )

        # Botão de retorno.
        mouse_position = pygame.mouse.get_pos()

        hovered = self.mode_back_button_rect.collidepoint(
            mouse_position
        )

        background_color = (
            (42, 58, 69)
            if hovered
            else (20, 39, 52)
        )

        pygame.draw.rect(
            self.screen,
            background_color,
            self.mode_back_button_rect,
            border_radius=10,
        )

        pygame.draw.rect(
            self.screen,
            (49, 130, 206),
            self.mode_back_button_rect,
            width=2,
            border_radius=10,
        )

        self._draw_text(
            "VOLTAR",
            self.font_normal,
            self.WHITE,
            center=self.mode_back_button_rect.center,
        )

        # ==================================================
        # TELA DE INSTRUÇÕES
        # ==================================================

    def _draw_instructions(self) -> None:
        """Desenha a tela de instruções."""

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

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

        # Cartão de controles.
        controles_rect = pygame.Rect(
            65, 160, 320, 115
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

        # Cartão de objetivo.
        objetivo_rect = pygame.Rect(
            415, 160, 320, 115
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

        # Cartão de pontuação.
        pontos_rect = pygame.Rect(
            65, 300, 210, 125
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

        # Cartão de erros.
        erros_rect = pygame.Rect(
            295, 300, 210, 125
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

        # Cartão de dificuldade.
        dificuldade_rect = pygame.Rect(
            525, 300, 210, 125
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

        # Categorias.
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

        self._draw_text(
            "A aceitação dos materiais varia conforme a coleta local.",
            self.font_small,
            self.GRAY,
            center=(400, 538),
        )

        self._draw_text(
            "ENTER ou ESC para voltar ao menu",
            self.font_normal,
            self.GREEN,
            center=(400, 568),
        )

        # ==================================================
        # TELA DA PARTIDA
        # ==================================================

    def _draw_game(self) -> None:
        """Desenha o cenário e os elementos da partida."""

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        # Informações da partida.
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

        if self.selected_mode == MODE_ELECTRONIC:
            instruction = "Use as setas para escolher a destinação correta"
            mode_label = "MODO: LIXO ELETRÔNICO"
        else:
            instruction = "Use as setas para escolher a lixeira correta"
            mode_label = "MODO: RECICLAGEM GERAL"

        self._draw_text(
            mode_label,
            self.font_small,
            self.GREEN,
            center=(400, 77),
        )

        self._draw_text(
            instruction,
            self.font_normal,
            self.GRAY,
            center=(400, 105),
        )

        # Feedback de acertos e erros.
        if self.feedback_timer > 0:

            self._draw_text(
                self.feedback_text,
                self.font_small,
                self.feedback_color,
                center=(400, 132),
            )

        # Destaque da coluna selecionada.
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

        # Linhas verticais das colunas.
        for lane_x in self.lane_centers:

            pygame.draw.line(
                self.screen,
                (25, 40, 54),
                (lane_x, 145),
                (lane_x, 455),
                2,
            )

        # Resíduo atual.
        if self.current_item is not None:

            self.current_item.draw(
                self.screen,
                self.font_item,
            )

        # Resíduo em animação de saída.
        if self.transition_item is not None:

            self.transition_item.draw(
                self.screen,
                self.font_item,
            )

        # Lixeiras.
        for bin_object in self.bins:

            bin_object.draw(
                self.screen,
                self.font_bin,
            )

        # Contornos de acerto e erro.
        for lane_index, highlight_color in (
            self.highlighted_bins.items()
        ):

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

        self._draw_text(
            "ESC: voltar ao menu",
            self.font_small,
            self.GRAY,
            center=(400, 583),
        )

        # ==================================================
        # TELA DE FIM DE JOGO
        # ==================================================

    def _draw_quiz(self) -> None:
        """Desenha a pergunta educativa e suas alternativas."""

        self.screen.blit(self.background_surface, (0, 0))

        panel = pygame.Rect(70, 85, 660, 470)
        pygame.draw.rect(
            self.screen, (17, 34, 49), panel, border_radius=18
        )
        pygame.draw.rect(
            self.screen, (49, 130, 206), panel, width=2, border_radius=18
        )

        self._draw_text(
            "DESAFIO DE CONHECIMENTO",
            self.font_title,
            (100, 180, 255),
            center=(400, 135),
        )
        self._draw_text(
            "Atividade opcional: suas respostas não alteram a pontuação da partida",
            self.font_small,
            self.GRAY,
            center=(400, 175),
        )

        if self.current_question is None:
            return

        self._draw_text(
            f"Pergunta {self.quiz_question_index + 1} de {len(self.quiz_questions)}",
            self.font_small,
            (100, 180, 255),
            center=(400, 202),
        )

        self._draw_text(
            self.current_question["question"],
            self.font_normal,
            self.WHITE,
            center=(400, 235),
        )

        mouse_position = pygame.mouse.get_pos()
        correct_index = self.current_question["correct_index"]

        for index, (option, option_rect) in enumerate(zip(
            self.current_question["options"], self.quiz_option_rects
        )):
            background_color = (23, 47, 63)
            border_color = (75, 105, 125)

            if self.quiz_answered and index == correct_index:
                background_color = (24, 83, 65)
                border_color = self.GREEN
            elif (
                self.quiz_answered
                and index == self.quiz_selected_index
                and not self.quiz_was_correct
            ):
                background_color = (91, 43, 48)
                border_color = self.RED
            elif not self.quiz_answered and option_rect.collidepoint(
                mouse_position
            ):
                background_color = (37, 68, 83)
                border_color = (100, 180, 255)

            pygame.draw.rect(
                self.screen, background_color, option_rect, border_radius=10
            )
            pygame.draw.rect(
                self.screen, border_color, option_rect, width=2, border_radius=10
            )

            self._draw_text(
                f"{index + 1}. {option}",
                self.font_normal,
                self.WHITE,
                center=option_rect.center,
            )

        if self.quiz_answered:
            feedback_color = self.GREEN if self.quiz_was_correct else (245, 195, 100)
            self._draw_wrapped_text(
                self.quiz_feedback,
                self.font_small,
                feedback_color,
                center=(400, 460),
                max_width=590,
                line_spacing=20,
                max_lines=2,
            )

            button_hovered = self.quiz_continue_button_rect.collidepoint(
                mouse_position
            )
            button_color = (39, 82, 76) if button_hovered else (24, 58, 56)
            pygame.draw.rect(
                self.screen,
                button_color,
                self.quiz_continue_button_rect,
                border_radius=9,
            )
            pygame.draw.rect(
                self.screen,
                self.GREEN,
                self.quiz_continue_button_rect,
                width=2,
                border_radius=9,
            )
            self._draw_text(
                "CONTINUAR",
                self.font_normal,
                self.WHITE,
                center=self.quiz_continue_button_rect.center,
            )
        else:
            self._draw_text(
                "Clique em uma alternativa ou pressione 1, 2 ou 3",
                self.font_small,
                self.GRAY,
                center=(400, 475),
            )

    def _draw_quiz_result(self) -> None:
        """Apresenta o resultado educativo sem misturá-lo ao recorde do jogo."""

        self.screen.blit(self.background_surface, (0, 0))

        panel = pygame.Rect(100, 100, 600, 420)
        pygame.draw.rect(
            self.screen,
            (20, 36, 52),
            panel,
            border_radius=18,
        )
        pygame.draw.rect(
            self.screen,
            (49, 130, 206),
            panel,
            width=2,
            border_radius=18,
        )

        total_questions = len(self.quiz_questions)
        correct_answers = self.quiz_correct_answers

        self._draw_text(
            "DESAFIO CONCLUÍDO!",
            self.font_title,
            (100, 180, 255),
            center=(400, 195),
        )
        self._draw_text(
            f"Você acertou {correct_answers} de {total_questions} perguntas.",
            self.font_subtitle,
            self.WHITE,
            center=(400, 270),
        )

        if correct_answers == total_questions:
            recognition = "CONQUISTA: GUARDIÃO DOS ELETRÔNICOS"
            recognition_color = self.GREEN
        elif correct_answers >= 4:
            recognition = "CONQUISTA: CONHECEDOR CONSCIENTE"
            recognition_color = self.GREEN
        elif correct_answers >= 2:
            recognition = "CONQUISTA: APRENDIZ AMBIENTAL"
            recognition_color = (245, 195, 80)
        else:
            recognition = "CONTINUE APRENDENDO E FAÇA NOVAS DESCOBERTAS!"
            recognition_color = self.GRAY

        self._draw_text(
            recognition,
            self.font_normal,
            recognition_color,
            center=(400, 335),
        )

        self._draw_text(
            "Este resultado é separado da pontuação e do recorde da partida.",
            self.font_small,
            self.GRAY,
            center=(400, 385),
        )

        mouse_position = pygame.mouse.get_pos()
        hovered = self.quiz_result_button_rect.collidepoint(mouse_position)
        button_color = (39, 82, 76) if hovered else (24, 58, 56)

        pygame.draw.rect(
            self.screen,
            button_color,
            self.quiz_result_button_rect,
            border_radius=9,
        )
        pygame.draw.rect(
            self.screen,
            self.GREEN,
            self.quiz_result_button_rect,
            width=2,
            border_radius=9,
        )
        self._draw_text(
            "VOLTAR AO FIM DE JOGO",
            self.font_small,
            self.WHITE,
            center=self.quiz_result_button_rect.center,
        )

    def _draw_game_over(self) -> None:
        """Desenha a tela de fim de jogo e os recordes."""

        self.screen.blit(
            self.background_surface,
            (0, 0),
        )

        panel = pygame.Rect(
            100, 110, 600, 410
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
            center=(400, 185),
        )

        self._draw_text(
            f"Pontuação final: {self.score}",
            self.font_subtitle,
            self.WHITE,
            center=(400, 250),
        )

        self._draw_text(
            f"Resíduos classificados: {self.items_processed}",
            self.font_normal,
            self.GRAY,
            center=(400, 295),
        )

        if self.new_record:

            self._draw_text(
                "NOVO RECORDE!",
                self.font_normal,
                self.GREEN,
                center=(400, 335),
            )

        else:

            self._draw_text(
                f"Recorde: {self.records.best_score}",
                self.font_normal,
                self.GREEN,
                center=(400, 335),
            )

        self._draw_text(
            "ENTER ou R para jogar novamente",
            self.font_normal,
            self.WHITE,
            center=(400, 390),
        )

        self._draw_text(
            "ESC para voltar ao menu",
            self.font_small,
            self.GRAY,
            center=(400, 430),
        )

        if self.selected_mode == MODE_ELECTRONIC:
            mouse_position = pygame.mouse.get_pos()
            hovered = self.quiz_start_button_rect.collidepoint(mouse_position)
            button_color = (34, 78, 88) if hovered else (22, 53, 68)

            pygame.draw.rect(
                self.screen,
                button_color,
                self.quiz_start_button_rect,
                border_radius=10,
            )
            pygame.draw.rect(
                self.screen,
                (100, 180, 255),
                self.quiz_start_button_rect,
                width=2,
                border_radius=10,
            )
            self._draw_text(
                "DESAFIO DE CONHECIMENTO (OPCIONAL)",
                self.font_small,
                self.WHITE,
                center=self.quiz_start_button_rect.center,
            )
            self._draw_text(
                "Q: iniciar desafio | não altera sua pontuação",
                self.font_small,
                self.GRAY,
                center=(400, 535),
            )

        self._draw_text(
            "Son Games",
            self.font_small,
            self.GRAY,
            center=(400, 575),
        )

        # ==================================================
        # DESENHAR AS TELAS E AS PARTÍCULAS
        # ==================================================

    def _draw(self) -> None:
        """
        Desenha a tela correspondente ao estado atual
        e apresenta as partículas ativas.
        """

        if self.state == self.MENU:

            self._draw_menu()

        elif self.state == self.MODE_SELECT:

            self._draw_mode_select()

        elif self.state == self.EWASTE_PREVIEW:

            self._draw_ewaste_preview()

        elif self.state == self.INSTRUCTIONS:

            self._draw_instructions()

        elif self.state == self.PLAYING:

            self._draw_game()

        elif self.state == self.QUIZ:

            self._draw_quiz()

        elif self.state == self.QUIZ_RESULT:

            self._draw_quiz_result()

        elif self.state == self.GAME_OVER:

            self._draw_game_over()

        # Mantém as animações de partículas.
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
        Executa o ciclo principal do EcoDrop.

        Processa eventos, atualiza a lógica, desenha
        a tela e mantém a taxa de atualização definida.
        """

        while self.running:

            self._handle_events()

            self._update()

            self._draw()

            self.clock.tick(
                self.FPS
            )
