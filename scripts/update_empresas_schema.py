import re
from pymongo import MongoClient
from datetime import datetime

# Conexão com o MongoDB
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['consultslt_db']

valid_regimes = ['SIMPLES', 'LUCRO_PRESUMIDO', 'LUCRO_REAL', 'MEI']

# 1. Atualizar campos ausentes
for empresa in db.empresas.find():
    update = {}
    if 'created_at' not in empresa:
        update['created_at'] = datetime.utcnow()
    if 'updated_at' not in empresa:
        update['updated_at'] = datetime.utcnow()
    if 'ativo' not in empresa:
        update['ativo'] = True
    if 'receita_bruta' not in empresa:
        update['receita_bruta'] = 0.0
    if 'fator_r' not in empresa:
        update['fator_r'] = 0.0
    if update:
        db.empresas.update_one({'_id': empresa['_id']}, {'$set': update})

# 2. Padronizar CNPJ
for empresa in db.empresas.find():
    cnpj = re.sub(r'\D', '', empresa.get('cnpj', ''))
    if len(cnpj) == 14 and cnpj != empresa.get('cnpj', ''):
        db.empresas.update_one({'_id': empresa['_id']}, {'$set': {'cnpj': cnpj}})

# 3. Atualizar regime tributário
for empresa in db.empresas.find():
    regime = empresa.get('regime', '').upper()
    if regime in valid_regimes and regime != empresa.get('regime', ''):
        db.empresas.update_one({'_id': empresa['_id']}, {'$set': {'regime': regime}})

# 4. Remover empresas inválidas
for empresa in db.empresas.find():
    if len(empresa.get('cnpj', '')) != 14 or empresa.get('regime', '') not in valid_regimes:
        db.empresas.delete_one({'_id': empresa['_id']})

# 5. Criar índice único em cnpj
try:
    db.empresas.create_index('cnpj', unique=True)
    print('Índice único em cnpj criado com sucesso!')
except Exception as e:
    print('Erro ao criar índice único:', e)

print('Atualização concluída!')
