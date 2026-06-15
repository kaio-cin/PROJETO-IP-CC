import pygame
from pygame.locals import *
from random import randint
from tela import *

#SONS
barulho_gag = pygame.mixer.Sound('assets/sons/gag.mp3') 
barulho_gag.set_volume(1) 

barulho_gaita = pygame.mixer.Sound('assets/sons/gaita.mp3') 
barulho_gaita.set_volume(1) 

barulho_fechei = pygame.mixer.Sound('assets/sons/fechei.mp3') 
barulho_fechei.set_volume(1) 


#PERSONAGENS

class Personagem():
    def __init__(self, x, y, vel, teclas, sprite):
        self.rect = pygame.Rect(x, y, 48, 64)
        self.vel = vel
        self.cima = teclas['cima']
        self.baixo = teclas['baixo']
        self.esq = teclas['esq']
        self.dir = teclas['dir']
        self.sprite = pygame.image.load(sprite).convert_alpha()
       


    def mover(self, teclas):
        if teclas[self.esq]: 
            self.rect.x -= self.vel
        if teclas[self.dir]: 
            self.rect.x += self.vel
        if teclas[self.cima]: 
            self.rect.y -= self.vel
        if teclas[self.baixo]: 
            self.rect.y += self.vel

    def desenhar(self, surf):
        surf.blit(self.sprite, self.rect)


Fred = Personagem(
    x=100, y=200,
    vel=4,
    teclas={"cima": pygame.K_w, "baixo": pygame.K_s,
            "esq":  pygame.K_a, "dir":   pygame.K_d},
    sprite="jogador1.png")

Stefan = Personagem(
    x=600, y=200,
    vel=4,
    teclas={"cima": pygame.K_UP,   "baixo": pygame.K_DOWN,
            "esq":  pygame.K_LEFT, "dir":   pygame.K_RIGHT},
    sprite="jogador2.png")

#COLETAVEIS
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


coletaveis = [Coletavel(*posicao_coletavel_aleatoria(), "AND",         "and.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "NAND",        "nand.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "NOT",         "not.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "OR",          "or.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "MUX",         "mux.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "DMUX",        "dmux.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Contador",    "contador.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Registrador", "registrador.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "FlipFlop",    "flipflop.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Cerveja Alemã",    "cervejaalema.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "Gaita de Fole",    "gaitadefole.png"),
    Coletavel(*posicao_coletavel_aleatoria(), "APS",    "APS.png"),]

