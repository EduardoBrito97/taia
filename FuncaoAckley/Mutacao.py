import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict
from Auxiliar import desvioPadrao
from Auxiliar import calculaFitness
from Config import LIM_MIN
from Config import LIM_MAX
from Config import PROB_MUTACAO
from Config import PESO_FITNESS_IDV_MUTACAO
from Config import PASSO_BLX_MAX
from Config import ROUNDING

def realizarMutacao(populacao, metUsado):
    if metUsado % 10 == 1:
        return mutacaoUniforme(populacao)
    elif metUsado % 10 == 2:
        return mutacaoNaoUniforme(populacao)
    elif metUsado % 10 == 3:
        return mutacaoGaussiana(populacao)
    elif metUsado % 10 == 4:
        return mutacaoBlx(populacao)
    elif metUsado % 10 == 5:
        return mutacaoAditiva(populacao)
    else:
        raise Exception("No method recognized for mutation.")

def mutacaoUniforme(populacao):
  novaPop = []
  for individuo in populacao:
    novoIndividuo = []
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        novoX = round(random.uniform(LIM_MIN, LIM_MAX), ROUNDING)

      novoIndividuo.append(novoX)
    novaPop.append(novoIndividuo)

  return novaPop

def mutacaoNaoUniforme(populacao):
  novaPop = []
  for individuo in populacao:
    desvPadr = desvioPadrao(individuo)
    novoIndividuo = []
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        limInferior = (x - desvPadr) % 15
        limSuperior = (x + desvPadr) % 15
        novoX = round(random.uniform(limInferior, limSuperior), ROUNDING)

      novoIndividuo.append(novoX)
    novaPop.append(novoIndividuo)

  return novaPop

def mutacaoGaussiana(populacao):
  novaPop = []
  mu = 0
  sigma = 0.5
  for individuo in populacao:
    dX = random.gauss(mu, sigma)
    novoIndividuo = []
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        novoX = (x + dX) % 15
      novoIndividuo.append(novoX)
      
    novaPop.append(novoIndividuo)

  return novaPop

def mutacaoBlx(populacao):
  novaPop = []
  for individuo in populacao:
    novoIndividuo = []
    fitnessIndividuo = calculaFitness(individuo)
    multiplicadorPorFitness = 1/(fitnessIndividuo*PESO_FITNESS_IDV_MUTACAO)
    passo = PASSO_BLX_MAX * multiplicadorPorFitness
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        novoX = round(random.uniform(x + (LIM_MIN*passo), x + (LIM_MAX*passo)), ROUNDING) % 15
      novoIndividuo.append(novoX)
      
    novaPop.append(novoIndividuo)

  return novaPop

def mutacaoAditiva(populacao):
  novaPop = populacao
  for individuo in novaPop:
    filho = []
    if (PROB_MUTACAO * 100 > random.randint(0, 101)):
      for x in individuo:
        x = x + random.uniform(0.0, 1.0)
        if x > 15:
          x = 15
        elif x < -15:
          x = -15
        filho.append(x)
      populacao.remove(individuo)
      populacao.append(filho)
  return populacao
      