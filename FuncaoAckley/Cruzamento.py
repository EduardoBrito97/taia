import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict
from Config import NUM_XS
from Config import PASSO_BLX_MAX
from Auxiliar import calculaFitness

def cruzar(pai1, pai2, metUsado):
  if metUsado % 100 < 20:
    return cruzamentoDiscreto(pai1, pai2, 2)
  elif metUsado % 100 < 30:
    return cruzamentoIntermediario(pai1, pai2, 2)
  elif metUsado % 100 < 40:
    return cruzamentoBlx(pai1, pai2, 2)
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
      filho.append((pai1[i] * probPai1) + (pai2[i] * probPai2))
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
      xi = random.uniform(menor - (PASSO_BLX_MAX * delta), maior + (PASSO_BLX_MAX * delta)) % 15
      filho.append(xi)
    filhos.append(filho)

  return filhos