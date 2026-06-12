import pygame 
from pygame.locals import*
from sys import exit

pygame.init

barulho_colisao = pygame.mixer.Sound('smw_coin.wav') 
barulho_colisao.set_volume(1) 

barulho_gag = pygame.mixer.Sound('smw_coin.wav') #mudar depois
barulho_gag.set_volume(1) 

barulho_gaita = pygame.mixer.Sound('smw_coin.wav') #mudar depois
barulho_gaita.set_volume(1) 

barulho_fechei = pygame.mixer.Sound('smw_coin.wav') #mudar depois
barulho_fechei.set_volume(1) 

largura = 1550
altura = 800


tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("PC-Hersteller")

class Personagem():
    def __init__(self, x, y, vel, teclas, sprite):
        self.rect = pygame.Rect(x, y, 48, 64)
        self.vel = vel
        self.teclas = teclas
        self.sprite = pygame.image.load(sprite).convert_alpha()
    def mover(self, teclas):
        if teclas[self.esq]: self.rect.x -= self.vel
        if teclas[self.dir]: self.rect.x += self.vel
        if teclas[self.cima]: self.rect.y -= self.vel
        if teclas[self.baixo]: self.rect.y += self.vel
    def desenhar(self, surf):
        surf.blit(self.sprite, self.rect)

Fred = Personagem(
    x=100, y=200,
    velocidade=4,
    teclas={"cima": pygame.K_w, "baixo": pygame.K_s,
            "esq":  pygame.K_a, "dir":   pygame.K_d},
    sprite_path="jogador1.png")

Stefan = Personagem(
    x=600, y=200,
    velocidade=4,
    teclas={"cima": pygame.K_UP,   "baixo": pygame.K_DOWN,
            "esq":  pygame.K_LEFT, "dir":   pygame.K_RIGHT},
    sprite_path="jogador2.png")

while True:
    tela.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            exit()
            
    teclas = pygame.key.get_pressed()
    Fred.mover(teclas)
    Stefan.mover(teclas)

    tela.fill((30, 30, 40))
    Fred.desenhar(tela)
    Stefan.desenhar(tela)

    pygame.display.update()                                 