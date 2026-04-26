import os
import re

# Define o diretório base do script
# __file__ se refere ao arquivo atual (apply_fix.py)
# os.path.dirname() pega o diretório onde o arquivo está (backend)
base_dir = os.path.dirname(__file__) 

# Caminho para a pasta 'api'
api_dir = os.path.join(base_dir, 'api')

# Lista de arquivos a serem modificados
target_files = [
    os.path.join(api_dir, 'alertas.py'),
    os.path.join(api_dir, 'auditoria.py'),
    os.path.join(api_dir, 'obrigacoes.py'),
]

# Conteúdo do arquivo de utilitários
utils_content = """
from bson import ObjectId
import datetime

def mongo_to_dict(mongo_object):
    \"\"\"
    Converte um único objeto do MongoDB para um dicionário Python limpo e compatível com JSON.
    \"\"\"
    if not mongo_object:
        return None
    
    data = dict(mongo_object)
    
    if '_id' in data and isinstance(data['_id'], ObjectId):
        data['id'] = str(data['_id'])
        del data['_id']

    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            data[key] = value.isoformat()

    return data

def mongo_list_to_dict_list(mongo_list):
    \"\"\"
    Converte uma lista de objetos do MongoDB para uma lista de dicionários limpos.
    \"\"\"
    if not mongo_list:
        return []
    return [mongo_to_dict(item) for item in mongo_list]
"""

# Padrões para modificação dos arquivos da API
import_statement = 'from backend.db.utils import mongo_list_to_dict_list'
# Este padrão busca por 'return await <qualquer_coisa>.to_list(length=None)'
return_pattern = re.compile(r'return await (\w+)\.to_list\(length=None\)')
# Esta é a substituição, que usa o grupo capturado (\1)
replacement_logic = r'    items_list = await \1.to_list(length=None)\n    return mongo_list_to_dict_list(items_list)'

def run_fix():
    """
    Executa todo o processo de correção.
    """
    print('--- Iniciando script de correção automática ---')

    # --- PASSO 1: Criar o arquivo utils.py ---
    db_dir = os.path.join(base_dir, 'db')
    utils_path = os.path.join(db_dir, 'utils.py')

    print(f'\n[PASSO 1] Verificando {utils_path}...')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f'  - Diretório criado: {db_dir}')
    
    with open(utils_path, 'w', encoding='utf-8') as f:
        f.write(utils_content.strip())
    print(f'  - SUCESSO: Arquivo {utils_path} criado/atualizado.')

    # --- PASSO 2: Modificar os arquivos da API ---
    print('\n[PASSO 2] Modificando os arquivos da API...')
    for file_path in target_files:
        print(f'  - Processando: {os.path.basename(file_path)}')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            
            # Adicionar a importação
            if import_statement not in content:
                # Tenta adicionar após o primeiro import
                content = re.sub(r'(from .+ import .+)', r'\1\n' + import_statement, content, 1)

            # Substituir a linha de retorno
            content, num_replacements = return_pattern.subn(replacement_logic, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'    - SUCESSO: Arquivo modificado.')
            else:
                print(f'    - Nenhuma alteração necessária.')

        except FileNotFoundError:
            print(f'    - ERRO: Arquivo não encontrado em {file_path}.')
        except Exception as e:
            print(f'    - ERRO INESPERADO: {e}')

    print('\n--- Script de correção finalizado ---')

# Executa a função principal
if __name__ == "__main__":
    run_fix()
