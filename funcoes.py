
import pygame
import os
import random
from random import randint
from constantes import altura, largura, margem_do_mapa, obstaculos, inventario, portas_restantes ,metas, flipflops, fonte, portas
from classes import Coletavel
from players import Fred, Stefan
from tela import tela_derrota, tela_inicio, tela_vitoria
from game.musicas import musica_fundo


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
    from constantes import easter_eggs
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

def ocorreu_colisoes(personagem, coletaveis):
    from constantes import tempo_inicio
    global nivel1_completo, nivel2_completo, nivel3_completo
    global coletaveis_totais_naopegos, normais_ativos

    for coletavel in coletaveis:
        from game.musicas import barulho_aps, barulho_cerveja, barulho_fechei, barulho_gag, barulho_gaita
        
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
                    if inventario['FlipFlop'] >= metas['meta_flipflops']:
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
    from constantes import nivel1_completo, nivel2_completo, nivel3_completo
    if not nivel1_completo:
        nivel = 'Nível 1 - Portas Lógicas'
        tipo = 'Portas Lógicas'
        meta = metas['meta_portas']

    
    elif not nivel2_completo:
        nivel = 'Nível 2 - Combinacionais'
        tipo = 'MUX'

    
    elif not nivel3_completo:
        nivel = 'Nível 3 - Sequenciais'
        tipo = 'FlipFlop'
        meta = metas['meta_flipflops']

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
                f'Portas: {quantidade} / {metas['meta_portas']}',
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
                f'FlipFlops: {quantidade} / {metas['meta_flipflops']}',
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
    global game_over, vitoria, tocou_som_vitoria, tocou_som_derrota
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
    tocou_som_derrota = False
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