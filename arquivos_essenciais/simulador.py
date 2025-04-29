import random
import yaml
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

@dataclass
class Cliente:
    """
    Classe que representa um cliente no sistema.
    id: identificador único do cliente
    tempo_chegada: momento em que o cliente chegou à fila atual
    fila_atual: nome da fila onde o cliente está
    proxima_fila: nome da próxima fila para onde o cliente será direcionado (se houver)
    """
    id: int
    tempo_chegada: float
    fila_atual: str
    proxima_fila: Optional[str] = None

class GeradorAleatorio:
    """
    Implementação do gerador linear congruente para geração de números pseudo-aleatórios.
    Este gerador é usado para simular tempos de chegada e serviço.
    """
    def __init__(self, seed=1, a=1664525, c=1013904223, M=2**32):
        self.anterior = seed
        self.a = a
        self.c = c
        self.M = M
    
    def ProximoAleatorio(self):
        """
        Gera o próximo número pseudo-aleatório usando o método linear congruente.
        Retorna um número entre 0 e 1.
        """
        self.anterior = (self.a * self.anterior + self.c) % self.M
        return self.anterior / self.M if self.M != 0 else 0

class Fila:
    """
    Classe que representa uma fila no sistema.
    Gerencia o estado da fila, incluindo servidores, clientes em espera e estatísticas.
    """
    def __init__(self, nome: str, config: dict):
        self.nome = nome
        self.tipo = config['type']
        # Extrai o número de servidores do tipo da fila (ex: G/G/2/5 -> 2 servidores)
        partes_tipo = self.tipo.split('/')
        self.num_servidores = int(partes_tipo[2]) if len(partes_tipo) > 2 else 1
        # Extrai a capacidade da fila (ex: G/G/2/5 -> capacidade 5)
        self.capacidade = int(partes_tipo[3]) if len(partes_tipo) > 3 else float('inf')
        
        # Configuração dos tempos de chegada e serviço
        self.tempo_chegada_min = config.get('arrival', {}).get('min', 0)
        self.tempo_chegada_max = config.get('arrival', {}).get('max', 0)
        self.tempo_servico_min = config['service']['min']
        self.tempo_servico_max = config['service']['max']
        
        # Configuração do roteamento (para qual fila os clientes irão após o serviço)
        self.roteamento = config.get('routing', [])
        
        # Estado da fila
        self.fila: List[Cliente] = []  # Lista de clientes em espera
        self.servidores: List[Tuple[Optional[Cliente], float]] = [(None, 0)] * self.num_servidores
        self.clientes_perdidos = 0
        self.tempo_em_estado = defaultdict(float)  # Tempo acumulado em cada estado
        self.ultimo_tempo_evento = 0
        self.gerador = GeradorAleatorio()
        
        # Estatísticas adicionais
        self.tempo_total_espera = 0
        self.numero_clientes_processados = 0
        self.tempo_total_servico = 0

    def gerar_tempo_servico(self) -> float:
        """
        Gera um tempo de serviço aleatório entre o mínimo e máximo configurados.
        """
        return self.tempo_servico_min + (self.tempo_servico_max - self.tempo_servico_min) * self.gerador.ProximoAleatorio()

    def gerar_tempo_chegada(self, tempo_atual: float) -> float:
        """
        Gera o próximo tempo de chegada.
        Se a fila não tem chegadas próprias (min=max=0), retorna infinito.
        """
        if self.tempo_chegada_min == 0 and self.tempo_chegada_max == 0:
            return float('inf')
        return tempo_atual + self.tempo_chegada_min + (self.tempo_chegada_max - self.tempo_chegada_min) * self.gerador.ProximoAleatorio()

    def obter_proxima_fila(self) -> Optional[str]:
        """
        Determina para qual fila o cliente será direcionado após o serviço.
        Usa as probabilidades de roteamento definidas na configuração.
        """
        if not self.roteamento:
            return None
            
        # Gera um número aleatório para determinar a próxima fila
        aleatorio = self.gerador.ProximoAleatorio()
        probabilidade_acumulada = 0
        
        for rota in self.roteamento:
            for proxima_fila, probabilidade in rota.items():
                probabilidade_acumulada += probabilidade
                if aleatorio <= probabilidade_acumulada:
                    return proxima_fila
                    
        # Se não encontrou uma fila (não deveria acontecer se as probabilidades somam 1)
        return None

class SimuladorRede:
    """
    Classe principal que gerencia a simulação da rede de filas.
    Coordena o fluxo de clientes entre as filas e coleta estatísticas.
    """
    def __init__(self, arquivo_config: str, num_eventos: int = 100000):
        # Carrega a configuração da rede do arquivo YAML
        with open(arquivo_config, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.num_eventos = num_eventos
        self.relogio = 0  # Tempo atual da simulação
        self.eventos = []  # Lista de eventos futuros
        self.filas: Dict[str, Fila] = {}
        self.contador_clientes = 0
        
        # Inicializa todas as filas da rede
        for nome_fila, config_fila in self.config['queues'].items():
            self.filas[nome_fila] = Fila(nome_fila, config_fila)
        
        # Agenda as chegadas iniciais para filas que têm taxa de chegada
        for nome_fila, fila in self.filas.items():
            if fila.tempo_chegada_min > 0 or fila.tempo_chegada_max > 0:
                self.agendar_evento("chegada", fila.gerar_tempo_chegada(2.0), nome_fila)

    def agendar_evento(self, tipo_evento: str, tempo: float, nome_fila: str, cliente: Optional[Cliente] = None):
        """
        Agenda um novo evento para ser processado no futuro.
        Os eventos são ordenados por tempo para garantir o processamento na ordem correta.
        """
        self.eventos.append((tempo, tipo_evento, nome_fila, cliente))
        self.eventos.sort()

    def processar_chegada(self, nome_fila: str, cliente: Optional[Cliente] = None):
        """
        Processa a chegada de um cliente em uma fila.
        Se o cliente não for fornecido, cria um novo cliente.
        Se a fila estiver cheia, incrementa o contador de clientes perdidos.
        """
        fila = self.filas[nome_fila]
        
        if cliente is None:
            self.contador_clientes += 1
            cliente = Cliente(
                id=self.contador_clientes,
                tempo_chegada=self.relogio,
                fila_atual=nome_fila,
                proxima_fila=fila.obter_proxima_fila()
            )
        else:
            # Atualiza a fila atual do cliente
            cliente.fila_atual = nome_fila
            # Determina a próxima fila para onde o cliente será direcionado
            cliente.proxima_fila = fila.obter_proxima_fila()

        # Verifica se a fila está cheia
        if len(fila.fila) >= fila.capacidade:
            fila.clientes_perdidos += 1
            return

        # Adiciona o cliente à fila
        fila.fila.append(cliente)
        
        # Agenda a próxima chegada se esta fila tem taxa de chegada
        if fila.tempo_chegada_min > 0 or fila.tempo_chegada_max > 0:
            self.agendar_evento("chegada", fila.gerar_tempo_chegada(self.relogio), nome_fila)

        # Tenta iniciar o serviço para o cliente recém-chegado
        for i in range(fila.num_servidores):
            if fila.servidores[i][0] is None and fila.fila:
                self.iniciar_servico(nome_fila, i)

    def iniciar_servico(self, nome_fila: str, indice_servidor: int):
        """
        Inicia o serviço para um cliente em um servidor específico.
        Agenda o evento de partida para o momento em que o serviço será concluído.
        """
        fila = self.filas[nome_fila]
        if fila.fila:
            cliente = fila.fila.pop(0)
            tempo_servico = fila.gerar_tempo_servico()
            
            # Atualiza estatísticas
            tempo_espera = self.relogio - cliente.tempo_chegada
            fila.tempo_total_espera += tempo_espera
            fila.tempo_total_servico += tempo_servico
            
            fila.servidores[indice_servidor] = (cliente, self.relogio + tempo_servico)
            self.agendar_evento("partida", self.relogio + tempo_servico, nome_fila, cliente)

    def processar_partida(self, nome_fila: str, cliente: Cliente):
        """
        Processa a partida de um cliente após o serviço.
        Libera o servidor e direciona o cliente para a próxima fila ou para fora do sistema.
        """
        fila = self.filas[nome_fila]
        
        # Atualiza estatísticas
        fila.numero_clientes_processados += 1
        
        # Encontra e libera o servidor
        for i in range(fila.num_servidores):
            if fila.servidores[i][0] and fila.servidores[i][0].id == cliente.id:
                fila.servidores[i] = (None, 0)
                break

        # Direciona para a próxima fila ou para fora do sistema
        if cliente.proxima_fila:
            # Cria uma cópia do cliente para enviar para a próxima fila
            novo_cliente = Cliente(
                id=cliente.id,
                tempo_chegada=self.relogio,
                fila_atual=cliente.proxima_fila,
                proxima_fila=None  # Será definido quando chegar à próxima fila
            )
            self.processar_chegada(cliente.proxima_fila, novo_cliente)
        else:
            pass  # Cliente sai do sistema

        # Tenta iniciar serviço para o próximo cliente
        for i in range(fila.num_servidores):
            if fila.servidores[i][0] is None and fila.fila:
                self.iniciar_servico(nome_fila, i)

    def calcular_metricas(self):
        """
        Calcula as métricas de desempenho para cada fila.
        """
        metricas = {}
        
        for nome_fila, fila in self.filas.items():
            # Tempo total de simulação
            tempo_total = self.relogio
            
            # Probabilidades de estados
            probabilidades = {}
            tempo_total_estados = sum(fila.tempo_em_estado.values())
            for estado, tempo in fila.tempo_em_estado.items():
                probabilidades[estado] = tempo / tempo_total_estados if tempo_total_estados > 0 else 0
            
            # População média
            populacao_media = sum(estado * prob for estado, prob in probabilidades.items())
            
            # Throughput (vazão)
            throughput = fila.numero_clientes_processados / tempo_total if tempo_total > 0 else 0
            
            # Utilização
            tempo_total_servico = fila.tempo_total_servico
            utilizacao = tempo_total_servico / (tempo_total * fila.num_servidores) if tempo_total > 0 else 0
            
            # Tempo médio de resposta
            tempo_medio_resposta = fila.tempo_total_espera / fila.numero_clientes_processados if fila.numero_clientes_processados > 0 else 0
            
            metricas[nome_fila] = {
                'probabilidades': probabilidades,
                'populacao_media': populacao_media,
                'throughput': throughput,
                'utilizacao': utilizacao,
                'tempo_medio_resposta': tempo_medio_resposta,
                'clientes_perdidos': fila.clientes_perdidos
            }
            
        return metricas

    def plotar_resultados(self, metricas):
        """
        Plota os resultados da simulação em gráficos.
        """
        # Configuração para exibir gráficos
        plt.figure(figsize=(15, 10))
        
        # Subplot 1: Utilização das filas
        plt.subplot(2, 2, 1)
        filas = list(metricas.keys())
        utilizacoes = [metricas[fila]['utilizacao'] * 100 for fila in filas]
        plt.bar(filas, utilizacoes)
        plt.title('Utilização das Filas (%)')
        plt.ylabel('Utilização (%)')
        plt.xticks(rotation=45)
        
        # Subplot 2: Throughput das filas
        plt.subplot(2, 2, 2)
        throughputs = [metricas[fila]['throughput'] for fila in filas]
        plt.bar(filas, throughputs)
        plt.title('Throughput das Filas (clientes/minuto)')
        plt.ylabel('Throughput')
        plt.xticks(rotation=45)
        
        # Subplot 3: Tempo médio de resposta
        plt.subplot(2, 2, 3)
        tempos_resposta = [metricas[fila]['tempo_medio_resposta'] for fila in filas]
        plt.bar(filas, tempos_resposta)
        plt.title('Tempo Médio de Resposta (minutos)')
        plt.ylabel('Tempo (minutos)')
        plt.xticks(rotation=45)
        
        # Subplot 4: Clientes perdidos
        plt.subplot(2, 2, 4)
        clientes_perdidos = [metricas[fila]['clientes_perdidos'] for fila in filas]
        plt.bar(filas, clientes_perdidos)
        plt.title('Clientes Perdidos')
        plt.ylabel('Número de Clientes')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('resultados_simulacao.png')
        plt.close()

    def executar(self):
        """
        Executa a simulação até atingir o número de eventos especificado.
        Processa eventos na ordem cronológica e coleta estatísticas.
        """
        print(f"Iniciando simulação da rede com {self.num_eventos} eventos...")
        
        eventos_processados = 0
        while eventos_processados < self.num_eventos and self.eventos:
            self.relogio, tipo_evento, nome_fila, cliente = self.eventos.pop(0)
            
            # Atualiza o tempo em estado para todas as filas
            for fila in self.filas.values():
                tempo_decorrido = self.relogio - fila.ultimo_tempo_evento
                # Conta clientes em serviço + clientes na fila
                num_clientes_na_fila = len(fila.fila)
                num_clientes_em_servico = sum(1 for s in fila.servidores if s[0] is not None)
                estado_atual = num_clientes_na_fila + num_clientes_em_servico
                fila.tempo_em_estado[estado_atual] += tempo_decorrido
                fila.ultimo_tempo_evento = self.relogio

            if tipo_evento == "chegada":
                self.processar_chegada(nome_fila, cliente)
            elif tipo_evento == "partida":
                self.processar_partida(nome_fila, cliente)

            eventos_processados += 1
            if eventos_processados % 10000 == 0:
                print(f"Processados {eventos_processados} eventos. Tempo atual: {self.relogio:.2f}")

        # Calcula e imprime os resultados
        metricas = self.calcular_metricas()
        self.plotar_resultados(metricas)
        
        print("\nResultados da Simulação:")
        print("=" * 50)
        for nome_fila, fila in self.filas.items():
            print(f"\nFila: {nome_fila} ({fila.tipo})")
            print(f"Clientes perdidos: {fila.clientes_perdidos}")
            print(f"População média: {metricas[nome_fila]['populacao_media']:.2f}")
            print(f"Throughput: {metricas[nome_fila]['throughput']:.4f} clientes/minuto")
            print(f"Utilização: {metricas[nome_fila]['utilizacao']*100:.2f}%")
            print(f"Tempo médio de resposta: {metricas[nome_fila]['tempo_medio_resposta']:.2f} minutos")
            print("Distribuição de estados:")
            for estado, prob in sorted(metricas[nome_fila]['probabilidades'].items()):
                print(f"Estado {estado}: {prob*100:.2f}%")
        
        print(f"\nTempo total de simulação: {self.relogio:.2f} minutos")
        
        return metricas

def criar_configuracao_melhorada(arquivo_original, arquivo_melhorado):
    """
    Cria uma configuração melhorada com base na análise dos resultados.
    """
    with open(arquivo_original, 'r') as f:
        config_original = yaml.safe_load(f)
    
    # Cria uma cópia da configuração original
    config_melhorada = config_original.copy()
    
    # Aplica melhorias com base na análise dos gargalos
    # 1. Aumenta o número de servidores na triagem
    config_melhorada['queues']['triagem']['type'] = 'M/M/3/15'  # Aumenta de 2 para 3 servidores e capacidade de 10 para 15
    
    # 2. Aumenta o número de servidores na emergência
    config_melhorada['queues']['emergencia']['type'] = 'M/M/4/10'  # Aumenta de 3 para 4 servidores e capacidade de 8 para 10
    
    # 3. Aumenta o número de servidores na consulta
    config_melhorada['queues']['consulta']['type'] = 'M/M/3/15'  # Aumenta de 2 para 3 servidores e capacidade de 12 para 15
    
    # 4. Aumenta o número de servidores na internação
    config_melhorada['queues']['internacao']['type'] = 'M/M/2/8'  # Aumenta de 1 para 2 servidores e capacidade de 6 para 8
    
    # 5. Aumenta o número de servidores na alta
    config_melhorada['queues']['alta']['type'] = 'M/M/2/25'  # Aumenta de 1 para 2 servidores e capacidade de 20 para 25
    
    # 6. Reduz os tempos de serviço em todas as filas
    config_melhorada['queues']['triagem']['service']['max'] = 6  # Reduz de 8 para 6 minutos
    config_melhorada['queues']['emergencia']['service']['max'] = 35  # Reduz de 45 para 35 minutos
    config_melhorada['queues']['consulta']['service']['max'] = 25  # Reduz de 30 para 25 minutos
    config_melhorada['queues']['internacao']['service']['max'] = 180  # Reduz de 240 para 180 minutos
    config_melhorada['queues']['alta']['service']['max'] = 4  # Reduz de 5 para 4 minutos
    
    # Salva a configuração melhorada
    with open(arquivo_melhorado, 'w') as f:
        yaml.dump(config_melhorada, f, default_flow_style=False)
    
    return config_melhorada

if __name__ == "__main__":
    # Executa a simulação com a configuração original
    print("Executando simulação com configuração original...")
    simulador_original = SimuladorRede("configuracao_rede.yml")
    metricas_original = simulador_original.executar()
    
    # Cria e executa a simulação com a configuração melhorada
    print("\nCriando configuração melhorada...")
    criar_configuracao_melhorada("configuracao_rede.yml", "configuracao_melhorada.yml")
    
    print("\nExecutando simulação com configuração melhorada...")
    simulador_melhorado = SimuladorRede("configuracao_melhorada.yml")
    metricas_melhorado = simulador_melhorado.executar()
    
    # Compara os resultados
    print("\nComparação entre as configurações original e melhorada:")
    print("=" * 50)
    
    for nome_fila in metricas_original.keys():
        print(f"\nFila: {nome_fila}")
        print(f"{'Métrica':<25} {'Original':<15} {'Melhorada':<15} {'Melhoria (%)':<15}")
        print("-" * 70)
        
        # População média
        pop_original = metricas_original[nome_fila]['populacao_media']
        pop_melhorado = metricas_melhorado[nome_fila]['populacao_media']
        melhoria_pop = ((pop_original - pop_melhorado) / pop_original * 100) if pop_original > 0 else 0
        print(f"{'População média':<25} {pop_original:<15.2f} {pop_melhorado:<15.2f} {melhoria_pop:<15.2f}")
        
        # Throughput
        thr_original = metricas_original[nome_fila]['throughput']
        thr_melhorado = metricas_melhorado[nome_fila]['throughput']
        melhoria_thr = ((thr_melhorado - thr_original) / thr_original * 100) if thr_original > 0 else 0
        print(f"{'Throughput':<25} {thr_original:<15.4f} {thr_melhorado:<15.4f} {melhoria_thr:<15.2f}")
        
        # Utilização
        util_original = metricas_original[nome_fila]['utilizacao'] * 100
        util_melhorado = metricas_melhorado[nome_fila]['utilizacao'] * 100
        melhoria_util = util_melhorado - util_original
        print(f"{'Utilização (%)':<25} {util_original:<15.2f} {util_melhorado:<15.2f} {melhoria_util:<15.2f}")
        
        # Tempo médio de resposta
        resp_original = metricas_original[nome_fila]['tempo_medio_resposta']
        resp_melhorado = metricas_melhorado[nome_fila]['tempo_medio_resposta']
        melhoria_resp = ((resp_original - resp_melhorado) / resp_original * 100) if resp_original > 0 else 0
        print(f"{'Tempo médio de resposta':<25} {resp_original:<15.2f} {resp_melhorado:<15.2f} {melhoria_resp:<15.2f}")
        
        # Clientes perdidos
        perd_original = metricas_original[nome_fila]['clientes_perdidos']
        perd_melhorado = metricas_melhorado[nome_fila]['clientes_perdidos']
        melhoria_perd = ((perd_original - perd_melhorado) / perd_original * 100) if perd_original > 0 else 0
        print(f"{'Clientes perdidos':<25} {perd_original:<15} {perd_melhorado:<15} {melhoria_perd:<15.2f}") 