import random

class JogoCobrinha:
    def __init__(self, largura=20, altura=20):
        self.largura = largura
        self.altura = altura
        self.reset()

    def reset(self):
        meio_x = self.largura // 2
        meio_y = self.altura // 2
        self.corpo = [
            (meio_x, meio_y),
            (meio_x - 1, meio_y),
            (meio_x - 2, meio_y)
        ]
        self.direcao = (1, 0)
        self.fim_de_jogo = False
        self.score = 0
        self.passos = 0
        self.passos_sem_comer = 0
        self.spawn_apple()

    def spawn_apple(self):
        posicoes_livres = [
            (x, y)
            for x in range(self.largura)
            for y in range(self.altura)
            if (x, y) not in self.corpo
        ]
        if posicoes_livres:
            self.maca = random.choice(posicoes_livres)
        else:
            self.maca = None

    def passo(self, acao=None):
        if self.fim_de_jogo:
            return

        if acao is not None:
            if isinstance(acao, int):
                dx, dy = self.direcao
                if acao == 1:
                    self.direcao = (dy, -dx)
                elif acao == 2:
                    self.direcao = (-dy, dx)
            elif isinstance(acao, tuple) and len(acao) == 2:
                dx_nova, dy_nova = acao
                dx_atual, dy_atual = self.direcao
                if dx_nova * dx_atual + dy_nova * dy_atual != -1:
                    self.direcao = acao

        cabeca_x, cabeca_y = self.corpo[0]
        nova_cabeca = (cabeca_x + self.direcao[0], cabeca_y + self.direcao[1])

        if (nova_cabeca[0] < 0 or nova_cabeca[0] >= self.largura or
            nova_cabeca[1] < 0 or nova_cabeca[1] >= self.altura or
            nova_cabeca in self.corpo):
            self.fim_de_jogo = True
            return

        self.corpo.insert(0, nova_cabeca)

        if nova_cabeca == self.maca:
            self.score += 1
            self.passos_sem_comer = 0
            self.spawn_apple()
        else:
            self.corpo.pop()
            self.passos_sem_comer += 1

        self.passos += 1
