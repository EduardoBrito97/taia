import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict
from Mutacao import realizarMutacao
from Selecao import realizarCruzamento
from Auxiliar import iniciarPopulacao
from Auxiliar import calculaFitness
from Auxiliar import desvioPadrao
from Config import FITNESS_DESEJADO
from Config import MAPA_NUM_METODO
from Config import NUM_AMOSTRAGEM
from Config import NUM_MAX_GERACOES

MET_USADO = 0

MELHOR_INDIVIDUO = []
FITNESS_MELHOR_INDIVIDUO = []
SOMA = []
MEDIA = []

def main():
  global MET_USADO

  mapaMetodoPassos = {}
  mapaMetodoMedias = {}
  mapaMetodoMediasMelhorIndividuo = {}
  mapaMetodoTempos = {}
  mapaMetodoSomas = {}

  for metodo in MAPA_NUM_METODO.keys():
    mapaMetodoPassos[metodo] = []
    mapaMetodoMedias[metodo] = []
    mapaMetodoMediasMelhorIndividuo[metodo] = []
    mapaMetodoTempos[metodo] = []
    mapaMetodoSomas[metodo] = []

  for i in range(0, NUM_AMOSTRAGEM):
    populacao = iniciarPopulacao()
    print("Amostragem " + str(i) + " inciada.")
    for metodo in MAPA_NUM_METODO.keys():
      MET_USADO = metodo
      populacaoUsada = populacao.copy()

      comeco = time.time()
      numPassosAgora = rodarPrograma(populacaoUsada)
      mapaMetodoTempos[metodo].append(time.time() - comeco)

      mapaMetodoPassos[metodo].append(numPassosAgora)

      mediaFitnessAgora = sum(MEDIA)/len(MEDIA)
      mapaMetodoMedias[metodo].append(mediaFitnessAgora)
      
      mediaFitnessMelhorIndividuoAgora = sum(FITNESS_MELHOR_INDIVIDUO)/len(FITNESS_MELHOR_INDIVIDUO)
      mapaMetodoMediasMelhorIndividuo[metodo].append(mediaFitnessMelhorIndividuoAgora)

      mediaSomaAgora = sum(SOMA)/len(SOMA)
      mapaMetodoSomas[metodo].append(mediaSomaAgora)
      if numPassosAgora < NUM_MAX_GERACOES:
        print("Método " + str(MET_USADO) + " convergiu!" + " Melhor indivíduo encontrado: " + str(MELHOR_INDIVIDUO[-1]))

  pegaDadosPlotaGraficos(mapaMetodoPassos, mapaMetodoMedias, mapaMetodoMediasMelhorIndividuo, mapaMetodoTempos, mapaMetodoSomas)

def rodarPrograma(populacao):
  resetarVarGlobais()
  atualizaDados(populacao)
  numGeracoes = 1
  while (numGeracoes <= NUM_MAX_GERACOES 
          and FITNESS_MELHOR_INDIVIDUO[-1] < FITNESS_DESEJADO):
    populacao = realizarCruzamento(populacao, MET_USADO)
    populacao = realizarMutacao(populacao, MET_USADO)
    atualizaDados(populacao)
    numGeracoes += 1

  return numGeracoes

def resetarVarGlobais():
  global SOMA, FITNESS_MELHOR_INDIVIDUO, MEDIA, MELHOR_INDIVIDUO
  SOMA = []
  FITNESS_MELHOR_INDIVIDUO = []
  MEDIA = []
  MELHOR_INDIVIDUO = []

def atualizaDados(populacao):
  global SOMA, MEDIA, MELHOR_INDIVIDUO, FITNESS_MELHOR_INDIVIDUO
  SOMA.append(0)
  melhor_individuo = 0
  fitness_melhor_individuo = 0
  for individuo in populacao:
    fitness = calculaFitness(individuo)
    SOMA[-1] = SOMA[-1] + fitness
    if (fitness > fitness_melhor_individuo):
      fitness_melhor_individuo = fitness
      melhor_individuo = individuo

  MELHOR_INDIVIDUO.append(melhor_individuo)
  FITNESS_MELHOR_INDIVIDUO.append(fitness_melhor_individuo)
  MEDIA.append(SOMA[-1] / len(populacao))
  return

def pegaDadosPlotaGraficos(mapaMetodoPassos, mapaMetodoMedias, mapaMetodoMediasMelhorIndividuo, mapaMetodoTempos, mapaMetodoSomas):
  x_mP=[]
  x_mF=[]
  x_mFM=[]
  x_mTE=[]
  x_mS=[]
  x_mP_Error=[]
  x_mF_Error=[]
  x_mFM_Error=[]
  x_mTE_Error=[]
  x_mS_Error=[]
  for metodo in MAPA_NUM_METODO.keys():
    mediaPassos = sum(mapaMetodoPassos[metodo])/len(mapaMetodoPassos[metodo])
    mediaFitness = sum(mapaMetodoMedias[metodo])/len(mapaMetodoMedias[metodo])
    mediaFitnessMelhorIndividuo = sum( mapaMetodoMediasMelhorIndividuo[metodo])/len(mapaMetodoMediasMelhorIndividuo[metodo])
    mediaTempoExecucao = sum(mapaMetodoTempos[metodo])/len(mapaMetodoTempos[metodo])
    mediaSoma = sum(mapaMetodoSomas[metodo])/len(mapaMetodoSomas[metodo])
    x_mP.append(mediaPassos)
    x_mF.append(mediaFitness)
    x_mFM.append(mediaFitnessMelhorIndividuo)
    x_mTE.append(mediaTempoExecucao)
    x_mS.append(mediaSoma)
    x_mP_Error.append(desvioPadrao(mapaMetodoPassos[metodo]))
    x_mF_Error.append(desvioPadrao(mapaMetodoMedias[metodo]))
    x_mFM_Error.append(desvioPadrao(mapaMetodoMediasMelhorIndividuo[metodo]))
    x_mTE_Error.append(desvioPadrao(mapaMetodoTempos[metodo]))
    x_mS_Error.append(desvioPadrao(mapaMetodoSomas[metodo]))
    print('Quantidade de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaPassos))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoPassos[metodo])))
    print('Média de fitness para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaFitness))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoMedias[metodo])))
    print('Média de fitness melhores individuos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaFitnessMelhorIndividuo))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoMediasMelhorIndividuo[metodo])))
    print('Média tempo de execução para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaTempoExecucao) + ' segundos')
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoTempos[metodo])))
    print('Média de soma de fitness para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaSoma))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoSomas[metodo])))

    print('------------------------------------------------------------------------------------------------')

  plotGraficos(x_mP,x_mF,x_mFM,x_mTE,x_mS,x_mP_Error,x_mF_Error,x_mFM_Error,x_mTE_Error,x_mS_Error, MAPA_NUM_METODO.keys())

def plotGraficos(y_mP,y_mF,y_mFM,y_mTE,y_mS,y_mP_Error,y_mF_Error,y_mFM_Error,y_mTE_Error,y_mS_Error,x):
  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mP,yerr=y_mP_Error, color='green')
  plt.xlabel("Métodos")
  plt.ylabel("Quantidade de Passos")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mF,yerr=y_mF_Error, color='orange')
  plt.xlabel("Métodos")
  plt.ylabel("Média de fitness")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mFM,yerr=y_mFM_Error, color='blue')
  plt.xlabel("Métodos")
  plt.ylabel("Média de fitness melhores individuos ")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mTE,yerr=y_mTE_Error, color='red')
  plt.xlabel("Métodos")
  plt.ylabel("Média tempo de execução")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mS,yerr=y_mS_Error, color='purple')
  plt.xlabel("Métodos")
  plt.ylabel("Média de soma de fitness")
  plt.xticks(x_pos, x)
  plt.show()

main()