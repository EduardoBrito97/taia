import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from Config import NUM_XS
from Config import NUM_POP
from Config import LIM_MIN
from Config import LIM_MAX

def funcaoAckley(individuo):
  somaXiQuadrado = 0
  somaCosXi = 0
  for xi in individuo:
    somaXiQuadrado += xi*xi
    somaCosXi += math.cos(math.pi * 2 * xi)
  
  exp1 = -0.2*math.sqrt(somaXiQuadrado/NUM_XS)
  primeiraExpressao = -20 * np.exp(exp1)

  exp2 = somaCosXi / NUM_XS
  segundaExpressao = -np.exp(exp2)
  
  resultadoPuro = primeiraExpressao + segundaExpressao + 20 + np.exp(1)
  return round(resultadoPuro, 15)

def calculaFitness(individuo):
  return 1 / (1 + funcaoAckley(individuo))

def desvioPadrao(elementos):
  mi = sum(elementos)/len(elementos)
  soma = 0
  for i in elementos:
    soma += abs(i - mi)**2
  return ((soma/len(elementos))**0.5)

def iniciarPopulacao():
  populacao = []
  while (len(populacao) < NUM_POP):
    individuo = geraIndividuo()
    if (not individuo in populacao):
      populacao.append(individuo)

  return populacao

def geraIndividuo():
  individuo = []
  for _ in range(NUM_XS):
    individuo.append(random.uniform(LIM_MIN, LIM_MAX))
  return individuo