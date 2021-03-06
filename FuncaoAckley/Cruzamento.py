import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict
from Config import NUM_XS
from Config import PASSO_BLX_MAX
from Config import ROUNDING
from Auxiliar import calculaFitness

def cruzar(pai1, pai2, metUsado):
  if metUsado % 100 < 20:
    return cruzamentoDiscreto(pai1, pai2, 2)
  elif metUsado % 100 < 30:
    return cruzamentoIntermediario(pai1, pai2, 2)
  elif metUsado % 100 < 40:
    return cruzamentoBlx(pai1, pai2, 2)
  elif metUsado % 100 < 50:
    return cruzamentoCrossover(pai1, pai2, 1)
  else:
    raise Exception("No method recognized for crossing.")

def cruzamentoDiscreto(pai1, pai2, numFilhos):
  filhos = []
  for _ in range(numFilhos):
    filho = []
    for i in range(NUM_XS):
      filho.append((pai1[i] * 0.5) + (pai2[i] * 0.5))
    filhos.append(filho)

  return filhos

def cruzamentoIntermediario(pai1, pai2, numFilhos):
  filhos = []
  fitnessPai1 = calculaFitness(pai1)
  fitnessPai2 = calculaFitness(pai2)
  probPai1 = fitnessPai1 / (fitnessPai1 + fitnessPai2)
  probPai2 = fitnessPai2 / (fitnessPai1 + fitnessPai2)
  for _ in range(numFilhos):
    filho = []
    for i in range(NUM_XS):
      filho.append(round((pai1[i] * probPai1) + (pai2[i] * probPai2), ROUNDING))
    filhos.append(filho)

  return filhos

def cruzamentoBlx(pai1, pai2, numFilhos):
  filhos = []
  for _ in range(numFilhos):
    filho = []
    for i in range(NUM_XS):
      menor = min(pai1[i], pai2[i])
      maior = max(pai1[i], pai2[i])

      delta = (maior - menor)
      xi = round(random.uniform(menor - (PASSO_BLX_MAX * delta), maior + (PASSO_BLX_MAX * delta)), ROUNDING) % 15
      filho.append(xi)
    filhos.append(filho)

  return filhos

def cruzamentoCrossover(pai1, pai2, numFilhos):
  filhos = []
  halfA = []
  halfB = []
  for _ in range(numFilhos):
    filho = []
    cutPoint = random.randint(0,len(pai1))
    halfA = pai1[0:cutPoint] + pai2[cutPoint:]
    halfB = pai2[0:cutPoint] + pai1[cutPoint:]
    multiplier = 0.5 * random.uniform(0.0, 1.0)
    halfA = [i * multiplier for i in halfA]
    halfB = [i * multiplier for i in halfB]
    filho = [x + y for x, y in zip(halfA, halfB)]
    filhos.append(filho)
  return filhos