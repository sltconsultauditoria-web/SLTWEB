import subprocess
import os
import sys

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python master_fix_script.py <caminho_base_do_backend>")
        sys.exit(1)

    backend_base_path = sys.argv[1]

    print("\n--- Encontrando arquivos de router ---")
    find_command = ["python3", "find_router_files.py", backend_base_path]
    router_files_output = run_command(find_command)

    if router_files_output:
        router_files = router_files_output.strip().split("\n")
        print(f"Encontrados {len(router_files)} arquivos de router.")
        
        print("\n--- Aplicando correção de rotas duplicadas ---")
        for router_file in router_files:
            if router_file:
                print(f"Processando arquivo: {router_file}")
                fix_command = ["python3", "fix_duplicated_routes.py", router_file]
                run_command(fix_command)
    else:
        print("Nenhum arquivo de router encontrado para processar.")

    print("\n--- Processo de correção de rotas duplicadas concluído ---")