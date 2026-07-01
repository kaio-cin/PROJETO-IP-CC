import pygame
from game.constantes import largura, altura

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Hersteller")
mapa = pygame.image.load('assets/sprites/mapa.png').convert()
mapa = pygame.transform.scale(mapa, (largura, altura))

tela_vitoria = pygame.image.load('assets/sprites/tela_vitoria.png').convert()
tela_vitoria = pygame.transform.scale(tela_vitoria, (largura, altura))

tela_derrota = pygame.image.load('assets/sprites/tela_derrota.png').convert()
tela_derrota = pygame.transform.scale(tela_derrota, (largura, altura))

tela_inicio = pygame.image.load("assets/sprites/tela_inicio.png").convert()
tela_inicio = pygame.transform.scale(tela_inicio, (largura, altura))

tamanho_icone_efeito = 37

def _carregar_icone_efeito(caminho):
    img = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(img, (tamanho_icone_efeito, tamanho_icone_efeito))

icone_cerveja_frames = [
    _carregar_icone_efeito('assets/sprites/cerveja/cervejaalema.png'),
    _carregar_icone_efeito('assets/sprites/cerveja/cervejaalemacinza.png'),
]

icone_gato_frames = [
    _carregar_icone_efeito('assets/sprites/gato/gato.png'),
    _carregar_icone_efeito('assets/sprites/gato/gato_cinza.png'),
]