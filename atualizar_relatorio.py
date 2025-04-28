def parse_queue_data(text, queue_name):
    queue_data = {}
    in_queue = False
    for line in text.split('\n'):
        if f"Fila: {queue_name}" in line:
            in_queue = True
            continue
        if in_queue and line.startswith('Fila:'):
            break
        if in_queue and ':' in line and 'Estado' not in line:
            key, value = [x.strip() for x in line.split(':', 1)]
            queue_data[key] = value
    return queue_data

def format_time(minutes):
    days = minutes // (24 * 60)
    remaining_minutes = minutes % (24 * 60)
    hours = remaining_minutes // 60
    minutes = remaining_minutes % 60
    return f"{int(days)} dias, {int(hours)} horas e {int(minutes)} minutos"

def create_report(terminal_output):
    # Extrair dados das filas
    queues = ['triagem', 'emergencia', 'consulta', 'internacao', 'alta']
    original_data = {}
    improved_data = {}
    
    # Separar dados originais e melhorados
    parts = terminal_output.split('[4/5] Executando simulação com configuração melhorada v2...')
    original_part = parts[0]
    improved_part = parts[1]
    
    # Coletar dados
    for queue in queues:
        original_data[queue] = parse_queue_data(original_part, queue)
        improved_data[queue] = parse_queue_data(improved_part, queue)
    
    # Criar relatório
    report = """# RELATÓRIO DE COMPARAÇÃO V2 - ATUALIZADO

## VISÃO GERAL DO SISTEMA

O sistema de emergência hospitalar foi simulado em duas configurações:
1. Configuração Original
2. Configuração Melhorada V2

### Tempo Total de Simulação
- Original: """ + format_time(float(original_part.split('Tempo total de simulação:')[1].split('minutos')[0].strip())) + """
- Melhorado V2: """ + format_time(float(improved_part.split('Tempo total de simulação:')[1].split('minutos')[0].strip())) + """

## ANÁLISE COMPARATIVA POR FILA

"""
    
    for queue in queues:
        orig = original_data[queue]
        impr = improved_data[queue]
        
        report += f"### {queue.title()}\n"
        report += "| Métrica | Original | Melhorado V2 | Variação |\n"
        report += "|---------|-----------|--------------|----------|\n"
        
        metrics = [
            ('População média', 'População média'),
            ('Throughput', 'Throughput'),
            ('Utilização', 'Utilização'),
            ('Tempo médio de resposta', 'Tempo médio de resposta'),
            ('Clientes perdidos', 'Clientes perdidos')
        ]
        
        for metric_key, metric_name in metrics:
            if metric_key in orig and metric_key in impr:
                orig_val = orig[metric_key].split(' ')[0]
                impr_val = impr[metric_key].split(' ')[0]
                
                try:
                    orig_num = float(orig_val)
                    impr_num = float(impr_val)
                    if orig_num != 0:
                        var = ((impr_num - orig_num) / orig_num) * 100
                        var_str = f"{var:+.2f}%"
                    else:
                        var_str = "N/A"
                except:
                    var_str = "N/A"
                
                report += f"| {metric_name} | {orig_val} | {impr_val} | {var_str} |\n"
        
        report += "\n"
    
    report += """## CONCLUSÕES

1. Melhorias Significativas:
   - Redução expressiva no número de clientes perdidos no sistema
   - Diminuição nos tempos médios de resposta
   - Melhor distribuição da utilização dos recursos

2. Pontos de Atenção:
   - A fila de internação ainda apresenta alta utilização
   - Necessidade de monitoramento contínuo do sistema

3. Recomendações:
   - Considerar aumento adicional na capacidade de internação
   - Implementar sistema de monitoramento em tempo real
   - Desenvolver planos de contingência para picos de demanda

## PRÓXIMOS PASSOS

1. Curto Prazo:
   - Implementar as melhorias propostas
   - Estabelecer métricas de acompanhamento
   - Treinar equipe nas novas configurações

2. Médio Prazo:
   - Avaliar necessidade de ajustes adicionais
   - Desenvolver planos de expansão
   - Implementar sistema de gestão de leitos

3. Longo Prazo:
   - Planejamento de expansão física
   - Desenvolvimento de protocolos otimizados
   - Integração com outros setores do hospital"""
    
    return report

# Ler a saída do terminal
with open('saida_terminal.txt', 'r', encoding='utf-8') as f:
    terminal_output = f.read()

# Gerar e salvar o relatório
report_content = create_report(terminal_output)
with open('relatorio_comparacao_v2_atualizado.txt', 'w', encoding='utf-8') as f:
    f.write(report_content) 