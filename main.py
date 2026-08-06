import pygame
import sys
from jogo import JogoCobrinha
import visualizacao

def main():
    # Inicialização do Pygame
    pygame.init()
    try:
        pygame.font.init()
    except (ImportError, NotImplementedError, AttributeError) as e:
        print(f"Aviso: Módulo de fontes do Pygame não disponível ({e}). O jogo rodará sem exibir textos na tela.")

    # Dimensões do jogo
    largura_grelha = 20
    altura_grelha = 20
    fps = 10

    # Criar instâncias do jogo
    jogo = JogoCobrinha(largura_grelha, altura_grelha)
    largura_tela, altura_tela = visualizacao.obter_tamanho_tela(largura_grelha, altura_grelha)
    
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Cobrinha IA - Modo Manual")
    
    clock = pygame.time.Clock()

    # Fontes
    fonte_titulo = None
    fonte_sub = None
    fonte_overlay = None
    fonte_overlay_sub = None

    try:
        fonte_titulo = pygame.font.SysFont("Segoe UI", 24, bold=True)
        fonte_sub = pygame.font.SysFont("Segoe UI", 14)
        fonte_overlay = pygame.font.SysFont("Segoe UI", 28, bold=True)
        fonte_overlay_sub = pygame.font.SysFont("Segoe UI", 16)
    except Exception:
        try:
            fonte_titulo = pygame.font.Font(None, 28)
            fonte_sub = pygame.font.Font(None, 18)
            fonte_overlay = pygame.font.Font(None, 34)
            fonte_overlay_sub = pygame.font.Font(None, 20)
        except Exception:
            pass

    direcao_desejada = None
    pausado = False

    while True:
        # 1. Capturar Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                # Controles de direção
                if event.key in (pygame.K_UP, pygame.K_w):
                    direcao_desejada = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    direcao_desejada = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    direcao_desejada = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    direcao_desejada = (1, 0)
                
                # Outros comandos
                elif event.key == pygame.K_r:
                    jogo.reset()
                    direcao_desejada = None
                    pausado = False
                elif event.key in (pygame.K_SPACE, pygame.K_p):
                    if not jogo.fim_de_jogo:
                        pausado = not pausado

        # 2. Atualizar Estado do Jogo (se não estiver pausado ou fim de jogo)
        if not pausado and not jogo.fim_de_jogo:
            score_anterior = jogo.score
            jogo.passo(direcao_desejada)
            direcao_desejada = jogo.direcao
            
            if jogo.score > score_anterior:
                print(f"🍎 Maçã comida! Score: {jogo.score} | Passos: {jogo.passos}")
            if jogo.fim_de_jogo:
                print(f"💀 Fim de jogo! Score final: {jogo.score} | Passos sobrevivência: {jogo.passos}")

        # 3. Desenhar Tela
        visualizacao.desenhar_jogo(tela, jogo, fonte_titulo, fonte_sub)

        # Overlay de Fim de Jogo
        if jogo.fim_de_jogo:
            overlay = pygame.Surface((largura_tela, altura_tela - visualizacao.ALTURA_CABECALHO))
            overlay.set_alpha(200)
            overlay.fill((15, 23, 42))  # Cor Slate 900 semi-transparente
            tela.blit(overlay, (0, visualizacao.ALTURA_CABECALHO))

            if fonte_overlay is not None and fonte_overlay_sub is not None:
                try:
                    txt_gameover = fonte_overlay.render("FIM DE JOGO", True, (244, 63, 94)) # Rose 500
                    txt_restart = fonte_overlay_sub.render("Pressione R para reiniciar", True, (241, 245, 249))

                    pos_gameover = (largura_tela // 2 - txt_gameover.get_width() // 2, 
                                    visualizacao.ALTURA_CABECALHO + (altura_tela - visualizacao.ALTURA_CABECALHO) // 2 - 30)
                    pos_restart = (largura_tela // 2 - txt_restart.get_width() // 2, 
                                   visualizacao.ALTURA_CABECALHO + (altura_tela - visualizacao.ALTURA_CABECALHO) // 2 + 10)

                    tela.blit(txt_gameover, pos_gameover)
                    tela.blit(txt_restart, pos_restart)
                except Exception:
                    pass

        # Overlay de Pausa
        elif pausado:
            overlay = pygame.Surface((largura_tela, altura_tela - visualizacao.ALTURA_CABECALHO))
            overlay.set_alpha(180)
            overlay.fill((15, 23, 42))
            tela.blit(overlay, (0, visualizacao.ALTURA_CABECALHO))

            if fonte_overlay is not None and fonte_overlay_sub is not None:
                try:
                    txt_pausado = fonte_overlay.render("PAUSADO", True, (56, 189, 248)) # Sky 400
                    txt_continuar = fonte_overlay_sub.render("Pressione ESPAÇO para continuar", True, (241, 245, 249))

                    pos_pausado = (largura_tela // 2 - txt_pausado.get_width() // 2, 
                                   visualizacao.ALTURA_CABECALHO + (altura_tela - visualizacao.ALTURA_CABECALHO) // 2 - 30)
                    pos_continuar = (largura_tela // 2 - txt_continuar.get_width() // 2, 
                                     visualizacao.ALTURA_CABECALHO + (altura_tela - visualizacao.ALTURA_CABECALHO) // 2 + 10)

                    tela.blit(txt_pausado, pos_pausado)
                    tela.blit(txt_continuar, pos_continuar)
                except Exception:
                    pass

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
