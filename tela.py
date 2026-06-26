import pygame 
import random
from random import randint
from pygame.locals import *
from sys import exit


pygame.init()

#Inicializando as musicas
from game.musicas import *
musica_fundo.play(-1) #o -1 faz a musica tocar em loop

largura = 1550
altura = 800

#nivel 1 - portas logicas
nivel1_completo = False
meta_portas = 4

#nivel 2 - mux e demux
nivel2_completo = False
meta_mux = 2
meta_demux = 2
#nivel 3 - flip-flops
nivel3_completo = False
meta_flipflops = 4

nivel_anterior = 0

game_over = False
vitoria = False
tocou_som_vitoria = False      

tela_inicio = True

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("PC-Hersteller")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont('Arial', 20, True) #tamanho aleatório de fonte, quando a gente testar a gente troca
fonte_game_over = pygame.font.SysFont('Arial', 40, True) 

tempo_inicio = None #none por causa da tela inicial
limite = 35 * 1000  #35 segundos em milissegundos

inventario = {"Portas Lógicas": 0, "MUX": 0, "DEMUX": 0, "FlipFlop": 0}

easter_eggs = [("Cerveja Alemã", "assets/sprites/cervejaalema.png"), ("Gaita de Fole", "assets/sprites/gaita.png"), ("APS", "assets/sprites/aps.png")]

portas = [("Portas Lógicas", "assets/sprites/and.png"), ("Portas Lógicas", "assets/sprites/nand.png"), ("Portas Lógicas", "assets/sprites/not.png"), ("Portas Lógicas", "assets/sprites/or.png")]

combinacionais = [("MUX", "assets/sprites/mux.png"), ("DEMUX", "assets/sprites/dmux.png")]

flipflops = [("FlipFlop", "assets/sprites/flipflop.png")]

portas_restantes = []
combinacionais_restantes = []
flipflops_restantes = []

combinacionais_restantes = [
    ("MUX", "assets/sprites/mux.png"),
    ("MUX", "assets/sprites/mux.png"),
    ("DEMUX", "assets/sprites/dmux.png"),
    ("DEMUX", "assets/sprites/dmux.png")
    ]

obstaculos = [
    pygame.Rect(0, 335, 50, 40),  #parte esquerda do rio
    pygame.Rect(105, 335, 460, 40),  #parte pós primeira ponte do rio
    pygame.Rect(615, 337, 540, 40),  #parte pós segunda ponte do rio
    pygame.Rect(1210, 337, 330, 40), #parte direita do rio
    #caixas maiores
    pygame.Rect(853, 705, 20, 10),
    pygame.Rect(1140, 275, 20, 10),
    #caixas pequenas
    pygame.Rect(325, 708, 5, 6), 
    pygame.Rect(358, 697, 10, 6), 
    pygame.Rect(442, 482, 10, 20),
    pygame.Rect(478, 459, 10, 20),
    pygame.Rect(851, 553, 10, 20),
    pygame.Rect(885, 525, 10, 20),
    pygame.Rect(1060, 182, 15, 8),
    pygame.Rect(1097, 154, 15, 8),
    pygame.Rect(1144, 750, 5, 1),
    #bancos
    pygame.Rect(423, 212, 75, 5),
    pygame.Rect(958, 695, 75, 5),
    #fonte - nao existe um pygame.circle ent tive q fazer um retangulo aproximado, colisao c circulo é mais complicado
    pygame.Rect(864, 226, 57, 38),

    pygame.Rect(185, 197, 115, 105),  #casa azul
    pygame.Rect(1177, 0, 143, 147),   #casa marrom parte direita em cima
    pygame.Rect(100, 500, 120, 155),  #casa marrom parte esquerda baixo
    pygame.Rect(227, 650, 39, 1),     #cerca casa marrom parte esquerda baixo
    pygame.Rect(1184, 550, 120, 120), #casa verde
    pygame.Rect(1140, 680, 30, 1),    #cerca casa verde
    pygame.Rect(705, 705, 116, 100),  #casa marrom baixo
    pygame.Rect(630, 590, 128, 15),   #tenda
    pygame.Rect(753, 536, 7, 50),     #tenda
    pygame.Rect(435, 125, 75, 20),    #casinha marrom
    pygame.Rect(636, 793, 20, 1),     #cerca
    pygame.Rect(1117, 480, 20, 1)     #cerca
    ]



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


margem_do_mapa = 30 #valor aleatorio so pra colocar no codigo

def posicao_coletavel_aleatoria():
    posicao_valida = False
    while not posicao_valida:
        x = randint (50, largura - margem_do_mapa - 25)   #o -25 vem da largura do coletavel
        y = randint(50, altura - margem_do_mapa - 25)
        rect_coletavel = pygame.Rect(x, y, 25, 25)
        rect_checagem = rect_coletavel.inflate(10, 10) #para nao nascer colado no obstaculo (tava dando problema)
        if not any(rect_checagem.colliderect(obstaculo) for obstaculo in obstaculos): 
            posicao_valida = True
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
portas_restantes = portas.copy()
normais_ativos = spawnar_dois_coletaveis(portas_restantes)

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
                personagem.vel = personagem.vel_normal + 1.5
                personagem.vel_bonus = True
                personagem.controles_invertidos = True
                personagem.fim_efeito_cerveja = pygame.time.get_ticks() + 7000 #efeito dura 7 segundos

            else:
                if personagem == Fred: 
                    barulho_fechei.play()
                if personagem == Stefan:
                    barulho_gag.play()

                inventario[coletavel.tipo] += 1

                if coletavel.tipo == 'Portas Lógicas':
                    remover_do_pool( coletavel.tipo, coletavel.caminho_sprite, portas_restantes)

                    if inventario["Portas Lógicas"] >= 4:
                        nivel1_completo = True
                    
                    else:
                        manter_dois_coletaveis(portas_restantes)

                elif coletavel.tipo == "MUX":

                    remover_do_pool(
                        coletavel.tipo,
                        coletavel.caminho_sprite,
                        combinacionais_restantes
                    )

                    if inventario["MUX"] >= 2 and inventario["DEMUX"] >= 2:
                        nivel2_completo = True
                    else:
                        manter_dois_coletaveis(combinacionais_restantes)


                elif coletavel.tipo == "DEMUX":

                    remover_do_pool(
                        coletavel.tipo,
                        coletavel.caminho_sprite,
                        combinacionais_restantes
                    )

                    if inventario["MUX"] >= 2 and inventario["DEMUX"] >= 2:
                        nivel2_completo = True
                    else:
                        manter_dois_coletaveis(combinacionais_restantes)
                        
                elif coletavel.tipo == 'FlipFlop':
                    if inventario['FlipFlop'] >= meta_flipflops:
                        nivel3_completo = True

                    else:
                        novos_coletaveis = spawnar_dois_coletaveis(flipflops)
                        normais_ativos += novos_coletaveis
                        coletaveis_totais_naopegos += novos_coletaveis


def atualizar_coletaveis_ao_mudar_nivel():
    global coletaveis_totais_naopegos, normais_ativos, easter_eggs_nao_pegos, combinacionais_restantes
     
    easter_eggs_nao_pegos = spawnar_easter_eggs()

    if not nivel1_completo:
        normais_ativos = spawnar_dois_coletaveis(portas_restantes)

    elif not nivel2_completo:
        combinacionais_restantes = [
            ("MUX", "assets/sprites/mux.png"),
            ("MUX", "assets/sprites/mux.png"),
            ("DEMUX", "assets/sprites/dmux.png"),
            ("DEMUX", "assets/sprites/dmux.png")
        ]

        normais_ativos = spawnar_dois_coletaveis(combinacionais_restantes)

    elif not nivel3_completo:
        normais_ativos = spawnar_dois_coletaveis(flipflops)

    coletaveis_totais_naopegos = normais_ativos + easter_eggs_nao_pegos

#limpar as listas de coletaveis para o próximo nível
def remover_do_pool(tipo, sprite, pool):
    for item in pool:
        if item[0] == tipo and item[1] == sprite:
            pool.remove(item)
            break
#garante que sempre haja 2 coletaveis do tipo necessário para o nível, mesmo que o jogador pegue um e não tenha mais no pool
def manter_dois_coletaveis(pool):
    global normais_ativos, coletaveis_totais_naopegos
    
    normais_ativos[:] = [c for c in normais_ativos if c.naopego]

    ativos_visiveis = [
        c for c in normais_ativos
        if c.naopego
    ]

    coletaveis_totais_naopegos[:] = [c for c in coletaveis_totais_naopegos if c.naopego]

    while len(ativos_visiveis) < 2 and len(pool) > 0:

        sprites_ativos = [
            c.caminho_sprite
            for c in ativos_visiveis
        ]

        candidatos = [
            item
            for item in pool
            if item[1] not in sprites_ativos
        ]

        if len(candidatos) == 0:
            break

        tipo, sprite = random.choice(candidatos)   

        x, y = posicao_coletavel_aleatoria()

        novo = Coletavel(
            x,
            y,
            tipo,
            sprite
        )

        normais_ativos.append(novo)
        coletaveis_totais_naopegos.append(novo)

        ativos_visiveis.append(novo)

def mostrar_quantidade_coletaveis(surf):
    if not nivel1_completo:
        nivel = 'Nível 1 - Portas Lógicas'
        tipo = 'Portas Lógicas'
        meta = meta_portas

    
    elif not nivel2_completo:
        nivel = 'Nível 2 - Combinacionais'
        tipo = 'MUX'

    
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
        if not nivel1_completo:
            quantidade = inventario["Portas Lógicas"]
            texto_quantidade = fonte.render(
                f'Portas: {quantidade} / {meta_portas}',
                True,
                (255,255,255)
            )

        elif not nivel2_completo:
            texto_quantidade = fonte.render(
                f'MUX: {inventario["MUX"]}/2  |  DEMUX: {inventario["DEMUX"]}/2',
                True,
                (255,255,255)
            )

        elif not nivel3_completo:
            quantidade = inventario["FlipFlop"]
            texto_quantidade = fonte.render(
                f'FlipFlops: {quantidade} / {meta_flipflops}',
                True,
                (255,255,255)
            )

        surf.blit(texto_quantidade, (10, 10))

def desenhar_game_over(surf):
    surf.blit(tela_derrota, (0, 0))

def desenhar_vitoria(surf):
    surf.blit(tela_vitoria, (0, 0))

def desenhar_tela_inicio(surf):
    surf.blit(tela_inicio, (0, 0))

def reiniciar_jogo():
    global game_over, vitoria, tocou_som_vitoria
    global nivel1_completo, nivel2_completo, nivel3_completo
    global inventario
    global tempo_inicio
    global coletaveis_totais_naopegos
    global normais_ativos
    global easter_eggs_nao_pegos
    global nivel_anterior
    global portas_restantes
    global combinacionais_restantes

    portas_restantes = portas.copy()

    combinacionais_restantes = [
        ("MUX", "assets/sprites/mux.png"),
        ("MUX", "assets/sprites/mux.png"),
        ("DEMUX", "assets/sprites/dmux.png"),
        ("DEMUX", "assets/sprites/dmux.png")
    ]

    game_over = False
    vitoria = False
    tocou_som_vitoria = False
    nivel1_completo = False
    nivel2_completo = False
    nivel3_completo = False

    nivel_anterior = 0

    inventario = {
        "Portas Lógicas": 0,
        "MUX": 0,
        "DEMUX": 0,
        "FlipFlop": 0
    }

    Fred.rect.x = 100
    Fred.rect.y = 200

    Stefan.rect.x = 600
    Stefan.rect.y = 200

    Fred.vel = Fred.vel_normal
    Stefan.vel = Stefan.vel_normal

    Fred.vel_bonus = False
    Stefan.vel_bonus = False

    Fred.controles_invertidos = False
    Stefan.controles_invertidos = False

    tempo_inicio = pygame.time.get_ticks()
    musica_fundo.play(-1)
    easter_eggs_nao_pegos = spawnar_easter_eggs()
    normais_ativos = spawnar_dois_coletaveis(portas_restantes)

    coletaveis_totais_naopegos = (easter_eggs_nao_pegos + normais_ativos)
    

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

mapa = pygame.image.load('assets/sprites/mapa.png').convert()
mapa = pygame.transform.scale(mapa, (largura, altura))

tela_vitoria = pygame.image.load('assets/sprites/tela_vitoria.png').convert()
tela_vitoria = pygame.transform.scale(tela_vitoria, (largura, altura))

tela_derrota = pygame.image.load('assets/sprites/tela_derrota.png').convert()
tela_derrota = pygame.transform.scale(tela_derrota, (largura, altura))

tela_inicio = pygame.image.load("assets/sprites/tela_inicio.png").convert()
tela_inicio = pygame.transform.scale(tela_inicio, (largura, altura))

while True:
    clock.tick(60)
    tela.blit(mapa, (0, 0))
    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if tela_inicio and event.key == pygame.K_SPACE:
                tela_inicio = False
                tempo_inicio = pygame.time.get_ticks()

            elif (game_over or vitoria) and event.key == pygame.K_r:
                reiniciar_jogo()
    
    if tela_inicio:
        desenhar_tela_inicio(tela)
        pygame.display.update()
        continue

    elif game_over:
        desenhar_game_over(tela)
        pygame.display.update()
        continue

    elif vitoria:
        desenhar_vitoria(tela)
        pygame.display.update()
        musica_fundo.stop()
        if not tocou_som_vitoria: #o som toca apenas uma vez 
            tocou_som_vitoria = True
            som_vitoria.play(0)
        continue

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

    if tempo_inicio is not None:
        tempo_passado = pygame.time.get_ticks() - tempo_inicio
    else:
        tempo_passado = 0

    tempo_restante = max(0, limite - tempo_passado) #o max evita tempo negativo
    
    segundos_restantes = tempo_restante // 1000

    minutos = segundos_restantes // 60
    segundos = segundos_restantes % 60

    if tempo_restante == 0 and not (nivel1_completo and nivel2_completo and nivel3_completo):
        game_over = True

    if nivel1_completo and nivel2_completo and nivel3_completo:
        vitoria = True
    
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