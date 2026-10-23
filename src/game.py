import random
import pygame

from src.audio import AudioManager
from src.bin import Bin
from src.effects import ParticleBurst
from src.item import WasteItem


class EcoDropGame:
    """
    Controla o funcionamento principal do EcoDrop.

    Estados do jogo:
        MENU: menu principal.
        PLAYING: partida em andamento.
        GAME_OVER: fim da partida.
    """

    MENU = "menu"
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

    def __init__(self) -> None:
        """
        Inicializa a janela, as fontes, o áudio,
        as lixeiras e as configurações principais.
        """

        # --------------------------------------------------
        # JANELA E RELÓGIO
        # --------------------------------------------------

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "EcoDrop | Son Games"
        )

        self.clock = pygame.time.Clock()

        # --------------------------------------------------
        # ÁUDIO
        # --------------------------------------------------

        self.audio = AudioManager()

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
        # CATEGORIAS DAS LIXEIRAS
        # --------------------------------------------------

        bin_data = [
            ("papel", "PAPEL", (49, 130, 206)),
            ("plastico", "PLÁSTICO", (220, 66, 66)),
            ("vidro", "VIDRO", (46, 160, 100)),
            ("metal", "METAL", (225, 170, 45)),
            ("organico", "ORGÂNICOS", (133, 94, 66)),
        ]

        # Cria as cinco lixeiras.
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

        # --------------------------------------------------
        # RESÍDUOS DISPONÍVEIS
        # --------------------------------------------------

        # O primeiro elemento é o nome exibido.
        # O segundo elemento é a categoria interna.
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

    # ======================================================
    # CONTROLE DA PARTIDA
    # ======================================================

    def _reset_round(self) -> None:
        """
        Inicializa ou reinicia os dados de uma partida.
        """

        self.score = 0
        self.lives = 3
        self.combo = 0

        self.items_processed = 0
        self.level = 1

        self.fall_speed = 2.8

        self.current_item = None
        self.current_lane = 2

        self.spawn_timer = 0

        # Feedback de acertos e erros.
        self.feedback_text = ""
        self.feedback_color = self.WHITE
        self.feedback_timer = 0

        # Destaques temporários das lixeiras.
        self.highlighted_bins = {}

        # Animações de partículas ativas.
        self.effects = []

    def _start_game(self) -> None:
        """
        Inicia uma nova partida.
        """

        self._reset_round()

        self.state = self.PLAYING

        # Efeito sonoro de início.
        self.audio.play_start()

        # Cria o primeiro resíduo.
        self._spawn_item()

    def _spawn_item(self) -> None:
        """
        Cria um resíduo em uma coluna inicial aleatória.
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

    def _move_lane(self, direction: int) -> None:
        """
        Define a coluna de destino do resíduo.

        direction:
            -1 significa esquerda.
             1 significa direita.
        """

        new_lane = max(
            0,
            min(
                len(self.bins) - 1,
                self.current_lane + direction,
            ),
        )

        # Não permite ultrapassar as extremidades.
        if new_lane == self.current_lane:
            return

        self.current_lane = new_lane

        # Solicita o movimento horizontal suave.
        if self.current_item is not None:

            lane_x = self.lane_centers[
                self.current_lane
            ]

            self.current_item.move_to_x(
                lane_x
            )

    # ======================================================
    # EVENTOS DO TECLADO
    # ======================================================

    def _handle_events(self) -> None:
        """
        Processa os eventos da janela e do teclado.
        """

        for event in pygame.event.get():

            # Encerrar o jogo pela janela.
            if event.type == pygame.QUIT:
                self.running = False
                continue

            # Processamos apenas teclas pressionadas.
            if event.type != pygame.KEYDOWN:
                continue

            # --------------------------------------------------
            # MENU
            # --------------------------------------------------

            if self.state == self.MENU:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                ):
                    self._start_game()

            # --------------------------------------------------
            # PARTIDA
            # --------------------------------------------------

            elif self.state == self.PLAYING:

                if event.key == pygame.K_ESCAPE:

                    self.state = self.MENU

                    self.current_item = None

                    self.highlighted_bins.clear()
                    self.effects.clear()

                elif event.key == pygame.K_LEFT:

                    self._move_lane(-1)

                elif event.key == pygame.K_RIGHT:

                    self._move_lane(1)

            # --------------------------------------------------
            # FIM DE JOGO
            # --------------------------------------------------

            elif self.state == self.GAME_OVER:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_r,
                ):
                    self._start_game()

                elif event.key == pygame.K_ESCAPE:

                    self.state = self.MENU

                    self.highlighted_bins.clear()
                    self.effects.clear()

    # ======================================================
    # ATUALIZAÇÃO DA LÓGICA
    # ======================================================

    def _update(self) -> None:
        """
        Atualiza as partículas, os feedbacks e a partida.
        """

        # --------------------------------------------------
        # ATUALIZAR PARTÍCULAS
        # --------------------------------------------------

        for effect in self.effects:
            effect.update()

        # Remove as animações que terminaram.
        self.effects = [
            effect
            for effect in self.effects
            if not effect.finished
        ]

        # --------------------------------------------------
        # ATUALIZAR FEEDBACK VISUAL
        # --------------------------------------------------

        if self.feedback_timer > 0:

            self.feedback_timer -= 1

            # Remove os destaques quando o tempo termina.
            if self.feedback_timer == 0:

                self.highlighted_bins.clear()

        # --------------------------------------------------
        # LÓGICA DA PARTIDA
        # --------------------------------------------------

        if self.state != self.PLAYING:
            return

        # Cria outro resíduo quando necessário.
        if self.current_item is None:

            self.spawn_timer += 1

            if self.spawn_timer >= 45:
                self._spawn_item()

            return

        # Atualiza os movimentos vertical e horizontal.
        self.current_item.update()

        # Verifica se o resíduo alcançou a região das lixeiras.
        if (
            self.current_item.rect.bottom
            >= self.bins[0].rect.top
        ):
            self._resolve_item()

    # ======================================================
    # CLASSIFICAÇÃO DOS RESÍDUOS
    # ======================================================

    def _resolve_item(self) -> None:
        """
        Verifica a classificação, atualiza a pontuação
        e cria o feedback visual e sonoro.
        """

        if self.current_item is None:
            return

        item = self.current_item

        # --------------------------------------------------
        # ENCONTRAR A LIXEIRA MAIS PRÓXIMA
        # --------------------------------------------------

        # Considera a posição real do resíduo durante
        # o movimento horizontal suave.
        landed_lane = min(
            range(len(self.lane_centers)),
            key=lambda index: abs(
                item.x - self.lane_centers[index]
            ),
        )

        target_bin = self.bins[landed_lane]

        # --------------------------------------------------
        # ENCONTRAR A CATEGORIA CORRETA
        # --------------------------------------------------

        correct_lane = next(
            index
            for index, bin_object in enumerate(self.bins)
            if bin_object.category == item.category
        )

        correct_bin = self.bins[correct_lane]

        # --------------------------------------------------
        # ACERTO
        # --------------------------------------------------

        if item.category == target_bin.category:

            # Destaca a lixeira escolhida em verde.
            self.highlighted_bins = {
                landed_lane: self.GREEN
            }

            # Combo consecutivo.
            self.combo += 1

            # A recompensa aumenta com o combo.
            points = 100 * self.combo

            self.score += points

            # Mensagem de confirmação.
            self.feedback_text = (
                f"Correto! {item.name} -> "
                f"{target_bin.label} (+{points})"
            )

            self.feedback_color = self.GREEN

            # Efeito sonoro de acerto.
            self.audio.play_correct()

        # --------------------------------------------------
        # ERRO
        # --------------------------------------------------

        else:

            # A lixeira escolhida fica vermelha.
            # A lixeira correta fica verde.
            self.highlighted_bins = {
                landed_lane: self.RED,
                correct_lane: self.GREEN,
            }

            # Perde uma vida e reinicia o combo.
            self.lives -= 1
            self.combo = 0

            # Orientação educativa.
            self.feedback_text = (
                f"Incorreto! {item.name} vai em "
                f"{correct_bin.label}."
            )

            self.feedback_color = self.RED

            # O último erro toca o som de fim de jogo.
            if self.lives > 0:
                self.audio.play_error()

        # --------------------------------------------------
        # ANIMAÇÃO DE PARTÍCULAS
        # --------------------------------------------------

        self.effects.append(
            ParticleBurst(
                x=item.rect.centerx,
                y=item.rect.centery,
                color=self.feedback_color,
                particle_count=18,
            )
        )

        # --------------------------------------------------
        # TEMPORIZADORES
        # --------------------------------------------------

        # Tempo aproximado de 0,75 segundo a 60 FPS.
        self.feedback_timer = 45

        # Registra o resíduo classificado.
        self.items_processed += 1

        # --------------------------------------------------
        # PROGRESSÃO DE DIFICULDADE
        # --------------------------------------------------

        # O nível aumenta a cada cinco resíduos.
        self.level = (
            self.items_processed // 5
        ) + 1

        # A velocidade cresce gradualmente.
        # O limite evita que a queda fique rápida demais.
        self.fall_speed = min(
            5.0,
            2.8 + 0.25 * (self.level - 1),
        )

        # Remove o resíduo resolvido.
        self.current_item = None

        self.spawn_timer = 0

        # --------------------------------------------------
        # FIM DA PARTIDA
        # --------------------------------------------------

        if self.lives <= 0:

            self.state = self.GAME_OVER

            # Som de encerramento.
            self.audio.play_game_over()

    # ======================================================
    # FUNÇÃO AUXILIAR PARA TEXTOS
    # ======================================================

    def _draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        center: tuple[int, int] | None = None,
        topleft: tuple[int, int] | None = None,
    ) -> None:
        """
        Desenha um texto centralizado ou em uma posição fixa.
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

    # ======================================================
    # DESENHO DO MENU
    # ======================================================

    def _draw_menu(self) -> None:
        """
        Desenha o menu principal.
        """

        self.screen.fill(
            self.BACKGROUND
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
            "Use as setas durante a partida para escolher a lixeira.",
            self.font_small,
            self.GRAY,
            center=(400, 465),
        )

        self._draw_text(
            "Son Games | Projeto em desenvolvimento",
            self.font_small,
            self.GRAY,
            center=(400, 570),
        )

    # ======================================================
    # DESENHO DA PARTIDA
    # ======================================================

    def _draw_game(self) -> None:
        """
        Desenha a interface e os objetos da partida.
        """

        self.screen.fill(
            self.BACKGROUND
        )

        # --------------------------------------------------
        # PAINEL DE INFORMAÇÕES
        # --------------------------------------------------

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

        # --------------------------------------------------
        # INSTRUÇÕES
        # --------------------------------------------------

        self._draw_text(
            "Use as setas para colocar o resíduo na lixeira correta",
            self.font_normal,
            self.GRAY,
            center=(400, 88),
        )

        # --------------------------------------------------
        # FEEDBACK
        # --------------------------------------------------

        if self.feedback_timer > 0:

            self._draw_text(
                self.feedback_text,
                self.font_small,
                self.feedback_color,
                center=(400, 124),
            )

        # --------------------------------------------------
        # COLUNAS
        # --------------------------------------------------

        for lane_x in self.lane_centers:

            pygame.draw.line(
                self.screen,
                (25, 40, 54),
                (lane_x, 145),
                (lane_x, 455),
                2,
            )

        # --------------------------------------------------
        # RESÍDUO ATUAL
        # --------------------------------------------------

        if self.current_item is not None:

            self.current_item.draw(
                self.screen,
                self.font_item,
            )

        # --------------------------------------------------
        # LIXEIRAS
        # --------------------------------------------------

        for bin_object in self.bins:

            bin_object.draw(
                self.screen,
                self.font_bin,
            )

        # --------------------------------------------------
        # DESTAQUES COLORIDOS
        # --------------------------------------------------

        for (
            lane_index,
            highlight_color,
        ) in self.highlighted_bins.items():

            bin_rect = self.bins[lane_index].rect

            # Cria um contorno externo.
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

        # --------------------------------------------------
        # RODAPÉ
        # --------------------------------------------------

        self._draw_text(
            "ESC: voltar ao menu",
            self.font_small,
            self.GRAY,
            center=(400, 583),
        )

    # ======================================================
    # DESENHO DO FIM DE JOGO
    # ======================================================

    def _draw_game_over(self) -> None:
        """
        Desenha a tela de fim de jogo.
        """

        self.screen.fill(
            self.BACKGROUND
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
            "Pressione ENTER ou R para jogar novamente",
            self.font_normal,
            self.WHITE,
            center=(400, 380),
        )

        self._draw_text(
            "Pressione ESC para voltar ao menu",
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

    # ======================================================
    # DESENHO DA TELA ATUAL E DOS EFEITOS
    # ======================================================

    def _draw(self) -> None:
        """
        Desenha a tela atual e as animações de partículas.
        """

        if self.state == self.MENU:

            self._draw_menu()

        elif self.state == self.PLAYING:

            self._draw_game()

        elif self.state == self.GAME_OVER:

            self._draw_game_over()

        # As partículas são desenhadas por cima da tela.
        # Isso também permite que terminem de animar
        # durante a transição para o fim de jogo.
        for effect in self.effects:

            effect.draw(
                self.screen
            )

        # Atualiza a janela.
        pygame.display.flip()

    # ======================================================
    # LOOP PRINCIPAL
    # ======================================================

    def run(self) -> None:
        """
        Executa o loop principal do EcoDrop.
        """

        while self.running:

            self._handle_events()

            self._update()

            self._draw()

            self.clock.tick(
                self.FPS
            )
