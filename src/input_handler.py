import os
import re
from urllib.parse import urlparse
from src.extractors import extract_from_url, extract_from_pdf

def identify_input_type(input_data):
    """
    Analisa a entrada e determina se é uma URL, um caminho de arquivo PDF, 
    ou texto puro.
    
    Args:
        input_data (str): A string de entrada fornecida pelo usuário.
        
    Returns:
        str: 'URL', 'PDF', 'TEXT' ou 'UNKNOWN'
    """
    # 1. Verificar se é uma URL válida
    try:
        result = urlparse(input_data)
        if all([result.scheme, result.netloc]):
            return 'URL'
    except:
        pass

    # 2. Verificar se é um caminho de arquivo PDF
    # (No caso de upload via Streamlit, a lógica muda um pouco, mas para caminho local é assim)
    if isinstance(input_data, str) and input_data.lower().endswith('.pdf'):
        if os.path.exists(input_data):
            return 'PDF_FILE'
        # Mesmo que não exista localmente, se tem extensão PDF pode ser tratado como tal
        return 'PDF_PATH'

    # 3. Caso contrário, assumimos que é texto puro para ser lido diretamente
    if len(input_data) > 0:
        return 'TEXT'
        
    return 'UNKNOWN'

def process_input(input_data):
    """
    Função principal que roteia a entrada para o extrator correto.
    """
    input_type = identify_input_type(input_data)
    
    print(f"Tipo de entrada detectado: {input_type}")
    
    if input_type == 'URL':
        return extract_from_url(input_data)
    elif input_type in ['PDF_FILE', 'PDF_PATH']:
        return extract_from_pdf(input_data)
    elif input_type == 'TEXT':
        return input_data # Já é o texto
    else:
        raise ValueError("Tipo de entrada não suportado ou vazio.")
