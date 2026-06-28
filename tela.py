import pygame
from constantes import largura, altura

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("PC-Hersteller")
mapa = pygame.image.load('assets/sprites/mapa.png').convert()
mapa = pygame.transform.scale(mapa, (largura, altura))

tela_vitoria = pygame.image.load('assets/sprites/tela_vitoria.png').convert()
tela_vitoria = pygame.transform.scale(tela_vitoria, (largura, altura))

tela_derrota = pygame.image.load('assets/sprites/tela_derrota.png').convert()
tela_derrota = pygame.transform.scale(tela_derrota, (largura, altura))

tela_inicio = pygame.image.load("assets/sprites/tela_inicio.png").convert()
tela_inicio = pygame.transform.scale(tela_inicio, (largura, altura))