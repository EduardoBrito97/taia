import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict
from Auxiliar import desvioPadrao
from Auxiliar import calculaFitness
from Cruzamento import cruzar
from Config import PROB_RECOMB
from Config import NUM_POP

def realizarCruzamento(populacao, metUsado):
  chanceDaVez = random.randint(0,101)
  if (PROB_RECOMB * 100 < chanceDaVez):
    return populacao

  if metUsado % 1000 < 200:
    pais = pegarMelhoresPais(populacao, 2)
    filhos = cruzar(pais[0], pais[1], metUsado)
    
    pioresIndividuosIndices = pegarIndicesPioresIndividuos(populacao, 2)
    populacao[pioresIndividuosIndices[0]] = filhos[0]
    populacao[pioresIndividuosIndices[1]] = filhos[1]
  
  elif metUsado % 1000 < 300:
    pais = pegarPaisSuperSmashBros(populacao, len(populacao)/2) 
    indexPais = random.sample(range(0, len(pais)), len(pais))
    for i in range(0,len(indexPais),2):
      if i == len(pais) - 1:
        filhos = cruzar(pais[indexPais[i]], pais[indexPais[i]], metUsado)
      else:
        filhos = cruzar(pais[indexPais[i]], pais[indexPais[i+1]], metUsado)
      populacao.append(filhos[0])
      populacao.append(filhos[1])
  
  elif metUsado % 1000 < 400:
    indexesAleatorios = random.sample(range(0, NUM_POP), NUM_POP)
    for i in range(0, NUM_POP, 2):
      if i == NUM_POP - 1: 
        filhos = cruzar(populacao[indexesAleatorios[i]], populacao[indexesAleatorios[i]], metUsado)
      else:
        filhos = cruzar(populacao[indexesAleatorios[i]], populacao[indexesAleatorios[i+1]], metUsado)
      populacao.append(filhos[0])
      populacao.append(filhos[1])
    populacao.sort(reverse=True, key=calculaFitness)
    populacao = populacao[:NUM_POP]
  elif metUsado % 1000 < 500:
    populacaoCopy = populacao
    pais  = pegarMelhoresTorneio(populacao)
    filho = cruzar(pais[0],pais[1],metUsado)[0]
    fitnessPopulacao = list(map(calculaFitness, populacao))
    fitnessPopulacao, populacaoCopy = (list(t) for t in zip(*sorted(zip(fitnessPopulacao, populacaoCopy))))
    if fitnessPopulacao[0]<calculaFitness(filho):
      populacao.remove(populacaoCopy[0])
      populacao.append(filho)
  else:
    raise Exception("No method recognized for selection.")

  return populacao

def pegarPaisSuperSmashBros(populacao, numPais): ###Combate entres os individuos pra saber quem vai ser o pai
  pais = []
  perdedores = []
  while len(pais)<numPais:
    indexCombatentes = random.sample(range(0, len(populacao)), 2)
    combatenteA = populacao[indexCombatentes[0]]
    combatenteB = populacao[indexCombatentes[1]]
    if calculaFitness(combatenteA) > calculaFitness(combatenteB): ###A gente salva os vencedores e mata os perdedores
      pais.append(combatenteA)
      perdedores.append(combatenteB)
      populacao.pop(indexCombatentes[1]) 
    else: 
      pais.append(combatenteB)
      perdedores.append(combatenteA)
      populacao.pop(indexCombatentes[0])
  return pais

def pegarMelhoresPais(populacao, numPais):
  posicaoPais = []
  for i in range(0, NUM_POP):
    posicaoPais.append(random.randint(0, NUM_POP-1))
  
  mapaFitnessIndividuo = {}
  fitnessPais = []
  for posicao in posicaoPais:
    individuo = populacao[posicao]
    fitness = calculaFitness(individuo)
    fitnessPais.append(fitness)
    mapaFitnessIndividuo[fitness] = individuo

  fitnessPais.sort(reverse=True)
  pais = []
  for i in range(0, numPais):
    pais.append(mapaFitnessIndividuo[fitnessPais[i]])

  return pais

def pegarIndicesPioresIndividuos(populacao, numIndividuos):
  fitnessPop = []
  mapaFitnessPosicao = {}
  i = 0
  for individuo in populacao:
    fitness = calculaFitness(individuo)
    fitnessPop.append(fitness)
    mapaFitnessPosicao[fitness] = i
    i += 1
  
  fitnessPop.sort()
  indicesPioresIndividuos = []
  for i in range(0, numIndividuos):
    fitness = fitnessPop[i]
    posicaoFitness = mapaFitnessPosicao[fitness]
    indicesPioresIndividuos.append(posicaoFitness)

  return indicesPioresIndividuos


def pegarMelhoresTorneio(populacao):
  pais = []
  populacaoCopia = populacao
  fitnessPopulacao = list(map(calculaFitness, populacaoCopia))
  fitnessPopulacao, populacaoCopia = (list(t) for t in zip(*sorted(zip(fitnessPopulacao, populacaoCopia))))
  populacaoCopia = populacaoCopia[0:int(len(populacaoCopia)/2)]
  competidores = random.sample(range(0,len(populacaoCopia)), 5)
  competidores.sort()
  pais.append(populacaoCopia[competidores[-1]])
  pais.append(populacaoCopia[competidores[-2]])

  return pais
  