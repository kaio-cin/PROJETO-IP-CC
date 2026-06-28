import pygame 
from pygame.locals import *
from sys import exit

pygame.init()

from constantes import *
from tela import *
from game.musicas import *
from classes import *
from players import Fred, Stefan
from funcoes import spawnar_dois_coletaveis, spawnar_easter_eggs, desenhar_game_over, desenhar_tela_inicio, desenhar_vitoria, atualizar_coletaveis_ao_mudar_nivel, ocorreu_colisoes, mostrar_quantidade_coletaveis, reiniciar_jogo

easter_eggs_nao_pegos = spawnar_easter_eggs()
portas_restantes = portas.copy()
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
            if tela_inicio and event.key == pygame.K_SPACE:
                tela_inicio = False
                tempo_inicio = pygame.time.get_ticks()

            elif (game_over or vitoria) and event.key == pygame.K_r:
                reiniciar_jogo()
    
    if tela_inicio:
        desenhar_tela_inicio(tela)
        pygame.display.update()
        continue

    elif game_over:
        desenhar_game_over(tela)
        pygame.display.update()
        musica_fundo.stop()
        if not tocou_som_derrota:
            tocou_som_derrota = True
            som_derrota.play(0)
        continue

    elif vitoria:
        desenhar_vitoria(tela)
        pygame.display.update()
        musica_fundo.stop()
        if not tocou_som_vitoria: #o som toca apenas uma vez 
            tocou_som_vitoria = True
            som_vitoria.play(0)
        continue

    else:
        if not nivel1_completo:
            nivel_atual = 0

        else:
            if not nivel2_completo:
                nivel_atual = 1

            else:
                nivel_atual = 2

        if nivel_atual != nivel_anterior:
            nivel_anterior = nivel_atual
            atualizar_coletaveis_ao_mudar_nivel()

    if tempo_inicio is not None:
        tempo_passado = pygame.time.get_ticks() - tempo_inicio
    else:
        tempo_passado = 0

    tempo_restante = max(0, limite - tempo_passado) #o max evita tempo negativo
    
    segundos_restantes = tempo_restante // 1000

    minutos = segundos_restantes // 60
    segundos = segundos_restantes % 60

    if tempo_restante == 0 and not (nivel1_completo and nivel2_completo and nivel3_completo):
        game_over = True

    if nivel1_completo and nivel2_completo and nivel3_completo:
        vitoria = True
    
    texto_tempo = fonte.render(f'{minutos:02d}:{segundos:02d}', True, (255, 255, 255))
    
    pos_cronometro = (largura - 100, 10)
    tela.blit(texto_tempo, pos_cronometro)    #posição x=1350, y=10 (canto superior direito)

    ocorreu_colisoes(Fred, coletaveis_totais_naopegos)
    ocorreu_colisoes(Stefan, coletaveis_totais_naopegos)

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