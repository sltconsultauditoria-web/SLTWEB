import os
import re

# --- Configuração ---
# Diretório onde estão os arquivos de rotas que precisam de correção.
ROUTERS_DIR = "backend/routers" 
# A declaração de importação exata que está causando o problema.
BAD_IMPORT_STATEMENT = "from database import db"
# A mesma declaração, mas com espaços em branco flexíveis.
BAD_IMPORT_PATTERN = re.compile(r"^\s*from\s+database\s+import\s+db\s*$")
# A linha de importação corrigida, com indentação.
GOOD_IMPORT_STATEMENT = "    from database import db\n"

def get_indentation(line):
    """Calcula a indentação de uma linha."""
    return len(line) - len(line.lstrip(' '))

def fix_circular_imports():
    """
    Analisa os arquivos de rota e move a importação 'from database import db'
    do topo do arquivo para dentro das funções que a utilizam, evitando
    erros de importação circular.
    """
    print(f"🔍 Analisando arquivos em '{ROUTERS_DIR}'...")
    
    # Verifica se o diretório de rotas existe
    if not os.path.isdir(ROUTERS_DIR):
        print(f"❌ Erro: O diretório '{ROUTERS_DIR}' não foi encontrado.")
        print("Certifique-se de executar este script na pasta raiz do seu projeto de backend.")
        return

    # Lista todos os arquivos Python no diretório
    files_to_check = [f for f in os.listdir(ROUTERS_DIR) if f.endswith(".py")]
    
    modified_files_count = 0

    for filename in files_to_check:
        filepath = os.path.join(ROUTERS_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"⚠️  Não foi possível ler o arquivo {filepath}: {e}")
            continue

        new_lines = []
        import_found_at_top = False
        made_changes = False

        # 1. Encontra e comenta a importação no topo do arquivo
        for line in lines:
            if BAD_IMPORT_PATTERN.match(line):
                new_lines.append(f"# {line.lstrip()}") # Comenta a linha original
                import_found_at_top = True
                made_changes = True
            else:
                new_lines.append(line)
        
        # Se a importação problemática não foi encontrada, pula para o próximo arquivo
        if not import_found_at_top:
            continue

        # 2. Adiciona a importação dentro de cada função
        final_lines = []
        for line in new_lines:
            final_lines.append(line)
            # Procura por definições de função (async ou normal)
            if line.strip().startswith("def ") or line.strip().startswith("async def "):
                # Pega a indentação da próxima linha para ser mais preciso
                try:
                    next_line_index = new_lines.index(line) + 1
                    indent_level = get_indentation(new_lines[next_line_index])
                    # Adiciona a importação com a indentação correta
                    final_lines.append(' ' * indent_level + "from database import db\n")
                except IndexError:
                    # Caso a função não tenha corpo, usa a indentação padrão
                    final_lines.append(GOOD_IMPORT_STATEMENT)

        # 3. Salva as alterações no arquivo
        if made_changes:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(final_lines)
                print(f"✅ Arquivo modificado: {filepath}")
                modified_files_count += 1
            except Exception as e:
                print(f"❌ Erro ao salvar o arquivo {filepath}: {e}")

    if modified_files_count > 0:
        print(f"\n🎉 Processo concluído! {modified_files_count} arquivos foram corrigidos.")
        print("O servidor deve reiniciar automaticamente. Verifique o log para confirmar que os erros desapareceram.")
    else:
        print("\n✅ Nenhum arquivo precisou de modificação. Parece que as importações já estão corretas.")

if __name__ == "__main__":
    fix_circular_imports()
