import pygame 
from pygame.locals import*
from sys import exit

pygame.init

largura = 1550
altura = 800


tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("PC-Hersteller")

while True:
    tela.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            exit()

    pygame.display.update()                                 