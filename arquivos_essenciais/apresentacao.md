# Simulação de Sistema de Emergência Hospitalar
## Equipe: [Nomes dos membros]

## 1. Descrição do Sistema
O sistema simulado representa um departamento de emergência hospitalar com cinco filas principais:
- Triagem (M/M/3/15)
- Emergência (M/M/4/12)
- Consulta (M/M/4/20)
- Internação (M/M/4/15)
- Alta (M/M/2/25)

## 2. Modelo de Filas
O sistema utiliza notação de Kendall para representar as filas:
- M/M/s/K onde:
  - M: Distribuição de chegadas Poisson
  - M: Distribuição de serviço Exponencial
  - s: Número de servidores
  - K: Capacidade da fila

## 3. Resultados da Simulação

### 3.1 Métricas Gerais
| Métrica | Modelo Original | Modelo Melhorado V2 | Melhoria |
|---------|----------------|-------------------|----------|
| Tempo Total (min) | 10000 | 234290.42 | +224290.42 |
| Clientes Perdidos | 7066 | 620 | -91.23% |
| Throughput Total | 0.1000 | 0.1000 | 0% |
| Tempo Médio de Resposta | 1047.94 | 363.46 | -65.32% |

### 3.2 Análise por Fila

#### Triagem (M/M/3/15)
- População Média: 0.45 (-18.18%)
- Throughput: 0.1000 (0%)
- Utilização: 14.98% (-45.49%)
- Tempo de Resposta: 0.00 (0%)
- Clientes Perdidos: 0 (0%)

#### Emergência (M/M/4/12)
- População Média: 0.68 (-26.09%)
- Throughput: 0.0304 (0%)
- Utilização: 17.10% (-43.99%)
- Tempo de Resposta: 0.00 (-100%)
- Clientes Perdidos: 0 (0%)

#### Consulta (M/M/4/20)
- População Média: 1.05 (-33.12%)
- Throughput: 0.0696 (0%)
- Utilização: 26.16% (-62.51%)
- Tempo de Resposta: 0.00 (-100%)
- Clientes Perdidos: 0 (0%)

#### Internação (M/M/4/15)
- População Média: 14.74 (+115.18%)
- Throughput: 0.0296 (+428.57%)
- Utilização: 99.86% (-0.13%)
- Tempo de Resposta: 363.46 (-65.32%)
- Clientes Perdidos: 620 (-91.23%)

#### Alta (M/M/2/25)
- População Média: 0.29 (+3.57%)
- Throughput: 0.0973 (+32.92%)
- Utilização: 14.58% (-43.07%)
- Tempo de Resposta: 0.02 (-94.44%)
- Clientes Perdidos: 0 (0%)

## 4. Análise de Gargalos
O principal gargalo identificado foi na fila de internação:
- Alta utilização (99.86%)
- Aumento significativo na população média (+115.18%)
- Maior tempo de resposta entre todas as filas (363.46 minutos)

## 5. Melhorias Propostas
1. Aumento de servidores na fila de internação
2. Otimização dos fluxos entre filas
3. Ajuste nos parâmetros de chegada
4. Monitoramento contínuo da população média

## 6. Conclusões
1. Melhorias significativas foram alcançadas:
   - Redução de 91.23% nos clientes perdidos
   - Redução de 65.32% no tempo médio de resposta
   - Aumento de 428.57% no throughput da internação

2. Pontos de atenção:
   - Fila de internação ainda apresenta desafios
   - Necessidade de monitoramento contínuo
   - Possibilidade de ajustes adicionais

## 7. Referências
1. Kendall, D. G. (1953). Stochastic Processes Occurring in the Theory of Queues and their Analysis by the Method of the Imbedded Markov Chain
2. Gross, D., & Harris, C. M. (1998). Fundamentals of Queueing Theory
3. Law, A. M., & Kelton, W. D. (2000). Simulation Modeling and Analysis 