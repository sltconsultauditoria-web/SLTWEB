import sys
from pathlib import Path

# --- PONTO DE CONFIGURAÇÃO 1 ---
# Adiciona os diretórios 'backend' e a raiz ao path do Python
# para permitir a importação correta dos módulos da sua aplicação.
project_root = Path(__file__).parent.resolve()
backend_path = project_root / 'backend' # Assumindo que seu código está em 'backend'
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_path))
# -----------------------------

try:
    # --- PONTO DE CONFIGURAÇÃO 2 ---
    # Altere 'app_loader' para o nome do seu arquivo principal (sem .py)
    # que contém a linha 'app = FastAPI(...)'.
    # O nome da variável 'app' parece estar correto.
    from app_loader import app
    # -----------------------------

except ImportError as e:
    print(f"ERRO: Não foi possível importar a aplicação FastAPI.")
    print(f"Verifique se o nome do arquivo principal ('app_loader.py') e da variável ('app') estão corretos no script.")
    print(f"Detalhe do erro: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Ocorreu um erro inesperado ao carregar a aplicação: {e}")
    print("Isso pode acontecer se o código da aplicação tiver um erro que impede a importação.")
    sys.exit(1)

def get_all_routes():
    """
    Extrai e organiza todas as rotas da aplicação FastAPI.
    """
    routes_info = []
    for route in app.routes:
        if hasattr(route, "methods"):
            path = route.path
            name = route.name
            methods = ", ".join(route.methods)
            
            routes_info.append({
                "path": path,
                "methods": methods,
                "name": name
            })
            
    return routes_info

def print_routes_table(routes):
    """
    Imprime as rotas em uma tabela bem formatada.
    """
    if not routes:
        print("Nenhuma rota encontrada na aplicação.")
        return

    print("=" * 90)
    print("                    LISTA DE ENDPOINTS DA API                    ")
    print("=" * 90)
    
    # Ordenar rotas pelo path
    sorted_routes = sorted(routes, key=lambda x: x["path"])
    
    # Calcula a largura das colunas para alinhamento
    max_path = max(len(r["path"]) for r in sorted_routes) if sorted_routes else 10
    max_methods = max(len(r["methods"]) for r in sorted_routes) if sorted_routes else 10

    # Cabeçalho da tabela
    print(f"{'MÉTODOS':<{max_methods}} | {'ROTA (PATH)':<{max_path}} | {'NOME DA FUNÇÃO'}")
    print("-" * 90)

    # Linhas da tabela
    for route in sorted_routes:
        print(f"{route['methods']:<{max_methods}} | {route['path']:<{max_path}} | {route['name']}")
        
    print("=" * 90)
    print(f"Total de rotas encontradas: {len(routes)}")
    print("=" * 90)


if __name__ == "__main__":
    all_routes = get_all_routes()
    print_routes_table(all_routes)
