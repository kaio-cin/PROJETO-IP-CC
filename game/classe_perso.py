import pygame
from game.posição_obstaculos import *
from game.diemensoes_tela import largura, altura
class Personagem():
    def __init__(self, x, y, vel, teclas, sprite):
        self.rect = pygame.Rect(x, y, 48, 64)
        self.vel = vel
        self.cima = teclas['cima']
        self.baixo = teclas['baixo']
        self.esq = teclas['esq']
        self.dir = teclas['dir']
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.vel_normal = vel
        self.vel_bonus = False
        self.fim_efeito_cerveja = 0
        self.controles_invertidos = False

    def mover(self, teclas):

        if self.vel_bonus and pygame.time.get_ticks() >= self.fim_efeito_cerveja:
            self.vel = self.vel_normal
            self.vel_bonus = False
            self.controles_invertidos = False
            
        if not self.controles_invertidos:
            if teclas[self.esq]: 
                self.rect.x -= self.vel
            if teclas[self.dir]: 
                self.rect.x += self.vel
        else:
            if teclas[self.esq]: 
                self.rect.x += self.vel
            if teclas[self.dir]: 
                self.rect.x -= self.vel

        # checa colisao no eixo X e corrige
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo):
                if not self.controles_invertidos:
                    if teclas[self.dir]: 
                        self.rect.right = obstaculo.left
                    if teclas[self.esq]: 
                        self.rect.left  = obstaculo.right
                else:
                    if teclas[self.esq]: 
                        self.rect.right = obstaculo.left
                    if teclas[self.dir]: 
                        self.rect.left  = obstaculo.right

        # move no eixo Y
        if not self.controles_invertidos:
            if teclas[self.cima]:  
                self.rect.y -= self.vel
            if teclas[self.baixo]: 
                self.rect.y += self.vel
        else:
            if teclas[self.cima]:  
                self.rect.y += self.vel
            if teclas[self.baixo]: 
                self.rect.y -= self.vel

        # checa colisao no eixo Y e corrige
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo):
                if not self.controles_invertidos:
                    if teclas[self.baixo]: 
                        self.rect.bottom = obstaculo.top
                    if teclas[self.cima]:  
                        self.rect.top    = obstaculo.bottom
                else:
                    if teclas[self.cima]:  
                        self.rect.bottom = obstaculo.top
                    if teclas[self.baixo]: 
                        self.rect.top    = obstaculo.bottom
            
        if self.rect.x >= largura - 48: 
            self.rect.x = largura - 48
        if self.rect.x <= 0:            
            self.rect.x = 0
        if self.rect.y >= altura - 48:  
            self.rect.y = altura - 48
        if self.rect.y <= 0:           
            self.rect.y = 0


        

    def desenhar(self, surf):
        surf.blit(self.sprite, self.rect)
