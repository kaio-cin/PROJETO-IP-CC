import pygame 
import random
from random import randint
from pygame.locals import *
from sys import exit

pygame.init()

barulho_gag = pygame.mixer.Sound('assets/sons/gag.mp3') 
barulho_gag.set_volume(1) 

barulho_gaita = pygame.mixer.Sound('assets/sons/gaita.mp3') 
barulho_gaita.set_volume(0.3) 

barulho_fechei = pygame.mixer.Sound('assets/sons/fechei.mp3') 
barulho_fechei.set_volume(1) 

barulho_aps = pygame.mixer.Sound('assets/sons/aps.mp3') 
barulho_aps.set_volume(1) 

barulho_cerveja = pygame.mixer.Sound('assets/sons/cerveja.mp3') 
barulho_cerveja.set_volume(0.5) 

largura = 1200
altura = 700

#nivel 1 - portas logicas
nivel1_completo = False
meta_portas = 3

#nivel 2 - mux e demux
nivel2_completo = False
meta_combinacional = 3

#nivel 3 - flip-flops
nivel3_completo = False
meta_flipflops = 3

nivel_anterior = 0

game_over = False

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("PC-Hersteller")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont('Arial', 20, True) #tamanho aleatório de fonte, quando a gente testar a gente troca

tempo_inicio = pygame.time.get_ticks()  #pega o tempo do inicio do jogo
limite = 120 * 1000  #2 minutos em milissegundos

inventario = {"Portas Lógicas": 0, "Combinacionais": 0, "FlipFlop": 0}

easter_eggs = [("Cerveja Alemã", "assets/sprites/cervejaalema.png"), ("Gaita de Fole", "assets/sprites/gaita.png"), ("APS", "assets/sprites/aps.png")]

portas = [("Portas Lógicas", "assets/sprites/and.png"), ("Portas Lógicas", "assets/sprites/nand.png"), ("Portas Lógicas", "assets/sprites/not.png"), ("Portas Lógicas", "assets/sprites/or.png")]

combinacionais = [("Combinacionais", "assets/sprites/mux.png"), ("Combinacionais", "assets/sprites/dmux.png")]

flipflops = [("FlipFlop", "assets/sprites/flipflop.png")]

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
    x = randint (50, largura - margem_do_mapa - 25)   #o -25 vem da largura do coletavel
    y = randint(50, altura - margem_do_mapa - 25)
    return x, y


def spawnar_easter_eggs():
    lista_easter_eggs = []
    for tipo, sprite in easter_eggs:
        x, y = posicao_coletavel_aleatoria()
        lista_easter_eggs.append(Coletavel(x, y, tipo, sprite))
    
    return lista_easter_eggs


def spawnar_dois_coletaveis(lista_coletaveis):
    lista_coletaveis_escolhidos = []
    
    escolhidos = random.sample(lista_coletaveis, min(2, len(lista_coletaveis)))

    for tipo, sprite in escolhidos:
        x, y = posicao_coletavel_aleatoria()
        lista_coletaveis_escolhidos.append(Coletavel(x, y, tipo, sprite))

    return lista_coletaveis_escolhidos


easter_eggs_nao_pegos = spawnar_easter_eggs()
normais_ativos = spawnar_dois_coletaveis(portas)

coletaveis_totais_naopegos = easter_eggs_nao_pegos + normais_ativos


def ocorreu_colisoes(personagem, coletaveis):
    global tempo_inicio, nivel1_completo, nivel2_completo, nivel3_completo
    global coletaveis_totais_naopegos, normais_ativos

    for coletavel in coletaveis:
        if coletavel.naopego and personagem.rect.colliderect(coletavel.rect):
            coletavel.naopego = False
            
            if coletavel.tipo ==  "Gaita de Fole":
                barulho_gaita.play()
                tempo_inicio += 10 * 1000 #aumenta o tempo restante em 10 segundos
            elif coletavel.tipo == 'APS':
                barulho_aps.play()
                tempo_inicio -= 10 * 1000

            elif coletavel.tipo == 'Cerveja Alemã':
                barulho_cerveja.play()
                personagem.vel += 4

            else:
                if personagem == Fred: 
                    barulho_fechei.play()
                if personagem == Stefan:
                    barulho_gag.play()

                inventario[coletavel.tipo] += 1

                if coletavel.tipo == 'Portas Lógicas':
                    if inventario['Portas Lógicas'] >= meta_portas:
                        nivel1_completo = True

                    else:
                        novos_coletaveis = spawnar_dois_coletaveis(portas)
                        normais_ativos += novos_coletaveis
                        coletaveis_totais_naopegos += novos_coletaveis

                elif coletavel.tipo == 'Combinacionais':
                    if inventario["Combinacionais"] >= meta_combinacional:
                        nivel2_completo = True

                    else:
                        novos_coletaveis = spawnar_dois_coletaveis(combinacionais)
                        normais_ativos += novos_coletaveis
                        coletaveis_totais_naopegos += novos_coletaveis

                elif coletavel.tipo == 'FlipFlop':
                    if inventario['FlipFlop'] >= meta_flipflops:
                        nivel3_completo = True

                    else:
                        novos_coletaveis = spawnar_dois_coletaveis(flipflops)
                        normais_ativos += novos_coletaveis
                        coletaveis_totais_naopegos += novos_coletaveis


def atualizar_coletaveis_ao_mudar_nivel():
    global coletaveis_totais_naopegos, normais_ativos, easter_eggs_nao_pegos

    easter_eggs_nao_pegos = spawnar_easter_eggs()

    if not nivel1_completo:
        normais_ativos = spawnar_dois_coletaveis(portas)

    elif not nivel2_completo:
        normais_ativos = spawnar_dois_coletaveis(combinacionais)

    elif not nivel3_completo:
        normais_ativos = spawnar_dois_coletaveis(flipflops)

    coletaveis_totais_naopegos = normais_ativos + easter_eggs_nao_pegos



def mostrar_quantidade_coletaveis(surf):
    if not nivel1_completo:
        nivel = 'Nível 1 - Portas Lógicas'
        tipo = 'Portas Lógicas'
        meta = meta_portas

    
    elif not nivel2_completo:
        nivel = 'Nível 2 - Combinacionais'
        tipo = 'Combinacionais'
        meta = meta_combinacional

    
    elif not nivel3_completo:
        nivel = 'Nível 3 - Sequenciais'
        tipo = 'FlipFlop'
        meta = meta_flipflops

    else:
        nivel = 'Completo!'
        tipo = 'nenhum'
        meta = 0

    
    texto = fonte.render(nivel, True, (255, 255, 255))
    surf.blit(texto, (largura // 2 - texto.get_width() // 2, 10))   #essa funcao get_width pega a largura do texto

    if tipo != 'nenhum':
        quantidade = inventario[tipo]
        texto_quantidade = fonte.render(f'{tipo}: {quantidade} / {meta}', True, (255, 255, 255))
        surf.blit(texto_quantidade, (10, 10))

def desenhar_game_over(surf):
    surf.fill((0, 0, 0))
    texto    = fonte.render("GAME OVER", True, (255, 0, 0)) 
    surf.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2))


    
'''coletaveis_nivel1 = [Coletavel(*posicao_coletavel_aleatoria(), "Portas Lógicas",         "assets/sprites/and.png"),
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
'''

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

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            exit()

    if game_over:
        desenhar_game_over(tela)

    else:
        if not nivel1_completo:
            nivel_atual = 0

        else:
            if not nivel2_completo:
                nivel_atual = 1

            else:
                nivel_atual = 2

        if nivel_atual != nivel_anterior:
            nivel_anterior = nivel_atual
            atualizar_coletaveis_ao_mudar_nivel()


        tela.fill((30, 30, 40))

    '''if not nivel1_completo:
        for coletavel in coletaveis_nivel1:
            coletavel.desenhar(tela)
        ocorreu_colisoes(Stefan, coletaveis_nivel1)
        ocorreu_colisoes(Fred, coletaveis_nivel1)

    elif not nivel2_completo:
        for coletavel in coletaveis_nivel2:
            coletavel.desenhar(tela)
        ocorreu_colisoes(Stefan, coletaveis_nivel2)
        ocorreu_colisoes(Fred, coletaveis_nivel2)

    elif not nivel3_completo:
        for coletavel in coletaveis_nivel3:
            coletavel.desenhar(tela) 
        ocorreu_colisoes(Stefan, coletaveis_nivel3)
        ocorreu_colisoes(Fred, coletaveis_nivel3)'''

    tempo_passado = pygame.time.get_ticks() - tempo_inicio
    tempo_restante = max(0, limite - tempo_passado) #o max evita tempo negativo
    
    segundos_restantes = tempo_restante // 1000

    minutos = segundos_restantes // 60
    segundos = segundos_restantes % 60

    if tempo_restante == 0 and not (nivel1_completo and nivel2_completo and nivel3_completo):
        game_over = True

    texto_tempo = fonte.render(f'{minutos:02d}:{segundos:02d}', True, (255, 255, 255))
    
    pos_cronometro = (largura - 100, 10)
    tela.blit(texto_tempo, pos_cronometro)    #posição x=1350, y=10 (canto superior direito)

    ocorreu_colisoes(Fred, coletaveis_totais_naopegos)
    ocorreu_colisoes(Stefan, coletaveis_totais_naopegos)

    for coletavel in coletaveis_totais_naopegos:
        coletavel.desenhar(tela)
            
    teclas = pygame.key.get_pressed()
    Fred.mover(teclas)
    Stefan.mover(teclas)


    Fred.desenhar(tela)
    Stefan.desenhar(tela)

    mostrar_quantidade_coletaveis(tela)
  

    pygame.display.update()                                 