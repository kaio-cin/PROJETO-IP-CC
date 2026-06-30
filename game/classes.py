import pygame 
import os
from game.constantes import largura, altura, obstaculos

def carregar_animacao(pasta):
    arquivos = sorted(os.listdir(pasta))

    return [pygame.image.load(os.path.join(pasta, arq)).convert_alpha() for arq in arquivos]

class Personagem():
    def __init__(self, x, y, vel, teclas, pasta_animacoes):
        self.rect = pygame.Rect(x, y, 48, 64)
        self.vel = vel
        self.cima = teclas['cima']
        self.baixo = teclas['baixo']
        self.esq = teclas['esq']
        self.dir = teclas['dir']       
        self.vel_normal = vel
        self.vel_bonus = False
        self.fim_efeito_cerveja = 0
        self.vel_penalidade = False
        self.fim_efeito_gato = 0
        self.controles_invertidos = False
        #parte da animação de movimento do personagem
        self.animacoes = {
            "down": carregar_animacao(os.path.join(pasta_animacoes, "down")),
            "up": carregar_animacao(os.path.join(pasta_animacoes, "up")),
            "left": carregar_animacao(os.path.join(pasta_animacoes, "left")),
            "right": carregar_animacao(os.path.join(pasta_animacoes, "right"))}
        self.direcao = "down"
        self.frame = 0
        self.vel_animacao = 0.18
        self.movendo = False
        self.sprite = self.animacoes["down"][0] 

    def mover(self, teclas):

        if self.vel_bonus and pygame.time.get_ticks() >= self.fim_efeito_cerveja:
            self.vel = self.vel_normal
            self.vel_bonus = False
            self.controles_invertidos = False

        if self.vel_penalidade and pygame.time.get_ticks() >= self.fim_efeito_gato:
            self.vel = self.vel_normal
            self.vel_penalidade = False
            
        self.movendo = False

        if not self.controles_invertidos:
            if teclas[self.esq]:
                self.rect.x -= self.vel
                self.direcao = "left"
                self.movendo = True

            if teclas[self.dir]:
                self.rect.x += self.vel
                self.direcao = "right"
                self.movendo = True
        else:
            if teclas[self.esq]:
                self.rect.x += self.vel
                self.direcao = "left"
                self.movendo = True

            if teclas[self.dir]:
                self.rect.x -= self.vel
                self.direcao = "right"
                self.movendo = True

        # checa colisao no eixo X e corrige
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo):
                if not self.controles_invertidos:
                    if teclas[self.dir]:
                        self.rect.right = obstaculo.left
                    if teclas[self.esq]:
                        self.rect.left = obstaculo.right
                else:
                    if teclas[self.esq]:
                        self.rect.right = obstaculo.left
                    if teclas[self.dir]:
                        self.rect.left = obstaculo.right

        # move no eixo Y
        if not self.controles_invertidos:
            if teclas[self.cima]:
                self.rect.y -= self.vel
                self.direcao = "up"
                self.movendo = True

            if teclas[self.baixo]:
                self.rect.y += self.vel
                self.direcao = "down"
                self.movendo = True
        else:
            if teclas[self.cima]:
                self.rect.y += self.vel
                self.direcao = "up"
                self.movendo = True

            if teclas[self.baixo]:
                self.rect.y -= self.vel
                self.direcao = "down"
                self.movendo = True

        # checa colisao no eixo Y e corrige
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo):
                if not self.controles_invertidos:
                    if teclas[self.baixo]:
                        self.rect.bottom = obstaculo.top
                    if teclas[self.cima]:
                        self.rect.top = obstaculo.bottom
                else:
                    if teclas[self.cima]:
                        self.rect.bottom = obstaculo.top
                    if teclas[self.baixo]:
                        self.rect.top = obstaculo.bottom

        if self.rect.x >= largura - 48:
            self.rect.x = largura - 48
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= altura - 48:
            self.rect.y = altura - 48
        if self.rect.y <= 0:
            self.rect.y = 0


    def atualizar_animacao(self):
        if self.movendo:
            self.frame += self.vel_animacao

            if self.frame >= len(self.animacoes[self.direcao]):
                self.frame = 0
        else:
            self.frame = 0

        self.sprite = self.animacoes[self.direcao][int(self.frame)]


    def desenhar(self, surf):
        surf.blit(self.sprite, self.rect)



class Coletavel():
    def __init__(self, x, y, tipo, sprite):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.tipo = tipo
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.caminho_sprite = sprite
        self.naopego = True

    
    def desenhar(self, surf):
        if self.naopego:
            surf.blit(self.sprite, self.rect)
