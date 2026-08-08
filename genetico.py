import random
import numpy as np

def selecao_torneio(populacao, fitness_scores, tamanho_torneio=5):
    indices_sorteados = random.sample(range(len(populacao)), tamanho_torneio)
    
    melhor_indice = indices_sorteados[0]
    maior_fitness = fitness_scores[melhor_indice]
    
    for idx in indices_sorteados[1:]:
        if fitness_scores[idx] > maior_fitness:
            maior_fitness = fitness_scores[idx]
            melhor_indice = idx
            
    return populacao[melhor_indice]

def crossover(pesos_pai, pesos_mae):
    tamanho = len(pesos_pai)
    pesos_filho = np.zeros(tamanho)
    
    for i in range(tamanho):
        if random.random() < 0.5:
            pesos_filho[i] = pesos_pai[i]
        else:
            pesos_filho[i] = pesos_mae[i]
            
    return pesos_filho

def mutacao(pesos, taxa=0.1):
    pesos_mutados = np.copy(pesos)
    tamanho = len(pesos_mutados)
    
    for i in range(tamanho):
        if random.random() < taxa:
            ruido = random.uniform(-0.5, 0.5)
            pesos_mutados[i] += ruido
            
    return pesos_mutados

def elitismo(populacao, fitness_scores, n=5):
    pares = list(zip(populacao, fitness_scores))
    
    pares_ordenados = sorted(pares, key=lambda par: par[1], reverse=True)
    
    elite = [par[0] for par in pares_ordenados[:n]]
    
    return elite