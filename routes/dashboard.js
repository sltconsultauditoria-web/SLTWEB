const express = require('express');
const router = express.Router();
const Empresa = require('../models/Empresa');
const Obrigacao = require('../models/Obrigacao');
const Documento = require('../models/Documento');
const Alerta = require('../models/Alerta');
const Financeiro = require('../models/Financeiro');
const Log = require('../models/Log');

router.get('/', async (req, res) => {
  try {
    const empresasAtivas = await Empresa.countDocuments({ status: 'ativa' });
    const obrigacoesPendentes = await Obrigacao.countDocuments({ status: 'pendente' });
    const proximasObrigacoes = await Obrigacao.find({
      status: 'pendente',
      dataVencimento: { $lte: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) }
    });
    const certidoesEmitidas = await Documento.countDocuments({ tipo: 'certidao' });
    const alertasCriticos = await Alerta.countDocuments({ nivel: 'crítico', status: 'pendente' });
    const receitasMes = await Financeiro.aggregate([
      { $match: { tipo: 'receita', mes: new Date().getMonth() + 1 } },
      { $group: { _id: null, total: { $sum: "$valor" } } }
    ]);
    const despesasMes = await Financeiro.aggregate([
      { $match: { tipo: 'despesa', mes: new Date().getMonth() + 1 } },
      { $group: { _id: null, total: { $sum: "$valor" } } }
    ]);
    const atividadesRecentes = await Log.find().sort({ createdAt: -1 }).limit(10);

    res.json({
      empresasAtivas,
      obrigacoesPendentes,
      proximasObrigacoes,
      certidoesEmitidas,
      alertasCriticos,
      receitasMes: receitasMes[0]?.total || 0,
      despesasMes: despesasMes[0]?.total || 0,
      atividadesRecentes
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;