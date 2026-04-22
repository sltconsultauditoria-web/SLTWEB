from backend.main_enterprise import app

print("\n=== ROTAS REGISTRADAS NO FASTAPI ===\n")

routes = []

for route in app.routes:
    methods = getattr(route, "methods", [])
    path = getattr(route, "path", "")

    if methods and path:
        for method in methods:
            if method not in ["HEAD", "OPTIONS"]:
                routes.append((method, path))

# ordenar
routes = sorted(routes, key=lambda x: x[1])

for method, path in routes:
    print(f"{method:6} {path}")

print("\n=== CHECK LOGIN ===\n")

found = any(path == "/api/auth/login" and method == "POST" for method, path in routes)

if found:
    print("✅ Rota /api/auth/login EXISTE")
else:
    print("❌ Rota /api/auth/login NÃO EXISTE")