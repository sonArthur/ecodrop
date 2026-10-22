import pygame

from src.bin import Bin


# ==================================================
# 1. INICIALIZAÇÃO
# ==================================================

pygame.init()


# ==================================================
# 2. CONFIGURAÇÕES DO JOGO
# ==================================================

LARGURA = 800
ALTURA = 600
FPS = 60

FUNDO = (10, 20, 35)
VERDE = (52, 211, 153)
BRANCO = (245, 245, 245)
CINZA = (150, 165, 180)

# Cores de identificação das categorias.
AZUL_PAPEL = (49, 130, 206)
VERMELHO_PLASTICO = (220, 66, 66)
VERDE_VIDRO = (46, 160, 100)
AMARELO_METAL = (225, 170, 45)
MARROM_ORGANICOS = (133, 94, 66)


# ==================================================
# 3. CRIAÇÃO DA JANELA
# ==================================================

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption(
    "EcoDrop | Son Games"
)

relogio = pygame.time.Clock()


# ==================================================
# 4. FONTES
# ==================================================

fonte_titulo = pygame.font.Font(None, 64)
fonte_subtitulo = pygame.font.Font(None, 30)
fonte_instrucao = pygame.font.Font(None, 25)
fonte_categoria = pygame.font.Font(None, 25)
fonte_rodape = pygame.font.Font(None, 20)


# ==================================================
# 5. CRIAÇÃO DAS LIXEIRAS
# ==================================================

LARGURA_LIXEIRA = 136
ALTURA_LIXEIRA = 120

POSICAO_Y_LIXEIRAS = 390
ESPACAMENTO = 16
POSICAO_X_INICIAL = 28

lixeiras = [
    Bin(
        POSICAO_X_INICIAL,
        POSICAO_Y_LIXEIRAS,
        LARGURA_LIXEIRA,
        ALTURA_LIXEIRA,
        "papel",
        "PAPEL",
        AZUL_PAPEL
    ),

    Bin(
        POSICAO_X_INICIAL + (LARGURA_LIXEIRA + ESPACAMENTO),
        POSICAO_Y_LIXEIRAS,
        LARGURA_LIXEIRA,
        ALTURA_LIXEIRA,
        "plastico",
        "PLÁSTICO",
        VERMELHO_PLASTICO
    ),

    Bin(
        POSICAO_X_INICIAL + 2 * (LARGURA_LIXEIRA + ESPACAMENTO),
        POSICAO_Y_LIXEIRAS,
        LARGURA_LIXEIRA,
        ALTURA_LIXEIRA,
        "vidro",
        "VIDRO",
        VERDE_VIDRO
    ),

    Bin(
        POSICAO_X_INICIAL + 3 * (LARGURA_LIXEIRA + ESPACAMENTO),
        POSICAO_Y_LIXEIRAS,
        LARGURA_LIXEIRA,
        ALTURA_LIXEIRA,
        "metal",
        "METAL",
        AMARELO_METAL
    ),

    Bin(
        POSICAO_X_INICIAL + 4 * (LARGURA_LIXEIRA + ESPACAMENTO),
        POSICAO_Y_LIXEIRAS,
        LARGURA_LIXEIRA,
        ALTURA_LIXEIRA,
        "organico",
        "ORGÂNICOS",
        MARROM_ORGANICOS
    )
]


# ==================================================
# 6. LOOP PRINCIPAL
# ==================================================

executando = True

while executando:

    # ----------------------------------------------
    # PROCESSAMENTO DOS EVENTOS
    # ----------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

    # ----------------------------------------------
    # DESENHO DO FUNDO
    # ----------------------------------------------

    tela.fill(FUNDO)

    # ----------------------------------------------
    # TÍTULO
    # ----------------------------------------------

    titulo = fonte_titulo.render(
        "EcoDrop",
        True,
        VERDE
    )

    tela.blit(
        titulo,
        titulo.get_rect(
            center=(LARGURA // 2, 75)
        )
    )

    # ----------------------------------------------
    # SUBTÍTULO
    # ----------------------------------------------

    subtitulo = fonte_subtitulo.render(
        "Tetris da Reciclagem",
        True,
        BRANCO
    )

    tela.blit(
        subtitulo,
        subtitulo.get_rect(
            center=(LARGURA // 2, 125)
        )
    )

    # ----------------------------------------------
    # INSTRUÇÃO
    # ----------------------------------------------

    instrucao = fonte_instrucao.render(
        "Conheça as categorias de resíduos",
        True,
        CINZA
    )

    tela.blit(
        instrucao,
        instrucao.get_rect(
            center=(LARGURA // 2, 195)
        )
    )

    # ----------------------------------------------
    # ÁREA DE SEPARAÇÃO
    # ----------------------------------------------

    for lixeira in lixeiras:
        lixeira.draw(
            tela,
            fonte_categoria
        )

    # ----------------------------------------------
    # RODAPÉ
    # ----------------------------------------------

    rodape = fonte_rodape.render(
        "Desenvolvido por Arthur",
        True,
        CINZA
    )

    tela.blit(
        rodape,
        rodape.get_rect(
            center=(LARGURA // 2, 560)
        )
    )

    # ----------------------------------------------
    # ATUALIZAÇÃO DA TELA
    # ----------------------------------------------

    pygame.display.flip()

    # Mantém a execução próxima de 60 FPS.
    relogio.tick(FPS)


# ==================================================
# 7. ENCERRAMENTO
# ==================================================

pygame.quit()
