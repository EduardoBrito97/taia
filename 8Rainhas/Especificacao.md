# Especificação de Projeto - "8 Rainhas"

## Primeira parte
- Representação (genótipo): string de bits
- Recombinação: “cut-and-crossfill” crossover
- Probabilidade de Recombinação: 90%
- Mutação: troca de genes
- Probabilidade de Mutação: 40%
- Seleção de pais: ranking - Melhor de 2 de 5 escolhidos aleatoriamente
- Seleção de sobreviventes: substituição do pior
- Tamanho da população: 100
- Número de filhos gerados: 2
- Inicialização: aleatória
- Condição de término: Encontrar a solução, ou 10.000 avaliações de fitness
- Fitness?

## Segunda parte
- Implementar possíveis melhorias mudando:
    - Representação
    - Recombinação 
    - Mutação
    - Seleção de pais – roleta?
    - Seleção de sobreviventes: geracional ou substituição do pior
    - Tamanho da população: 10? 30? 50? 70? 120? 200?
    - O fitness pode ser melhorado?