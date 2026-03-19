Write-Host "==============================="
Write-Host "  INICIANDO CORREÇÃO BACKEND"
Write-Host "==============================="

# 1️⃣ Corrigir usuario.py (TrocarSenhaRequest)
$usuarioPath = "backend/schemas/usuario.py"

if (Test-Path $usuarioPath) {
    $content = Get-Content $usuarioPath -Raw
    if ($content -notmatch "TrocarSenhaRequest") {
        Add-Content $usuarioPath "`nfrom pydantic import BaseModel`n`nclass TrocarSenhaRequest(BaseModel):`n    senha_atual: str`n    nova_senha: str`n"
        Write-Host "✔ TrocarSenhaRequest criado"
    } else {
        Write-Host "✔ TrocarSenhaRequest já existe"
    }
}

# 2️⃣ Corrigir BaseRepository
$baseRepoPath = "backend/repositories/base.py"

$baseRepoContent = @"
from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
from backend.database import SessionLocal

T = TypeVar("T")


class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self):
        with SessionLocal() as db:
            return db.query(self.model).all()

    def get_by_id(self, id: int):
        with SessionLocal() as db:
            return db.query(self.model).filter(self.model.id == id).first()

    def create(self, obj):
        with SessionLocal() as db:
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

    def delete(self, id: int):
        with SessionLocal() as db:
            instance = db.query(self.model).filter(self.model.id == id).first()
            if instance:
                db.delete(instance)
                db.commit()
            return instance
"@

Set-Content $baseRepoPath $baseRepoContent
Write-Host "✔ BaseRepository corrigido"

# 3️⃣ Corrigir EmpresaRepository
$empresaRepoPath = "backend/repositories/empresa_repository.py"

$empresaRepoContent = @"
from backend.repositories.base import BaseRepository
from backend.models.empresa import Empresa


class EmpresaRepository(BaseRepository[Empresa]):

    def __init__(self):
        super().__init__(Empresa)
"@

Set-Content $empresaRepoPath $empresaRepoContent
Write-Host "✔ EmpresaRepository corrigido"

# 4️⃣ Limpar cache
Get-ChildItem -Path backend -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✔ Cache removido"

Write-Host ""
Write-Host "==============================="
Write-Host "  CORREÇÃO FINALIZADA"
Write-Host "==============================="
Write-Host ""

# 5️⃣ Subir aplicação
$env:PYTHONPATH="."
uvicorn backend.main_enterprise:app --reload
