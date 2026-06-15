import pygame 
import random
from random import randint
from pygame.locals import *
from sys import exit



pygame.init()
from game.players import *
from game.config_sons import *
from game.coletaveis import *
from game.colisoes import *

largura = 1550
altura = 800


tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("PC-Hersteller")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont('Arial', 20, True) #tamanho aleatório de fonte, quando a gente testar a gente troca

tempo_inicio = pygame.time.get_ticks()  #pega o tempo do inicio do jogo
limite = 120 * 1000  #2 minutos em milissegundos


margem_do_mapa = 30 #valor aleatorio so pra colocar no codigo


while True:
    clock.tick(60)
    tela.fill((30, 30, 40))

    if not nivel1_completo:
        for coletavel in coletaveis_nivel1:
            coletavel.desenhar(tela)
        ocorreu_colisoes(Stefan, coletaveis_nivel1)
        ocorreu_colisoes(Fred, coletaveis_nivel1)

    elif not nivel2_completo:
        for coletavel in coletaveis_nivel2:
            coletavel.desenhar(tela)
        ocorreu_colisoes(Stefan, coletaveis_nivel2)
        ocorreu_colisoes(Fred, coletaveis_nivel2)

    elif not nivel3_completo:
        for coletavel in coletaveis_nivel3:
            coletavel.desenhar(tela) 
        ocorreu_colisoes(Stefan, coletaveis_nivel3)
        ocorreu_colisoes(Fred, coletaveis_nivel3)

    tempo_passado = pygame.time.get_ticks() - tempo_inicio
    tempo_restante = max(0, limite - tempo_passado) #o max evita tempo negativo
    
    segundos_restantes = tempo_restante // 1000

    minutos = segundos_restantes // 60
    segundos = segundos_restantes % 60
    texto_tempo = f'{minutos:02d}:{segundos:02d}'

    texto_surface = fonte.render(texto_tempo, True, (255, 255, 255))
    tela.blit(texto_surface, (1350, 10))  #posição x=1350, y=10 (canto superior direito)

    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            exit()
            
    teclas = pygame.key.get_pressed()
    Fred.mover(teclas,largura, altura)
    Stefan.mover(teclas,largura, altura)


    Fred.desenhar(tela,)
    Stefan.desenhar(tela)

    mostrar_quantidade_coletaveis(tela)
  

    pygame.display.update()                                 