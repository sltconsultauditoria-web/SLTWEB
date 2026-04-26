const Empresa = require('../models/empresa');
const mongoose = require('mongoose');

exports.createEmpresa = async (req, res) => {
  try {
    console.log("Recebendo payload no backend:", req.body);
    const empresa = new Empresa(req.body);
    await empresa.save();
    console.log("Empresa criada com sucesso:", empresa);
    res.status(201).json({ success: true, message: 'Empresa criada com sucesso', data: empresa });
  } catch (error) {
    console.error("Erro ao criar empresa:", error);
    res.status(400).json({ success: false, message: error.message });
  }
};

exports.getEmpresas = async (req, res) => {
  try {
    const { page = 1, limit = 10, sort = '{}', ...filters } = req.query;
    const sortOptions = JSON.parse(sort);

    const empresas = await Empresa.find(filters)
      .sort(sortOptions)
      .skip((page - 1) * limit)
      .limit(Number(limit));

    const total = await Empresa.countDocuments(filters);

    res.status(200).json({
      success: true,
      data: empresas,
      pagination: {
        total,
        page: Number(page),
        limit: Number(limit),
      },
    });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Erro ao buscar empresas' });
  }
};

exports.getEmpresaById = async (req, res) => {
  try {
    const empresa = await Empresa.findById(req.params.id);
    if (!empresa) {
      return res.status(404).json({ success: false, message: 'Empresa não encontrada' });
    }
    res.status(200).json({ success: true, data: empresa });
  } catch (error) {
    res.status(400).json({ success: false, message: 'ID inválido' });
  }
};

exports.updateEmpresa = async (req, res) => {
  try {
    const empresa = await Empresa.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!empresa) {
      return res.status(404).json({ success: false, message: 'Empresa não encontrada' });
    }
    res.status(200).json({ success: true, message: 'Empresa atualizada com sucesso', data: empresa });
  } catch (error) {
    res.status(400).json({ success: false, message: 'Erro ao atualizar empresa' });
  }
};

exports.deleteEmpresa = async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ success: false, message: 'ID inválido' });
    }

    const empresa = await Empresa.findByIdAndDelete(id);
    if (!empresa) {
      return res.status(404).json({ success: false, message: 'Empresa não encontrada' });
    }
    res.status(200).json({ success: true, message: 'Empresa excluída com sucesso' });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Erro ao excluir empresa' });
  }
};