import pygame 
from game.classe_perso import *
#classe

Fred = Personagem(
    x=100, y=200,
    vel=4,
    teclas={"cima": pygame.K_w, "baixo": pygame.K_s,
            "esq":  pygame.K_a, "dir":   pygame.K_d},
    sprite="assets/sprites/fred.png"
    )

Stefan = Personagem(
    x=600, y=200,
    vel=4,
    teclas={"cima": pygame.K_UP,   "baixo": pygame.K_DOWN,
            "esq":  pygame.K_LEFT, "dir":   pygame.K_RIGHT},
    sprite="assets/sprites/stefan.png"
    )

#dimensões
Fred.rect.x = 100
Fred.rect.y = 200

Stefan.rect.x = 600
Stefan.rect.y = 200

Fred.vel = Fred.vel_normal
Stefan.vel = Stefan.vel_normal