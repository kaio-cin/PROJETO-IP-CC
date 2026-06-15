import pygame
from random import randint
from tela import largura, altura, margem_do_mapa, fonte



#nivel 1 - portas logicas
nivel1_completo = False
meta_portas = 3

#nivel 2 - mux e demux
nivel2_completo = False
meta_combinacional = 3

#nivel 3 - flip-flops
nivel3_completo = False
meta_flipflops = 3


inventario = {"Portas Lógicas": 0, "Combinacionais": 0, "FlipFlop": 0, "Gaita de Fole" : 0, "APS" :0, "Cerveja Alemã" : 0}


class Coletavel():
    def __init__(self, x, y, tipo, sprite):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.tipo = tipo
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.naopego = True

    
    def desenhar(self, surf):
        if self.naopego:
            surf.blit(self.sprite, self.rect)

def posicao_coletavel_aleatoria():
    x = randint (50, largura - margem_do_mapa - 25)   #o -32 vem da largura do coletavel
    y = randint(50, altura - margem_do_mapa - 25)
    return x, y


def mostrar_quantidade_coletaveis(surf):
    i = 0
    for tipo, quantidade in inventario.items():
        if (tipo == 'Portas Lógicas') or (tipo == 'Combinacionais') or (tipo == 'FlipFlop'):
            surf.blit(fonte.render(f'{tipo}: {quantidade}', True, (255, 255, 255)), (10, 20 * i))
        i += 1


coletaveis_nivel1 = [Coletavel(*posicao_coletavel_aleatoria(), "Portas Lógicas",         "assets/sprites/and.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Portas Lógicas",        "assets/sprites/nand.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Portas Lógicas",         "assets/sprites/not.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Portas Lógicas",          "assets/sprites/or.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Cerveja Alemã",    "assets/sprites/cervejaalema.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Gaita de Fole",    "assets/sprites/gaita.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "APS",    "assets/sprites/aps.png"),]

coletaveis_nivel2 = [
    Coletavel(*posicao_coletavel_aleatoria(), "Combinacionais",         "assets/sprites/mux.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Combinacionais",        "assets/sprites/dmux.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Combinacionais",         "assets/sprites/mux.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Combinacionais",        "assets/sprites/dmux.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Cerveja Alemã",    "assets/sprites/cervejaalema.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Gaita de Fole",    "assets/sprites/gaita.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "APS",    "assets/sprites/aps.png"),]

coletaveis_nivel3 = [
    Coletavel(*posicao_coletavel_aleatoria(), "FlipFlop",    "assets/sprites/flipflop.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "FlipFlop",    "assets/sprites/flipflop.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "FlipFlop",    "assets/sprites/flipflop.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "FlipFlop",    "assets/sprites/flipflop.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Cerveja Alemã",    "assets/sprites/cervejaalema.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Gaita de Fole",    "assets/sprites/gaita.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "APS",    "assets/sprites/aps.png"),]

#o * serve para desempacotar a tupla, invés de trazer ela assim (x,y) traz ela assim x,y (finalmente pode usar isso sem restrição das listas)
