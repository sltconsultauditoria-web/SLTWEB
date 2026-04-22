import inspect
from main_enterprise import app


def listar_rotas():
    print("\n📋 ROTAS REGISTRADAS NA APLICAÇÃO\n")
    print("-" * 80)

    for route in app.routes:
        if hasattr(route, "methods"):
            methods = ",".join(route.methods)
            path = route.path
            name = route.name

            try:
                source_file = inspect.getsourcefile(route.endpoint)
                source_line = inspect.getsourcelines(route.endpoint)[1]
                source_info = f"{source_file}:{source_line}"
            except Exception:
                source_info = "N/A"

            print(f"🔹 {methods:10} {path}")
            print(f"   ↳ Função: {name}")
            print(f"   ↳ Origem: {source_info}")
            print("-" * 80)


if __name__ == "__main__":
    listar_rotas()
