import pygame


class Personagem():
    def __init__(self, x, y, vel, teclas, sprite):
        self.rect = pygame.Rect(x, y, 48, 64)
        self.vel = vel
        self.cima = teclas['cima']
        self.baixo = teclas['baixo']
        self.esq = teclas['esq']
        self.dir = teclas['dir']
        self.sprite = pygame.image.load(sprite).convert_alpha()
       

    def mover(self, teclas, largura, altura):
        if teclas[self.esq]: 
            self.rect.x -= self.vel
        if teclas[self.dir]: 
            self.rect.x += self.vel
        if teclas[self.cima]: 
            self.rect.y -= self.vel
        if teclas[self.baixo]: 
            self.rect.y += self.vel

        if self.rect.x >= largura - 64:
            self.rect.x = largura - 64
        if self.rect.x <= 0:
            self.rect.x = 0
        
        if self.rect.y >= altura - 64:
            self.rect.y = altura - 64
        if self.rect.y <= 0:
            self.rect.y = 0
       

    def desenhar(self, surf):
        surf.blit(self.sprite, self.rect)


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
