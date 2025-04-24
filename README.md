# -T2-Avalia-o-de-Aprendizagem-Simula-o-e-M-todos-Anal-ticos---2025-1
 T2 | Avaliação de Aprendizagem Simulação e Métodos Analíticos - 2025/1

# Simulação de Sistema de Emergência Hospitalar

Este projeto implementa uma simulação de um sistema de emergência hospitalar utilizando teoria de filas. O modelo representa o fluxo de pacientes através de diferentes estágios do atendimento hospitalar.

## Estrutura do Sistema

O sistema é composto por 5 filas principais:

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

## Como Executar

1. Certifique-se de ter Python 3.7+ instalado
2. Instale as dependências:
   ```bash
   pip install pyyaml
   ```
3. Execute a simulação:
   ```bash
   python simulador.py
   ```

## Análise de Desempenho

A simulação coleta as seguintes métricas para cada fila:
- Probabilidade de estados
- Número de clientes perdidos
- Tempo médio de espera
- Utilização dos servidores
- Throughput (vazão)

## Melhorias Propostas

Após análise inicial, serão propostas melhorias no sistema, incluindo:
- Ajuste no número de servidores
- Modificação nas capacidades das filas
- Otimização das probabilidades de roteamento
- Redução nos tempos de serviço

## Resultados

Os resultados da simulação serão apresentados em:
1. Apresentação em PowerPoint/PDF
2. Vídeo explicativo
3. Arquivos de configuração YAML (antes e depois das melhorias)
4. Planilhas com cálculos dos índices de desempenho
