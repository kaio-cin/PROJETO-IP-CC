from game.config_sons import *
from game.coletaveis import *
from game.players import Fred, Stefan


def ocorreu_colisoes(personagem, coletaveis):
    global tempo_inicio, nivel1_completo, nivel2_completo, nivel3_completo
    for coletavel in coletaveis:
        if coletavel.naopego and personagem.rect.colliderect(coletavel.rect):
            coletavel.naopego = False
            inventario[coletavel.tipo] += 1
            if coletavel.tipo ==  "Gaita de Fole":
                barulho_gaita.play()
                tempo_inicio += 10 * 1000 #aumenta o tempo restante em 10 segundos
            else: 
                if coletavel.tipo == 'APS':
                    barulho_aps.play()
                    tempo_inicio -= 10 * 1000 #diminui o tempo restante em 10 segundos
                else:
                    if coletavel.tipo == 'Cerveja Alemã':
                        barulho_cerveja.play()
                        personagem.vel += 4
                    else:
                        if personagem == Fred: 
                            barulho_fechei.play()
                        if personagem == Stefan:
                            barulho_gag.play() 
                        if coletavel.tipo == 'Portas Lógicas':
                            if inventario['Portas Lógicas'] >= meta_portas:
                                nivel1_completo = True
                        if coletavel.tipo == 'Combinacionais':
                            if inventario["Combinacionais"] >= meta_combinacional:
                                nivel2_completo = True
                        if coletavel.tipo == 'FlipFlop':
                            if inventario['FlipFlop'] >= meta_flipflops:
                                nivel3_completo = True

