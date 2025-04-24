# Simulação de Sistema de Emergência Hospitalar
## Avaliação de Aprendizagem - Simulação e Métodos Analíticos

---

## Equipe
- Nome do Aluno 1
- Nome do Aluno 2
- Nome do Aluno 3

---

## Descrição do Sistema

O sistema modelado representa um departamento de emergência hospitalar com 5 filas principais:

1. **Triagem (M/M/2/10)**
   - 2 atendentes
   - Capacidade de 10 pacientes
   - Recebe chegadas externas
   - Distribui pacientes para emergência (30%) e consulta (70%)

2. **Emergência (M/M/3/8)**
   - 3 médicos
   - Capacidade de 8 pacientes
   - 60% dos pacientes recebem alta
   - 40% são internados

3. **Consulta (M/M/2/12)**
   - 2 médicos
   - Capacidade de 12 pacientes
   - 70% dos pacientes recebem alta
   - 30% são internados

4. **Internação (M/M/1/6)**
   - 1 servidor
   - Capacidade de 6 pacientes
   - 100% dos pacientes recebem alta após internação

5. **Alta (M/M/1/20)**
   - 1 servidor
   - Capacidade de 20 pacientes
   - Ponto final do sistema

---

## Modelo da Rede de Filas

![Diagrama da Rede de Filas Original](diagrama_rede_original.png)

- **Notação de Kendall**: M/M/s/K
  - M: Distribuição de chegadas Markoviana (exponencial)
  - M: Distribuição de serviço Markoviana (exponencial)
  - s: Número de servidores
  - K: Capacidade da fila

- **Tempos de Serviço**:
  - Triagem: 3-8 minutos
  - Emergência: 15-45 minutos
  - Consulta: 10-30 minutos
  - Internação: 120-240 minutos
  - Alta: 2-5 minutos

- **Probabilidades de Roteamento**:
  - Triagem → Emergência: 30%
  - Triagem → Consulta: 70%
  - Emergência → Alta: 60%
  - Emergência → Internação: 40%
  - Consulta → Alta: 70%
  - Consulta → Internação: 30%
  - Internação → Alta: 100%

---

## Resultados da Simulação - Modelo Original

### Probabilidades dos Estados

| Fila | Estado 0 | Estado 1 | Estado 2 | Estado 3 | Estado 4 | Estado 5+ |
|------|----------|----------|----------|----------|----------|-----------|
| Triagem | XX% | XX% | XX% | XX% | XX% | XX% |
| Emergência | XX% | XX% | XX% | XX% | XX% | XX% |
| Consulta | XX% | XX% | XX% | XX% | XX% | XX% |
| Internação | XX% | XX% | XX% | XX% | XX% | XX% |
| Alta | XX% | XX% | XX% | XX% | XX% | XX% |

### Índices de Desempenho

| Fila | População Média | Throughput (clientes/min) | Utilização (%) | Tempo Médio de Resposta (min) | Clientes Perdidos |
|------|-----------------|---------------------------|----------------|-------------------------------|-------------------|
| Triagem | XX | XX | XX% | XX | XX |
| Emergência | XX | XX | XX% | XX | XX |
| Consulta | XX | XX | XX% | XX | XX |
| Internação | XX | XX | XX% | XX | XX |
| Alta | XX | XX | XX% | XX | XX |

---

## Análise de Gargalos

Com base nos resultados da simulação, identificamos os seguintes gargalos no sistema:

1. **Triagem**:
   - Alta utilização (XX%)
   - Tempo médio de resposta elevado (XX minutos)
   - XX clientes perdidos

2. **Emergência**:
   - Alta utilização (XX%)
   - Tempo médio de resposta elevado (XX minutos)
   - XX clientes perdidos

3. **Consulta**:
   - Alta utilização (XX%)
   - Tempo médio de resposta elevado (XX minutos)
   - XX clientes perdidos

4. **Internação**:
   - Alta utilização (XX%)
   - Tempo médio de resposta elevado (XX minutos)
   - XX clientes perdidos

5. **Alta**:
   - Alta utilização (XX%)
   - Tempo médio de resposta elevado (XX minutos)
   - XX clientes perdidos

---

## Proposta de Melhoria

Para resolver os gargalos identificados, propomos as seguintes melhorias:

1. **Triagem**:
   - Aumentar o número de servidores de 2 para 3
   - Aumentar a capacidade da fila de 10 para 15
   - Reduzir o tempo máximo de serviço de 8 para 6 minutos

2. **Emergência**:
   - Aumentar o número de servidores de 3 para 4
   - Aumentar a capacidade da fila de 8 para 10
   - Reduzir o tempo máximo de serviço de 45 para 35 minutos

3. **Consulta**:
   - Aumentar o número de servidores de 2 para 3
   - Aumentar a capacidade da fila de 12 para 15
   - Reduzir o tempo máximo de serviço de 30 para 25 minutos

4. **Internação**:
   - Aumentar o número de servidores de 1 para 2
   - Aumentar a capacidade da fila de 6 para 8
   - Reduzir o tempo máximo de serviço de 240 para 180 minutos

5. **Alta**:
   - Aumentar o número de servidores de 1 para 2
   - Aumentar a capacidade da fila de 20 para 25
   - Reduzir o tempo máximo de serviço de 5 para 4 minutos

---

## Modelo Melhorado

![Diagrama da Rede de Filas Melhorada](diagrama_rede_melhorado.png)

---

## Comparação dos Resultados

### Melhoria nos Índices de Desempenho

| Fila | População Média | Throughput | Utilização | Tempo Médio de Resposta | Clientes Perdidos |
|------|-----------------|------------|------------|------------------------|-------------------|
| Triagem | -XX% | +XX% | -XX% | -XX% | -XX% |
| Emergência | -XX% | +XX% | -XX% | -XX% | -XX% |
| Consulta | -XX% | +XX% | -XX% | -XX% | -XX% |
| Internação | -XX% | +XX% | -XX% | -XX% | -XX% |
| Alta | -XX% | +XX% | -XX% | -XX% | -XX% |

---

## Conclusões

1. **Impacto das Melhorias**:
   - Redução significativa no tempo médio de resposta em todas as filas
   - Aumento no throughput do sistema
   - Redução no número de clientes perdidos
   - Melhor utilização dos recursos

2. **Custos vs. Benefícios**:
   - Aumento no número de servidores: +XX servidores
   - Aumento na capacidade das filas: +XX posições
   - Melhoria no tempo de atendimento: -XX% no tempo total

3. **Recomendações Adicionais**:
   - Implementar sistema de priorização de pacientes
   - Considerar horários de pico para dimensionamento
   - Avaliar a possibilidade de telemedicina para consultas não urgentes

---

## Referências

1. Notação de Kendall para sistemas de filas
2. Teoria de filas e simulação de sistemas
3. Análise de desempenho de sistemas hospitalares 