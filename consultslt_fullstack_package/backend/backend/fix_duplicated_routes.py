import ast
import re
import sys

class RouteFixer(ast.NodeTransformer):
    def __init__(self, router_prefix):
        self.router_prefix = router_prefix.strip("/")
        # Extract the last segment of the prefix as the base resource name (e.g., 'alertas' from 'api/alertas')
        self.base_resource_name = self.router_prefix.split("/")[-1]

    def visit_Call(self, node):
        # Check for FastAPI route decorators like @router.get, @router.post, etc.
        if isinstance(node.func, ast.Attribute) and \
           isinstance(node.func.value, ast.Name) and \
           node.func.value.id == 'router' and \
           node.func.attr in ['get', 'post', 'put', 'delete', 'patch']:

            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                original_path = node.args[0].value
                
                # Normalize original_path for comparison (remove leading/trailing slashes)
                normalized_original_path = original_path.strip("/")

                # Check for duplication pattern: e.g., router_prefix = /api/alertas, original_path = /alertas/
                # The internal path starts with the same name as the last segment of the router prefix
                # or a singular/plural variation of it.
                
                # Heuristic: Check if the normalized path starts with the base_resource_name
                # or its singular form (by removing 's' if it ends with 's')
                resource_name_singular = self.base_resource_name[:-1] if self.base_resource_name.endswith('s') else self.base_resource_name

                # Check if the path segment immediately after the initial slash matches the base resource name
                # or its singular form, indicating a redundant path segment.
                path_segments = [s for s in normalized_original_path.split('/') if s]

                if path_segments and (path_segments[0] == self.base_resource_name or path_segments[0] == resource_name_singular):
                    # Remove the redundant segment from the path
                    new_path_segments = path_segments[1:]
                    new_path = '/' + '/'.join(new_path_segments)
                    
                    # Ensure the path is not empty, if so, it should be '/'
                    if not new_path or new_path == '//':
                        new_path = '/'

                    print(f"  Rota original: {original_path}")
                    print(f"  Sugestão de correção: {new_path}")
                    # Modify the AST node to reflect the new path
                    node.args[0].value = new_path
                    # For Python < 3.8 compatibility, also update node.args[0].s
                    if hasattr(node.args[0], 's'):
                        node.args[0].s = new_path
        return self.generic_visit(node)

def fix_routes_in_file(file_path):
    print(f"Analisando e corrigindo rotas em: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tree = ast.parse(content)
    router_prefix = ""

    # First pass: find the APIRouter prefix
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and \
           isinstance(node.func, ast.Name) and \
           node.func.id == 'APIRouter':
            for keyword in node.keywords:
                if keyword.arg == 'prefix' and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                    router_prefix = keyword.value.value
                    print(f"  APIRouter prefix encontrado: {router_prefix}")
                    break
        if router_prefix: # Stop after finding the prefix
            break

    if not router_prefix:
        print("  Nenhum prefixo de APIRouter encontrado. Pulando correção de rotas duplicadas.")
        return

    # Second pass: apply fixes to route paths
    fixer = RouteFixer(router_prefix)
    new_tree = fixer.visit(tree)

    # Generate the corrected code
    corrected_code = ast.unparse(new_tree)

    # Write the corrected code back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(corrected_code)
    print(f"  Correções aplicadas em {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fix_duplicated_routes.py <caminho_do_arquivo_router.py>")
        sys.exit(1)
    
    router_file_path = sys.argv[1]
    fix_routes_in_file(router_file_path)