from .repository import create, find_all, find_by_id, update, delete

def criar(data: dict):
    return create(data)

def listar():
    return find_all()

def obter(id: str):
    return find_by_id(id)

def atualizar(id: str, data: dict):
    return update(id, data)

def remover(id: str):
    return delete(id)
