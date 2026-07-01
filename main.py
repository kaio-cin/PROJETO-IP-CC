import pygame 
from pygame.locals import *
from sys import exit

pygame.init()

from game.constantes import *
from game.tela import *
from game.musicas import *
from game.classes import *
from game.players import Fred, Stefan
from game.funcoes import spawnar_dois_coletaveis, spawnar_easter_eggs, desenhar_game_over, desenhar_tela_inicio, desenhar_vitoria, atualizar_coletaveis_ao_mudar_nivel, ocorreu_colisoes, mostrar_quantidade_coletaveis, reiniciar_jogo
from game import constantes

easter_eggs_nao_pegos = spawnar_easter_eggs()
normais_ativos = spawnar_dois_coletaveis(portas_restantes)

coletaveis_totais_naopegos = easter_eggs_nao_pegos + normais_ativos

while True:
    clock.tick(60)
    tela.blit(mapa, (0, 0))
    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if boleanas['tela_inicio'] and event.key == pygame.K_SPACE:
                boleanas['tela_inicio'] = False
                boleanas['tempo_inicio'] = pygame.time.get_ticks()

            elif (boleanas['game_over'] or boleanas['vitoria']) and event.key == pygame.K_r:
                reiniciar_jogo(coletaveis_totais_naopegos, normais_ativos, easter_eggs_nao_pegos)
    
    constantes.mensagens_ativas[:] = [msg for msg in constantes.mensagens_ativas if pygame.time.get_ticks() < msg['fim']]

    fonte_mensagens = pygame.font.SysFont(None, 32)
    pos_x_mensagens = 10  # um pouco mais pra esquerda
    pos_y_base_mensagens = 40  # perto do rodapé da tela

    for i, msg in enumerate(constantes.mensagens_ativas):
        texto = fonte_mensagens.render(msg['texto'], True, msg['cor'])
        # desenha de baixo pra cima: a mais nova fica embaixo, a mais antiga sobe
        tela.blit(texto, (pos_x_mensagens, pos_y_base_mensagens + i * 30))

    if boleanas['tela_inicio']:
        desenhar_tela_inicio(tela)
        pygame.display.update()
        continue

    elif boleanas['game_over']:
        desenhar_game_over(tela)
        pygame.display.update()
        musica_fundo.stop()
        if not boleanas['tocou_som_derrota']:
            boleanas['tocou_som_derrota'] = True
            som_derrota.play(0)
        continue

    elif boleanas['vitoria']:
        desenhar_vitoria(tela)
        pygame.display.update()
        musica_fundo.stop()
        if not boleanas['tocou_som_vitoria']: #o som toca apenas uma vez 
            boleanas['tocou_som_vitoria'] = True
            som_vitoria.play(0)
        continue

    else:
        if not boleanas['nivel1_completo']:
            nivel_atual = 0

        else:
            if not boleanas['nivel2_completo']:
                nivel_atual = 1

            else:
                nivel_atual = 2

        if nivel_atual != boleanas['nivel_anterior']:
            boleanas['nivel_anterior'] = nivel_atual
            atualizar_coletaveis_ao_mudar_nivel(coletaveis_totais_naopegos, normais_ativos, easter_eggs_nao_pegos)

    if boleanas['tempo_inicio'] is not None:
        tempo_passado = pygame.time.get_ticks() - boleanas['tempo_inicio']
    else:
        tempo_passado = 0

    tempo_restante = max(0, limite - tempo_passado) #o max evita tempo negativo
    
    segundos_restantes = tempo_restante // 1000

    minutos = segundos_restantes // 60
    segundos = segundos_restantes % 60

    if tempo_restante == 0 and not (boleanas['nivel1_completo'] and boleanas['nivel2_completo'] and boleanas['nivel3_completo']):
        boleanas['game_over'] = True

    if boleanas['nivel1_completo'] and boleanas['nivel2_completo'] and boleanas['nivel3_completo']:
        boleanas['vitoria'] = True
    
    texto_tempo = fonte.render(f'{minutos:02d}:{segundos:02d}', True, (255, 255, 255))
    
    pos_cronometro = (largura - 100, 10)
    tela.blit(texto_tempo, pos_cronometro)    #posição x=1350, y=10 (canto superior direito)

    ocorreu_colisoes(Fred, coletaveis_totais_naopegos, normais_ativos)
    ocorreu_colisoes(Stefan, coletaveis_totais_naopegos, normais_ativos)

    for coletavel in coletaveis_totais_naopegos:
        coletavel.desenhar(tela)
            
    teclas = pygame.key.get_pressed()
    Fred.mover(teclas)
    Fred.atualizar_animacao()
    
    Stefan.mover(teclas)
    Stefan.atualizar_animacao()


    Fred.desenhar(tela)
    Stefan.desenhar(tela)

    mostrar_quantidade_coletaveis(tela)
  

    pygame.display.update()                                 