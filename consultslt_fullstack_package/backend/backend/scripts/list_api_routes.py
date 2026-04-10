from main_enterprise import app

print("\n🌐 ROTAS DA API\n")

routes = []

for route in app.routes:
    if hasattr(route, "methods"):
        methods = ",".join(route.methods)
        path = route.path
        routes.append((methods, path))

for m, p in routes:
    print(f"{m:10} {p}")

print("\nTotal:", len(routes))