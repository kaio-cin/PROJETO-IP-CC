# 🎮 HERSTELLER

> Projeto Final da disciplina de Introdução à Programação (IP)
> Centro de Informática (CIn) – Universidade Federal de Pernambuco (UFPE)

---

## 📖 Sobre o Projeto

**HERSTELLER** é um jogo cooperativo desenvolvido em Python utilizando a biblioteca Pygame, no qual dois jogadores precisam trabalhar juntos para coletar componentes necessários para construir um computador de 8 bits.

Os jogadores controlam os personagens **Stefan** e **Fred**, compartilhando o mesmo teclado e cooperando para superar obstáculos, administrar o tempo disponível e coletar os itens espalhados pelo mapa.

---

## 👥 Equipe

| Integrante                                 | E-mail                                        |
| ------------------------------------------ | --------------------------------------------- |
| Breno Alves Chagas Rabelo                  | [bacr@cin.ufpe.br](mailto:bacr@cin.ufpe.br)   |
| Frederico Hazin Costa                      | [fhc@cin.ufpe.br](mailto:fhc@cin.ufpe.br)     |
| Kaio Ruan da Silva Barros                  | [krsb@cin.ufpe.br](mailto:krsb@cin.ufpe.br)   |
| Sofia Mendonça de Vasconcelos do A. Bastos | [smvab@cin.ufpe.br](mailto:smvab@cin.ufpe.br) |
| Alice de Medeiros Costa                    | [amc6@cin.ufpe.br](mailto:amc6@cin.ufpe.br)   |
| Nina Tiné Cantilino                        | [ntc@cin.ufpe.br](mailto:ntc@cin.ufpe.br)     |

### Professores

* Ricardo Massa
* Márcio Lopes Cornélio

---

## 🎯 Objetivo

Coletar todos os componentes necessários para a construção de um computador de 8 bits antes que o tempo acabe.

O jogo incentiva:

* Cooperação entre jogadores;
* Coordenação de movimentos;
* Gerenciamento de tempo;
* Exploração do mapa;
* Trabalho em equipe.

---

## 🕹️ Mecânicas do Jogo

### Personagens

* 👨 Stefan
* 👨 Fred

Os dois personagens possuem animações para todas as direções de movimento:

* ⬆️ Cima
* ⬇️ Baixo
* ⬅️ Esquerda
* ➡️ Direita

---

## 📦 Itens Coletáveis

### Portas Lógicas

* AND
* NAND
* NOT
* OR

### Dispositivos Combinacionais

* MUX
* DMUX

### Dispositivos Sequenciais

* Flip-Flops

---

## 🎁 Easter Eggs

| Item             | Efeito                                      |
| ---------------- | ------------------------------------------- |
| 🎵 Gaita de Fole | Adiciona 10 segundos ao tempo               |
| 📚 APS           | Remove 10 segundos                          |
| 🍺 Cerveja Alemã | Inverte os controles e aumenta a velocidade |
| 🐱 Gato ruivo    | Diminui a velocidade do personagem          |
---

## 🗺️ Mapa

O cenário do jogo é inspirado em uma região rural da Alemanha.

### Obstáculos

* 🌊 Rio
* 📦 Caixas
* 🏠 Casas
* ⛲ Fonte
* 🪑 Bancos

---

## 🎨 Direção Artística

O projeto possui forte influência dos **Pixel Indie Games**.

Características visuais:

* Pixel Art
* Interface gráfica temática
* Personagens estilizados
* Itens colecionáveis desenhados manualmente
* Ambiente inspirado em áreas rurais alemãs

---

## 🔊 Sistema de Áudio

### Sons dos Personagens

**Stefan**

* "Gag de la Gag" ao coletar itens

**Fred**

* "Fechei" ao coletar itens

### Sons Especiais

| Evento                  | Áudio                    |
| ----------------------- | ------------------------ |
| Música de Fundo         | Nena - 99 Luftballons    |
| Coleta da Gaita de Fole | Som de gaita de fole     |
| Coleta da Cerveja Alemã | Música "A Praieira"      |
| Coleta da APS           | Fail Sound Effect (SFX)  |
| Coleta do Gato ruivo    | Som de um miado          |
| Vitória                 | Efeito sonoro de vitória |
| Derrota                 | Efeito sonoro de derrota |


---

## 🖥️ Telas do Jogo

O projeto possui:

* Tela inicial
* Tela de vitória
* Tela de derrota

Todas as telas utilizam frases temáticas em alemão para reforçar a identidade do jogo.

---

## 🏗️ Arquitetura do Projeto

A estrutura do projeto foi organizada para facilitar a manutenção do código e permitir melhor desenvolvimento do jogo e a organização entre os membros da equipe.

```

│
├── main.py
├── backup.py
├── README.md
│
├── assets/
│   │
│   ├── sprites/
│   │
│   └── sons/
│
├── game/
│   │
│   ├── classes.py
│   ├── players.py
│   ├── funcoes.py
│   ├── constantes.py
│   ├── tela.py
│   └── musicas.py
│
├── .vscode/
│
└── __pycache__/

```

## ⚠️ Dificuldades Encontradas

* Aprender a utilizar Git e GitHub de forma colaborativa;
* Modularizar o código adequadamente;
* Implementar obstáculos e colisões no mapa;
* Organizar o trabalho em equipe;
* Integrar diferentes partes do sistema desenvolvidas por membros distintos.

---

## 📋 Divisão do Trabalho

### Alice de Medeiros Costa

* Criação dos sprites dos personagens;
* Criação dos sprites das portas lógicas;
* Criação dos sprites dos multiplexadores, demultiplexadores e flip-flops;
* Desenvolvimento das telas de início, vitória e derrota.

### Breno Alves Chagas Rabelo

* Implementação da lógica de spawn dos coletáveis;
* Sistema de substituição dos itens coletados;
* Lógica de animação dos personagens;
* Adição do som de derrota;
* Aprimoramento geral da lógica do jogo.

### Frederico Hazin Costa

* Criação dos sprites do mapa;
* Criação das animações dos personagens;
* Criação do sprite da gaita de fole.

### Kaio Ruan da Silva Barros

* Desenvolvimento da classe de coletáveis;
* Aprimoramento da movimentação;
* Implementação dos obstáculos;
* Sistema de inventário;
* Implementação das telas de vitória e derrota;
* Melhorias na tela inicial.

### Nina Tiné Cantilino

* Desenvolvimento da classe Personagem;
* Implementação inicial da movimentação;
* Criação de sprites das portas lógicas e do gato;
* Implementação de obstáculos;
* Sistema de tempo;
* Integração dos efeitos sonoros.

### Sofia Mendonça

* Criação de sprites;
* Organização do GitHub;
* Modularização do código.

---

## 📚 Lições Aprendidas

O desenvolvimento deste projeto proporcionou uma importante experiência prática.

Principais aprendizados:

* Trabalho colaborativo em equipe;
* Comunicação eficiente entre os integrantes;
* Utilização de Git e GitHub para controle de versão;
* Aplicação de Programação Orientada a Objetos (POO);
* Estruturação e modularização de projetos maiores;
* Desenvolvimento de jogos utilizando a biblioteca Pygame;
* Planejamento e divisão de tarefas;
* Resolução de problemas em equipe.

---

## 🚀 Tecnologias Utilizadas

* Python
* Pygame
* Git
* GitHub
* Piskel

---

## 🏫 Informações Acadêmicas

**Universidade Federal de Pernambuco (UFPE)**
**Centro de Informática (CIn)**
**Bacharelado em Ciência da Computação**

Projeto Final – Introdução à Programação (IP)
