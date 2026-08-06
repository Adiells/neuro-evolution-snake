import pygame

LARGURA_CELULA = 20
ALTURA_CABECALHO = 60

# Cores
COR_BG = (15, 23, 42)          # Slate 900
COR_GRADE = (30, 41, 59)       # Slate 800
COR_CABECALHO = (30, 41, 59)
COR_TEXTO = (241, 245, 249)    # Slate 100
COR_TEXTO_SEC = (148, 163, 184)# Slate 400
COR_CABECA = (56, 189, 248)    # Sky 400
COR_CORPO = (14, 165, 233)     # Sky 500
COR_MACA = (244, 63, 94)       # Rose 500

def obter_tamanho_tela(largura_grelha, altura_grelha):
    return (largura_grelha * LARGURA_CELULA, altura_grelha * LARGURA_CELULA + ALTURA_CABECALHO)

def desenhar_jogo(tela, jogo, fonte_titulo, fonte_sub):
    # 1. Limpar tela
    tela.fill(COR_BG)

    # 2. Desenhar cabeçalho
    largura_tela = jogo.largura * LARGURA_CELULA
    pygame.draw.rect(tela, COR_CABECALHO, (0, 0, largura_tela, ALTURA_CABECALHO))

    # Desenhar linha divisória
    pygame.draw.line(tela, (71, 85, 105), (0, ALTURA_CABECALHO - 1), (largura_tela, ALTURA_CABECALHO - 1), 1)

    # Textos do cabeçalho
    if fonte_titulo is not None:
        try:
            txt_score = fonte_titulo.render(f"SCORE: {jogo.score}", True, COR_TEXTO)
            tela.blit(txt_score, (20, 10))
        except Exception:
            pass

    if fonte_sub is not None:
        try:
            txt_passos = fonte_sub.render(f"PASSOS: {jogo.passos}", True, COR_TEXTO_SEC)
            tela.blit(txt_passos, (largura_tela - txt_passos.get_width() - 20, 20))
        except Exception:
            pass

    # 3. Desenhar grade
    for x in range(jogo.largura):
        for y in range(jogo.altura):
            rect = (x * LARGURA_CELULA, ALTURA_CABECALHO + y * LARGURA_CELULA, LARGURA_CELULA, LARGURA_CELULA)
            pygame.draw.rect(tela, COR_GRADE, rect, 1)

    # 4. Desenhar Maçã
    if jogo.maca:
        mx, my = jogo.maca
        centro = (mx * LARGURA_CELULA + LARGURA_CELULA // 2, ALTURA_CABECALHO + my * LARGURA_CELULA + LARGURA_CELULA // 2)
        raio = LARGURA_CELULA // 2 - 2
        # Corpo da maçã
        pygame.draw.circle(tela, COR_MACA, centro, raio)
        # Detalhe brilhante
        pygame.draw.circle(tela, (255, 255, 255), (centro[0] - 2, centro[1] - 2), 2)

    # 5. Desenhar Cobra
    for i, (cx, cy) in enumerate(jogo.corpo):
        rect = (cx * LARGURA_CELULA + 1, ALTURA_CABECALHO + cy * LARGURA_CELULA + 1, LARGURA_CELULA - 2, LARGURA_CELULA - 2)
        if i == 0:
            # Cabeça
            pygame.draw.rect(tela, COR_CABECA, rect, border_radius=6)
            
            # Olhos da cobra para dar carisma
            dx, dy = jogo.direcao
            px, py = cx * LARGURA_CELULA, ALTURA_CABECALHO + cy * LARGURA_CELULA
            
            # Desenhar olhinhos dependendo da direção
            cor_olho = (15, 23, 42)
            if dx == 1:   # Leste
                pygame.draw.circle(tela, cor_olho, (px + 14, py + 6), 2)
                pygame.draw.circle(tela, cor_olho, (px + 14, py + 14), 2)
            elif dx == -1: # Oeste
                pygame.draw.circle(tela, cor_olho, (px + 6, py + 6), 2)
                pygame.draw.circle(tela, cor_olho, (px + 6, py + 14), 2)
            elif dy == 1:  # Sul
                pygame.draw.circle(tela, cor_olho, (px + 6, py + 14), 2)
                pygame.draw.circle(tela, cor_olho, (px + 14, py + 14), 2)
            elif dy == -1: # Norte
                pygame.draw.circle(tela, cor_olho, (px + 6, py + 6), 2)
                pygame.draw.circle(tela, cor_olho, (px + 14, py + 6), 2)
        else:
            # Corpo
            # Interpolação de cor opcional para gradiente
            # Reduz a intensidade da cor ao longo do corpo
            factor = max(0.5, 1.0 - (i / len(jogo.corpo)) * 0.5)
            cor_corpo_grad = (
                int(COR_CORPO[0] * factor),
                int(COR_CORPO[1] * factor),
                int(COR_CORPO[2] * factor)
            )
            pygame.draw.rect(tela, cor_corpo_grad, rect, border_radius=4)
