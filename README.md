# 🐍🧠 NeuroEvolution Snake (Cobrinha IA)

Este projeto implementa o clássico jogo da cobrinha (Snake) com uma arquitetura de engenharia de software desacoplada, projetada especificamente para suportar o treinamento de inteligência artificial através de **Neuroevolução** (Rede Neural Artificial + Algoritmo Genético).

---

## 📌 Estado Atual do Projeto

O projeto encontra-se na fase de **Core Engine e Interface Visual**. Toda a física do jogo, regras, renderização e controle de loop manual estão prontos e testados. 

### Módulos Implementados

1. **[jogo.py](jogo.py)**: Lógica pura do jogo.
   - Controla o corpo da cobra, spawn de maçãs, contagem de passos e colisão física (paredes e corpo).
   - **Independência de Interface**: Não utiliza nenhuma biblioteca gráfica, permitindo rodar em modo *headless* (sem tela) para treinamento em alta velocidade (lote).
   - **Rastreamento de Métricas**: Já computa as variáveis cruciais para a função de aptidão (*fitness*):
     - `score`: Número de maçãs comidas.
     - `passos`: Tempo total de sobrevivência.
     - `passos_sem_comer`: Contador de inatividade para penalizar e evitar loops infinitos.

2. **[visualizacao.py](visualizacao.py)**: Engine de renderização com Pygame.
   - Visual moderno em *Slate Dark Mode* e gradientes de cor ao longo do corpo da cobra.
   - Detalhes visuais (olhos dinâmicos na cabeça da cobra que se orientam de acordo com a direção).
   - **Resiliência a Dependências**: Suporta fallback automático e logs em terminal caso o sistema operacional não tenha suporte à renderização de fontes TTF do Pygame.

3. **[main.py](main.py)**: Orquestrador do loop de jogo (10 FPS) e manipulador de eventos de entrada física (teclado).
   - Suporte a comandos manuais (W, A, S, D ou setas direcionais).
   - Atalhos rápidos de pausa (`Space` ou `P`) e reinicialização (`R` após fim de jogo).

---

## 🧠 Preparado para Neuroevolução

A arquitetura do motor de jogo foi desenhada sob medida para plugar a IA nos próximos passos:
* **Entradas (Sensores)**: O estado da cobra e da maçã em [jogo.py](jogo.py) será convertido em 11 sensores booleanos (direção da maçã, perigo imediato à frente, esquerda e direita).
* **Saídas (Decisões Relativas)**: O método `passo()` de [jogo.py](jogo.py#L32) aceita ações de rotação relativa de 90° (`0 = seguir em frente`, `1 = virar esquerda`, `2 = virar direita`), mapeando exatamente as 3 saídas da Rede Neural Multicamadas (MLP) a ser implementada.

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de possuir o Python instalado em sua máquina. Instale as dependências executando:

```bash
pip install -r requirements.txt
```

### Jogar Manualmente
Para testar os controles físicos, movimentação e renderização:

```bash
python main.py
```

* **Mover**: Setas direcionais ou `W`/`A`/`S`/`D`
* **Pausar**: Barra de Espaço ou `P`
* **Reiniciar**: `R` (quando a tela exibir "FIM DE JOGO")

---

## 👥 Participantes do Projeto

* **Adiel Emilson**
* **Carlos Adauto**
* **Ricardo Pistori**
* **Guilherme Rocha**
