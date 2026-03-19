"""
Script para corrigir automaticamente repositories que usam
collection = get_collection("nome")

Converte para padrão BaseRepository + property collection
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR / "repositories"


def extract_collection_name(content: str):
    """
    Extrai o nome da collection de:
    collection = get_collection("nome")
    """
    match = re.search(r'collection\s*=\s*get_collection\(["\'](.+?)["\']\)', content)
    if match:
        return match.group(1)
    return None


def fix_repository(file_path: Path):
    content = file_path.read_text(encoding="utf-8")

    if "get_collection(" not in content:
        return False

    collection_name = extract_collection_name(content)
    if not collection_name:
        return False

    print(f"🔧 Corrigindo: {file_path.name} → collection '{collection_name}'")

    # Remove linha collection = get_collection(...)
    content = re.sub(
        r'collection\s*=\s*get_collection\(["\'](.+?)["\']\)\n',
        '',
        content
    )

    # Remove import get_collection se existir
    content = re.sub(
        r'from\s+backend\.core\.database\s+import\s+get_collection\n',
        '',
        content
    )

    # Garantir import BaseRepository
    if "BaseRepository" not in content:
        content = "from backend.repositories.base import BaseRepository\n\n" + content

    # Criar nova classe padrão
    class_name = file_path.stem.replace("_repository", "").capitalize() + "Repository"

    new_class = f'''
from datetime import datetime
from bson import ObjectId


class {class_name}(BaseRepository):

    @property
    def collection(self):
        return self.db.{collection_name}
'''

    # Substitui tudo pelo novo template + mantém métodos antigos (se houver)
    methods = re.split(r'class\s+\w+', content, maxsplit=1)
    if len(methods) > 1:
        remaining = methods[1]
        content = new_class + remaining
    else:
        content = new_class

    file_path.write_text(content, encoding="utf-8")
    return True


def main():
    print("🚀 Iniciando correção automática dos repositories...\n")

    fixed = 0

    for file in REPO_DIR.glob("*_repository.py"):
        if fix_repository(file):
            fixed += 1

    print(f"\n✅ Correção finalizada. {fixed} arquivos ajustados.")


if __name__ == "__main__":
    main()
