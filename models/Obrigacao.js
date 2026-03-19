const mongoose = require('mongoose');

const ObrigacaoSchema = new mongoose.Schema({
  titulo: { type: String, required: true },
  descricao: { type: String },
  dataVencimento: { type: Date, required: true },
  status: { 
    type: String, 
    enum: ['pendente', 'concluída', 'atrasada'], 
    default: 'pendente' 
  },
  empresa_id: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'Empresa', 
    required: true 
  },
  criadoEm: { type: Date, default: Date.now },
  atualizadoEm: { type: Date, default: Date.now }
});

// Criar índice para consultas rápidas por empresa
ObrigacaoSchema.index({ empresa_id: 1 });

module.exports = mongoose.model('Obrigacao', ObrigacaoSchema);