// --- Comandos de Migração para a coleção: obrigacoes ---
db.obrigacoes.updateOne(
  { "_id": ObjectId("69a0964b66fd0002169d5d1a") },
  { "$set": {'id': 'VALOR_PADRAO_PARA_ID'} }
); // AVISO: Documento ID 69a0964b66fd0002169d5d1a não tinha os campos: ['id']

// --- Comandos de Migração para a coleção: alertas ---
db.alertas.updateOne(
  { "_id": ObjectId("...") },
  { "$set": {'status': 'VALOR_PADRAO_PARA_STATUS'} }
); // AVISO: Documento ID ... não tinha os campos: ['status']
