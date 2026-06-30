import pygame
#META COLETAVEIS
metas = {
    'meta_portas' : 4,
    'meta_mux' : 2,
    'meta_demux' : 2,
    'meta_flipflops' : 4

}

#boleanas
#nivel 1 - portas logicas
boleanas = {
'nivel1_completo' : False,
#nivel 2 - mux e demux
'nivel2_completo' : False,
#nivel 3 - flip-flops
'nivel3_completo' : False,
'nivel_anterior' : 0,
'game_over' : False,
'vitoria' : False,
'tocou_som_vitoria' : False,
'tocou_som_derrota' : False,
'tela_inicio' : True
}

#MEDIDAS
largura = 1550
altura = 800
fonte = pygame.font.SysFont('Arial', 20, True) #tamanho aleatório de fonte, quando a gente testar a gente troca
fonte_game_over = pygame.font.SysFont('Arial', 40, True) 
clock = pygame.time.Clock()
tempo_inicio = int() #none por causa da tela inicial
limite = 35 * 1000  #35 segundos em milissegundos
margem_do_mapa = 30 #valor aleatorio so pra colocar no codigo



#COLISOES
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


#imagens

inventario = {"Portas Lógicas": 0, "MUX": 0, "DEMUX": 0, "FlipFlop": 0}

easter_eggs = [("Cerveja Alemã", "assets/sprites/cervejaalema.png"), ("Gaita de Fole", "assets/sprites/gaita.png"), ("APS", "assets/sprites/aps.png"), ('Gato', 'assets/sprites/gato.png')]

portas = [("Portas Lógicas", "assets/sprites/and.png"), ("Portas Lógicas", "assets/sprites/nand.png"), ("Portas Lógicas", "assets/sprites/not.png"), ("Portas Lógicas", "assets/sprites/or.png")]

combinacionais = [("MUX", "assets/sprites/mux.png"), ("DEMUX", "assets/sprites/dmux.png")]

flipflops = [("FlipFlop", "assets/sprites/flipflop.png")]

portas_restantes = portas.copy()
flipflops_restantes = flipflops.copy()
combinacionais_restantes = [
    ("MUX", "assets/sprites/mux.png"),
    ("MUX", "assets/sprites/mux.png"),
    ("DEMUX", "assets/sprites/dmux.png"),
    ("DEMUX", "assets/sprites/dmux.png")
    ]
