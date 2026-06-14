import pygame 
import random
from random import randint
from pygame.locals import*
from sys import exit

pygame.init()

barulho_gag = pygame.mixer.Sound('gag.mp3') 
barulho_gag.set_volume(1) 

barulho_gaita = pygame.mixer.Sound('gaita.mp3') 
barulho_gaita.set_volume(1) 

barulho_fechei = pygame.mixer.Sound('fechei.mp3') 
barulho_fechei.set_volume(1) 

largura = 1550
altura = 800

#nivel 1 - portas logicas
qtd_portas = 0
meta_portas = 3

#nivel 2 - mux e demux
qtd_combinacional = 0
meta_combinacional = 3

#nivel 3 - contador, registrador e flip-flop
qtd_sequencial = 0
meta_sequencial = 5

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("PC-Hersteller")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont('Arial', 20, True) #tamanho aleatório de fonte, quando a gente testar a gente troca

tempo_inicio = pygame.time.get_ticks()  #pega o tempo do inicio do jogo
limite = 120 * 1000  #2 minutos em milissegundos

inventario = {"AND": 0, "NAND": 0, "NOT": 0, "OR": 0, "MUX": 0, "DMUX": 0, "Contador": 0, "Registrador": 0, "Flipflop": 0}

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


class Coletavel():
    def __init__(self, x, y, tipo, sprite):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.tipo = tipo
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.naopego = True

    
    def desenhar(self, surf):
        if self.naopego:
            surf.blit(self.sprite, self.rect)


margem_do_mapa = 30 #valor aleatorio so pra colocar no codigo

def posicao_coletavel_aleatoria():
    x = randint (50, largura - margem_do_mapa - 25)   #o -32 vem da largura do coletavel
    y = randint(50, altura - margem_do_mapa - 25)
    return x, y


def ocorreu_colisoes(personagem, coletaveis):
    for coletavel in coletaveis:
        if coletavel.naopego and personagem.rect.colliderect(coletavel.rect):
            coletavel.naopego = False
            inventario[coletavel.tipo] += 1
            barulho_colisao.play()



def mostrar_quantidade_coletaveis(surf):
    i = 0
    for tipo, quantidade in inventario.items():
        surf.blit(fonte.render(f'{tipo}: {quantidade}', True, (255, 255, 255)), (10, 20 * i))
        i += 1


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

#o * serve para desempacotar a tupla, invés de trazer ela assim (x,y) traz ela assim x,y (finalmente pode usar isso sem restrição das listas)

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

while True:
    clock.tick(60)
    tela.fill((30, 30, 40))
    
    tempo_passado = pygame.time.get_ticks() - tempo_inicio
    tempo_restante = max(0, limite - tempo_passado) #o max evita tempo negativo
    
    segundos_restantes = tempo_restante // 1000

    minutos = segundos_restantes // 60
    segundos = segundos_restantes % 60
    texto_tempo = f'{minutos:02d}:{segundos:02d}'

    texto_surface = fonte.render(texto_tempo, True, (255, 255, 255))
    tela.blit(texto_surface, (10, 10))  #posição x=10, y=10 (canto superior esquerdo)

    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            exit()
            
    teclas = pygame.key.get_pressed()
    Fred.mover(teclas)
    Stefan.mover(teclas)

    ocorreu_colisoes(Fred, coletaveis)
    ocorreu_colisoes(Stefan, coletaveis)

    for coletavel in coletaveis:
        coletavel.desenhar(tela)

    
    Fred.desenhar(tela)
    Stefan.desenhar(tela)

    mostrar_quantidade_coletaveis(tela)
  

    pygame.display.update()                                 