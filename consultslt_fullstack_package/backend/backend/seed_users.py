"""
Script de seed de usuários padrão do sistema
"""

import sys
import os
from pathlib import Path
import bcrypt
import logging

# Adicionar backend ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from database import get_db_context, init_db
from models import User
from schemas import PerfilUsuario, PERMISSOES_POR_PERFIL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def seed_users():
    """
    Cria usuários administradores padrão
    """
    try:
        # Inicializar banco (criar tabelas)
        logger.info("🔄 Inicializando banco de dados...")
        init_db()
        
        logger.info("🌱 Iniciando seed de usuários...")
        
        # Usuários obrigatórios conforme especificação
        default_users = [
            {
                "nome": "Administrador Padrão",
                "email": "admin@empresa.com",
                "password": "admin123",
                "perfil": PerfilUsuario.ADMIN,
                "primeiro_login": True  # Forçar troca de senha
            },
            {
                "nome": "William Lucas",
                "email": "william.lucas@sltconsult.com.br",
                "password": "slt@2024",
                "perfil": PerfilUsuario.ADMIN,
                "primeiro_login": False
            },
            {
                "nome": "Super Administrador",
                "email": "admin@consultslt.com.br",
                "password": "Admin@123",
                "perfil": PerfilUsuario.SUPER_ADMIN,
                "primeiro_login": False
            }
        ]
        
        with get_db_context() as db:
            for user_data in default_users:
                # Verificar se já existe
                existing = db.query(User).filter(User.email == user_data["email"]).first()
                
                if existing:
                    logger.info(f"✅ Usuário já existe: {user_data['email']}")
                    continue
                
                # Hash da senha
                hashed_password = bcrypt.hashpw(
                    user_data["password"].encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # Permissões baseadas no perfil
                permissoes = PERMISSOES_POR_PERFIL.get(user_data["perfil"], [])
                
                # Criar usuário
                novo_usuario = User(
                    nome=user_data["nome"],
                    email=user_data["email"],
                    password=hashed_password,
                    perfil=user_data["perfil"].value,
                    permissoes=permissoes,
                    ativo=True,
                    primeiro_login=user_data["primeiro_login"]
                )
                
                db.add(novo_usuario)
                db.commit()
                
                logger.info(f"✅ Usuário criado: {user_data['email']} (perfil: {user_data['perfil'].value})")
        
        logger.info("✅ Seed de usuários concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao executar seed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    seed_users()
