import yaml
import os
from graphviz import Digraph

def gerar_diagrama_rede(arquivo_config, arquivo_saida='diagrama_rede'):
    """
    Gera um diagrama da rede de filas usando Graphviz.
    
    Args:
        arquivo_config: Caminho para o arquivo de configuração YAML
        arquivo_saida: Nome do arquivo de saída (sem extensão)
    """
    # Carrega a configuração
    with open(arquivo_config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Cria um novo grafo
    dot = Digraph(comment='Rede de Filas do Hospital', format='png')
    dot.attr(rankdir='LR', size='11,8', dpi='300')
    
    # Configuração do estilo
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # Adiciona os nós (filas)
    for nome_fila, config_fila in config['queues'].items():
        # Extrai informações da notação de Kendall
        tipo = config_fila['type']
        partes_tipo = tipo.split('/')
        num_servidores = partes_tipo[2] if len(partes_tipo) > 2 else '1'
        capacidade = partes_tipo[3] if len(partes_tipo) > 3 else '∞'
        
        # Cria o rótulo do nó
        label = f"{nome_fila.capitalize()}\n{tipo}\n"
        
        # Adiciona informações de tempo de serviço
        tempo_min = config_fila['service']['min']
        tempo_max = config_fila['service']['max']
        label += f"Serviço: {tempo_min}-{tempo_max} min"
        
        # Adiciona o nó ao grafo
        dot.node(nome_fila, label)
    
    # Adiciona as arestas (roteamento)
    for nome_fila, config_fila in config['queues'].items():
        if 'routing' in config_fila and config_fila['routing']:
            for rota in config_fila['routing']:
                for proxima_fila, probabilidade in rota.items():
                    # Formata a probabilidade como porcentagem
                    prob_percent = f"{probabilidade*100:.0f}%"
                    dot.edge(nome_fila, proxima_fila, label=prob_percent)
    
    # Salva o diagrama
    dot.render(arquivo_saida, view=False)
    print(f"Diagrama gerado: {arquivo_saida}.png")

if __name__ == "__main__":
    # Gera o diagrama para a configuração original
    gerar_diagrama_rede("configuracao_rede.yml", "diagrama_rede_original")
    
    # Gera o diagrama para a configuração melhorada
    gerar_diagrama_rede("configuracao_melhorada.yml", "diagrama_rede_melhorado") 