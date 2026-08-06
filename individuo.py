def calcular_posicao(cabeca: tuple, direcao_atual: str, direcao_relativa: str) -> tuple:
    x, y = cabeca
    if(direcao_atual == 'norte'):
        if(direcao_relativa == 'frente'):
            return (x, y-1)
        elif(direcao_relativa == 'esquerda'):
            return (x-1, y)
        elif(direcao_relativa == 'direita'):
            return (x+1, y)
        else:
            return cabeca
    elif(direcao_atual == 'oeste'):
        if(direcao_relativa == 'frente'):
            return (x-1, y)
        elif(direcao_relativa == 'esquerda'):
            return (x, y+1)
        elif(direcao_relativa == 'direita'):
            return (x, y-1)
        else:
            return cabeca   
    elif(direcao_atual == 'leste'):
        if(direcao_relativa == 'frente'):
            return (x+1, y)
        elif(direcao_relativa == 'esquerda'):
            return (x, y-1)
        elif(direcao_relativa == 'direita'):
            return (x, y+1)
        else:
            return cabeca
    elif(direcao_atual == 'sul'):
        if(direcao_relativa == 'frente'):
            return (x, y+1)
        elif(direcao_relativa == 'esquerda'):
            return (x+1, y)
        elif(direcao_relativa == 'direita'):
            return (x-1, y)
        else:
            return cabeca
    else:
        return cabeca

def eh_perigo(proxima_posicao: tuple, corpo: list) -> int:
    """
    Retorna 1 se houver perigo e 0 se não 
    """
    if(proxima_posicao in corpo): return 1
    if(proxima_posicao[0] < 0 or proxima_posicao[0] >= 20): return 1
    if(proxima_posicao[1] < 0 or proxima_posicao[1] >= 20): return 1 
    return 0



def calcular_sensores(estado_jogo: dict) -> tuple:
    cabeca = estado_jogo['cabeca'] # posicao (x, y)
    direcao = estado_jogo['direcao'] # "Norte, sul, leste, oeste"
    corpo = estado_jogo['corpo'] # lista de posicoes
    maca = estado_jogo['maca'] # posicao (x, y) da maçã

    posicao_frente = calcular_posicao(cabeca, direcao, 'frente')
    posicao_direita = calcular_posicao(cabeca, direcao, 'direita')
    posicao_esquerda = calcular_posicao(cabeca, direcao, 'esquerda')

    perigo_frente = eh_perigo(posicao_frente, corpo)
    perigo_direita = eh_perigo(posicao_direita, corpo)
    perigo_esquerda = eh_perigo(posicao_esquerda, corpo)

    dir_norte = 1 if direcao == 'norte' else 0
    dir_sul = 1 if direcao == 'sul' else 0
    dir_leste = 1 if direcao == 'leste' else 0
    dir_oeste = 1 if direcao == 'oeste' else 0

    maca_esquerda = 1 if maca[0] < cabeca[0] else 0
    maca_direita = 1 if maca[0] > cabeca[0] else 0
    maca_abaixo = 1 if maca[1] > cabeca[1] else 0
    maca_acima = 1 if maca[1] < cabeca[1] else 0

    return (
        perigo_frente, perigo_direita, perigo_esquerda, 
        dir_norte, dir_sul, dir_leste, dir_oeste,
        maca_esquerda, maca_direita, maca_acima, maca_abaixo
    )

def calcular_fitness(passos: int, macas_comidas: int, passos_sem_comer: int) -> float:
    pontos_sobrevivencia = passos
    pontos_comida = (macas_comidas**2) * 100
    penalidade = passos_sem_comer / 2

    fitness = pontos_sobrevivencia + pontos_comida - penalidade 

    return max(fitness, 1)

def registrar_geracao(historico, fitness_scores):
    media = sum(fitness_scores) / len(fitness_scores)
    maximo = max(fitness_scores)

    historico['media'].append(media)
    historico['maximo'].append(maximo)

class Individuo:
    def __init__(self):
        self.rede = 0
        self.passos = 0
        self.macas_comidas = 0
        self.passos_sem_comer = 0
        self.fitness = 0
        self.vivo = 0

    def decidir_acao(self, estado_jogo: dict):
        sensores = calcular_sensores(estado_jogo)
        acao = self.rede.prever(sensores)
        return acao 

    def registrar_passo(self, comeu_maca: bool):
        self.passos += 1
        if(comeu_maca):
            self.macas_comidas += 1
            self.passos_sem_comer = 0
        else:
            self.passos_sem_comer += 1
    
    def finalizar(self):
        self.fitness = calcular_fitness(self.passos, self.macas_comidas, self.passos_sem_comer)
        return self.fitness




if __name__ == '__main__':
    # apenas para teste, desconsiderem
    estado_fake = {
        "cabeca": (5, 5),
        "direcao": 'norte',
        'corpo': [(5,5), (5, 6), (5, 7)],
        'maca': (8, 2)
    }
    sensores = calcular_sensores(estado_fake)
    print(sensores)

    print(calcular_fitness(passos=150, macas_comidas=3, passos_sem_comer=20))