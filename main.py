
import pygame

# Inicializa os módulos do Pygame.
pygame.init()

# Configurações da janela.
LARGURA = 800
ALTURA = 600
FPS = 60

# Paleta de cores inicial.
FUNDO = (10, 20, 35)
VERDE = (52, 211, 153)
BRANCO = (245, 245, 245)

# Cria a janela do jogo.
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("EcoDrop - Tetris da Reciclagem")

# Relógio para controlar a taxa de atualização.
relogio = pygame.time.Clock()

# Fonte para os textos.
fonte_titulo = pygame.font.Font(None, 64)
fonte_subtitulo = pygame.font.Font(None, 28)

executando = True

while executando:
    # Processa eventos, como fechar a janela.
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # Desenha o fundo.
    tela.fill(FUNDO)

    # Desenha o título.
    titulo = fonte_titulo.render(
        "EcoDrop", True, VERDE
    )
    tela.blit(
        titulo,
        titulo.get_rect(center=(LARGURA // 2, 230))
    )

    # Desenha o subtítulo.
    subtitulo = fonte_subtitulo.render(
        "Tetris da Reciclagem", True, BRANCO
    )
    tela.blit(
        subtitulo,
        subtitulo.get_rect(center=(LARGURA // 2, 285))
    )

    # Atualiza a tela.
    pygame.display.flip()

    # Mantém o jogo próximo de 60 FPS.
    relogio.tick(FPS)

# Encerra o Pygame corretamente.
pygame.quit()
