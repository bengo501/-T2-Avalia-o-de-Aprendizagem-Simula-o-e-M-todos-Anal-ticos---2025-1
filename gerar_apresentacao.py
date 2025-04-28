import os
import subprocess
import platform

def generate_presentation():
    # Verificar se o Pandoc está instalado
    try:
        subprocess.run(['pandoc', '--version'], check=True, capture_output=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Erro: Pandoc não está instalado ou não está no PATH.")
        print("Por favor, instale o Pandoc: https://pandoc.org/installing.html")
        return False
    
    # Verificar se o arquivo Markdown existe
    if not os.path.exists('relatorio_apresentacao.md'):
        print("Erro: Arquivo 'relatorio_apresentacao.md' não encontrado.")
        return False
    
    # Verificar se os arquivos de imagem existem
    required_images = ['diagrama_rede_original.png', 'diagrama_rede_melhorado_v2.png']
    for image in required_images:
        if not os.path.exists(image):
            print(f"Aviso: Imagem '{image}' não encontrada. A apresentação pode ficar incompleta.")
    
    # Comando para gerar a apresentação
    cmd = [
        'pandoc',
        'relatorio_apresentacao.md',
        '-o', 'apresentacao_hospital.pptx',
        '--slide-level=2',
        '--toc',
        '--toc-depth=2',
        '--highlight-style=tango',
        '--variable', 'fontsize=10pt',
        '--variable', 'mainfont="Arial"',
        '--variable', 'monofont="Courier New"',
        '--variable', 'urlcolor=blue',
        '--variable', 'linkcolor=blue',
        '--variable', 'toccolor=blue'
    ]
    
    # Executar o comando
    try:
        subprocess.run(cmd, check=True)
        print("Apresentação gerada com sucesso: apresentacao_hospital.pptx")
        return True
    except subprocess.SubprocessError as e:
        print(f"Erro ao gerar a apresentação: {e}")
        return False

if __name__ == "__main__":
    generate_presentation() 