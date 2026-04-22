const express = require('express');
const router = express.Router();
const Obrigacao = require('../models/Obrigacao');

// Criar obrigação
router.post('/', async (req, res) => {
  try {
    const obrigacao = new Obrigacao(req.body);
    await obrigacao.save();
    res.status(201).json(obrigacao);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Listar obrigações de uma empresa
router.get('/empresa/:empresaId', async (req, res) => {
  try {
    const obrigacoes = await Obrigacao.find({ empresa_id: req.params.empresaId });
    res.json(obrigacoes);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Atualizar obrigação
router.put('/:id', async (req, res) => {
  try {
    const obrigacao = await Obrigacao.findByIdAndUpdate(
      req.params.id, 
      req.body, 
      { new: true }
    );
    res.json(obrigacao);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Deletar obrigação
router.delete('/:id', async (req, res) => {
  try {
    await Obrigacao.findByIdAndDelete(req.params.id);
    res.json({ message: 'Obrigação removida com sucesso' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;