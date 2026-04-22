const mongoose = require('mongoose');

function validateCNPJ(cnpj) {
  cnpj = cnpj.replace(/[\.\-\/]/g, '');

  if (cnpj.length !== 14 || /^(\\d)\1+$/.test(cnpj)) {
    return false;
  }

  let t = cnpj.length - 2, d = cnpj.substring(t), d1 = parseInt(d.charAt(0)), d2 = parseInt(d.charAt(1));
  let calc = x => cnpj.substring(0, x).split('').reduce((s, e, i) => s + e * ((x + 1) - i), 0) % 11;
  let v1 = calc(t), v2 = calc(t + 1);
  v1 = v1 < 2 ? 0 : 11 - v1; v2 = v2 < 2 ? 0 : 11 - v2;

  return v1 === d1 && v2 === d2;
}

const empresaSchema = new mongoose.Schema({
  nome: { type: String, required: true },
  razaoSocial: { type: String, required: true },
  cnpj: {
    type: String,
    required: true,
    unique: true,
    validate: {
      validator: validateCNPJ,
      message: 'CNPJ inválido',
    },
  },
  regimeTributario: {
    type: String,
    enum: ['Simples Nacional', 'Lucro Presumido', 'MEI'],
  },
  receitaBruta: { type: Number, required: true },
  fatorR: { type: Number, default: null },
  status: {
    type: String,
    enum: ['Ativo', 'Inativo'],
    default: 'Ativo',
  },
}, { timestamps: true });

module.exports = mongoose.model('Empresa', empresaSchema);