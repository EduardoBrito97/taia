# Especificação 'Função Ackley'

## Projeto
Desenvolvimento de um Algoritmo Evolucionário (Estratégia Evolutiva) para a determinação do ponto de mínimo global da função de Ackley, definida por:

![Função](funcao.jpg)

- Considere n = 30 e -15 ≤ xi ≤ 15.

Cada equipe, de no máximo de 3 integrantes, deverá implementar um Algoritmo
Evolutivo (Estratégia Evolutiva) em qualquer linguagem de programação. 

## Relatório
Além da implementação, a equipe deverá gerar um relatório descrevendo a sua implementação, dando ênfase nos tópicos:
1) Descrição esquemática do algoritmo implementado;
2) Descrição dos processos de:
    - Representação das soluções (indivíduos)
    - Função de Fitness
    - População (tamanho, inicialização, etc)
    - Processo de seleção
    - Operadores Genéticos (Recombinação e Mutação)
    - Processo de seleção por sobrevivência
    - Condições de término do Algoritmo Evolucionário
3) Descrição dos resultados experimentais

*** Compare com uma modificação da própria Estratégia Evolutiva, ou com um Algoritmo Genérico (Real)


## Especificação definida pelo grupo
- Representação (Indivíduo): Um array de 30 números reais.
- Função de Fitness: 1 / (1 + função de Ackley no indivíduo).
- População:
    - Tamanho: 100.
    - Inicialização:
        - Números reais aleatórios entre -15 e 15.
        - Sem repetição.
- Processo de seleção: 
    - Melhores pais aleatórios com elitismo.
- Operadores genéticos:
    - Recombinação: Crossover modificado.
    - Mutação: Mutação Não Uniforme modificada.
- Probabilidade de mutação: 5%.
- Probabilidade de recombinação: 5%.
- Condições de término: 10000 gerações ou fitness > 0.999. Arredondamento de 7 casas decimais.
- Indivíduos encontrados em 20 execuções disponíveis em "Resultado Ecnontrados 20 execuções.txt".

## Métodos implementados
### Seleção
- Melhores pais / piores indivíduos
- Matar metade da população
- Sobrevivência dos mais fortes
- Melhores pais aleatórios com elitismo

### Cruzamento
- Cruzamento Discreto
- Cruzamento Intermediário
- Cruzamento BLX (Blend)
- Crossover modificado

### Mutação
- Mutação Uniforme
- Mutação Não Uniforme
- Mutação Gaussiana
- Mutação BLX
- Mutação Não Uniforme modificada

## Notas
    Para uma maior descrição dos métodos e dos resultados encontrados, favor verificar em "Relatório.pdf".