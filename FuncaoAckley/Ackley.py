import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict

NUM_MAX_ITERACOES = 10000
NUM_POP = 100
PROB_MUTACAO = 0.4
PROB_RECOMB = 0.9
NUM_XS = 30
QTD_PAIS = 5

MET_USADO = 0

MELHOR_INDIVIDUO = [[]]
FITNESS_MELHOR_INDIVIDUO = [0]
FITNESS_DESEJADO = 1

SOMA = []
MEDIA = []

NUM_AMOSTRAGEM = 5

MAPA_NUM_METODO = { 0:"CROSSFILL ALEATÓRIO E MUTAÇÃO NORMAL",
                    1:"CROSSFILL E MUTAÇÃO MELHORADOS"}

y=["SM","CM"]

def main():
  global MET_USADO

  mapaMetodoPassos = {}
  mapaMetodoMedias = {}
  mapaMetodoMediasMelhorIndividuo = {}
  mapaMetodoTempos = {}
  mapaMetodoSomas = {}

  for metodo in range(0, len(MAPA_NUM_METODO)):
    mapaMetodoPassos[metodo] = []
    mapaMetodoMedias[metodo] = []
    mapaMetodoMediasMelhorIndividuo[metodo] = []
    mapaMetodoTempos[metodo] = []
    mapaMetodoSomas[metodo] = []

  for i in range(0, NUM_AMOSTRAGEM):
    populacao = iniciarPopulacao()
    print(i)
    for metodo in range(0, len(MAPA_NUM_METODO)):
      MET_USADO = metodo
      populacaoUsada = populacao.copy()

      comeco = time.time()
      numPassosAgora = int(rodarPrograma(populacaoUsada)/NUM_POP)
      mapaMetodoTempos[metodo].append(time.time() - comeco)

      mapaMetodoPassos[metodo].append(numPassosAgora)

      mediaFitnessAgora = sum(MEDIA)/len(MEDIA)
      mapaMetodoMedias[metodo].append(mediaFitnessAgora)
      
      mediaFitnessMelhorIndividuoAgora = sum(FITNESS_MELHOR_INDIVIDUO)/len(FITNESS_MELHOR_INDIVIDUO)
      mapaMetodoMediasMelhorIndividuo[metodo].append(mediaFitnessMelhorIndividuoAgora)

      mediaSomaAgora = sum(SOMA)/len(SOMA)
      mapaMetodoSomas[metodo].append(mediaSomaAgora)

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
  for metodo in MAPA_NUM_METODO:
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

  plotBar(x_mP,x_mF,x_mFM,x_mTE,x_mS,x_mP_Error,x_mF_Error,x_mFM_Error,x_mTE_Error,x_mS_Error,y)

def desvioPadrao(elementos):
  mi = sum(elementos)/len(elementos)
  soma = 0
  for i in elementos:
    soma += abs(i - mi)**2
  return ((soma/len(elementos))**0.5)

def plotBar(y_mP,y_mF,y_mFM,y_mTE,y_mS,y_mP_Error,y_mF_Error,y_mFM_Error,y_mTE_Error,y_mS_Error,x):
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

def rodarPrograma(populacao):
  resetarVarGlobais()
  atualizaInfograficos(populacao)
  numeroFitnessCalculados = NUM_POP
  while (numeroFitnessCalculados <= NUM_MAX_ITERACOES 
          and FITNESS_MELHOR_INDIVIDUO[-1] < FITNESS_DESEJADO):
    populacao = realizarCruzamento(populacao)
    populacao = realizarMutacao(populacao)
    atualizaInfograficos(populacao)
    numeroFitnessCalculados += NUM_POP

  return numeroFitnessCalculados

def resetarVarGlobais():
  global SOMA, FITNESS_MELHOR_INDIVIDUO, MEDIA, MELHOR_INDIVIDUO
  SOMA = []
  FITNESS_MELHOR_INDIVIDUO = []
  MEDIA = []
  MELHOR_INDIVIDUO = []

def iniciarPopulacao():
  populacao = []
  while (len(populacao) < NUM_POP):
    individuo = geraIndividuo()
    if (not individuo in populacao):
      populacao.append(individuo)

  return populacao

def geraIndividuo():
  individuo = []
  for _ in range(30):
    individuo.append(random.uniform(-15, 15))
  return individuo

def atualizaInfograficos(populacao):
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

def calculaFitness(individuo):
  somaXiQuadrado = 0
  for xi in individuo:
    somaXiQuadrado += xi*xi
  
  exp1 = -0.2*math.sqrt(somaXiQuadrado/30)
  primeiraExpressao = -20 * math.exp(exp1)

  somaCosXi = 0
  for xi in individuo:
    somaCosXi = math.cos(math.pi * 2 * xi)
  exp2 = somaCosXi / 30

  segundaExpressao = -math.exp(exp2)

  resultadoCalc = primeiraExpressao + segundaExpressao + 20 + 1
  return 1 / (1 + resultadoCalc)

def realizarCruzamento(populacao):
  chanceDaVez = random.randint(0,101)
  if (PROB_RECOMB * 100 < chanceDaVez):
    return populacao

  if MET_USADO == 0:
    pais = pegarPais(populacao, 2)
    filho1, filho2 = cutCrossfill(pais[0], pais[1])
    
    pioresIndividuosIndices = pegarIndicesPioresIndividuos(populacao, 2)
    populacao[pioresIndividuosIndices[0]] = filho1
    populacao[pioresIndividuosIndices[1]] = filho2
  
  elif MET_USADO == 1:
    pais = pegarPaisSuperSmashBros(populacao, len(populacao)/2) 
    indexPais = random.sample(range(0, len(pais)), len(pais))
    for i in range(0,len(indexPais),2):
      filho1, filho2 = cutCrossfill(pais[indexPais[i]], pais[indexPais[i+1]])
      populacao.append(filho1)
      populacao.append(filho2)

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

def pegarPais(populacao, numPais):
  posicaoPais = []
  for i in range(0, QTD_PAIS):
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

def pegarPaisMelhoradoTorneio(populacao,numPais):
  posicaoPais = []
  for i in range(0, NUM_POP):
    posicaoPais.append(i)

  mapaFitnessIndividuo = {}
  fitnessPais = []
  for posicao in posicaoPais:
    individuo = populacao[posicao]
    fitness = calculaFitness(individuo)
    fitnessPais.append(fitness)
    mapaFitnessIndividuo[fitness] = individuo

  fitnessPais.sort(reverse=True)
  
  campeaoSerieA = fitnessPais[0]
  campeaoSerieB = fitnessPais[int((len(fitnessPais)/2)+1)]
  pais = []
  pais.append(mapaFitnessIndividuo[campeaoSerieA])
  pais.append(mapaFitnessIndividuo[campeaoSerieB])
  return pais

def pegarPaisMelhorado(populacao, numPais):
  posicaoPais = []
  for i in range(0, NUM_POP):
    posicaoPais.append(i)

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

def cutCrossfill(pai1,pai2):
  filho1 = np.zeros(NUM_XS,np.float)
  filho2 = np.zeros(NUM_XS,np.float)
  ponto = random.randint(1,NUM_XS)

  filho1[0:ponto] = pai1[0:ponto]
  filho2[0:ponto] = pai2[0:ponto]

  return filho1, filho2

def edgeRecombination(pai1,pai2):
  filho1 = []
  neighbor = {}
  neighbor = defaultdict(list)
  
  for i in range(0,NUM_XS):
    index_p1 = pai1.index(i)
    index_p2 = pai2.index(i)
    neighbor[str(i)].append(pai1[(index_p1+1)%NUM_XS])
    neighbor[str(i)].append(pai1[(index_p1-1)%NUM_XS])
    if(pai2[(index_p2+1)%8] not in neighbor[str(i)]):
      neighbor[str(i)].append(pai2[(index_p2+1)%NUM_XS])
    if(pai2[(index_p2-1)%8] not in neighbor[str(i)]):
      neighbor[str(i)].append(pai2[(index_p2-1)%NUM_XS])

  X = random.randint(0,NUM_XS-1)
  while(len(filho1)!= NUM_XS):
    filho1.append(X)
    for i in range(0,NUM_XS):
      if X in neighbor[str(i)] : neighbor[str(i)].remove(X)
    Z = X
    if(neighbor[str(X)] == []):
      while(Z not in filho1):
        Z = random.randint(0,NUM_XS-1)
    else:
      tamanho = []
      for j in range(0,len(neighbor[str(X)])):
        index = neighbor[str(X)][j]
        tamanhoVizinho = len(neighbor[str(index)])
        tamanho.append(tamanhoVizinho)
      minVizinho = min(tamanho)

      vizinhos= []
      for j in range(0,len(neighbor[str(X)])):
        index = neighbor[str(X)][j]
        if(minVizinho == len(neighbor[str(index)])):
          vizinhos.append(index)
      
      Z = random.choice(vizinhos)
    
    X = Z
  
  filho = filho1
  if len(filho) == len(set(filho)):
    return filho
  else:
    if calculaFitness(pai1)>calculaFitness(pai2):
      return pai1
    else:
      return pai2

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

def realizarMutacao(populacao):
  novaPop = []
  for individuo in populacao:
    novoIndividuo = []
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        novoX = random.uniform(-15, 15)

      novoIndividuo.append(novoX)
    novaPop.append(novoIndividuo)

  return novaPop

main()