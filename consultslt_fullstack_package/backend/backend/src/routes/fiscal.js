const express = require('express');
const router = express.Router();
const { ObjectId } = require('mongodb');
const db = require('../db'); // Supondo que exista um módulo para conexão com o MongoDB

// Mock para consultas ao e-CAC
router.get('/ecac/certidoes/:cnpj', async (req, res) => {
  const { cnpj } = req.params;
  console.log(`Consulta de certidões para o CNPJ: ${cnpj}`);

  const certidoes = {
    status: 'regular',
    consultadoEm: new Date().toISOString(),
  };

  // Registrar consulta no banco
  await db.collection('fiscal_iris').updateOne(
    { cnpj },
    { $set: { certidoes } },
    { upsert: true }
  );

  res.status(200).json(certidoes);
});

router.get('/ecac/pendencias/:cnpj', async (req, res) => {
  const { cnpj } = req.params;
  console.log(`Consulta de pendências para o CNPJ: ${cnpj}`);

  const pendencias = [
    { descricao: 'DAS em atraso', periodo: '01/2025' },
    { descricao: 'Multa por atraso', periodo: '12/2024' },
  ];

  // Registrar consulta no banco
  await db.collection('fiscal_iris').updateOne(
    { cnpj },
    { $set: { pendencias } },
    { upsert: true }
  );

  res.status(200).json(pendencias);
});

// CRUD do módulo fiscal (IRIS)
router.post('/iris', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('fiscal_iris').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/iris', async (req, res) => {
  try {
    const calculos = await db.collection('fiscal_iris').find({ deletedAt: null }).toArray();
    res.status(200).json(calculos);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/iris/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const calculo = await db.collection('fiscal_iris').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!calculo) {
      return res.status(404).json({ error: 'Cálculo não encontrado' });
    }

    res.status(200).json(calculo);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/iris/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('fiscal_iris').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Cálculo não encontrado' });
    }

    res.status(200).json({ message: 'Cálculo atualizado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Adicionar endpoint para deletar um cálculo fiscal
router.delete('/iris/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('fiscal_iris').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Cálculo não encontrado' });
    }

    res.status(200).json({ message: 'Cálculo deletado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'empresas'

// Criar uma nova empresa
router.post('/empresas', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('empresas').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Listar todas as empresas
router.get('/empresas', async (req, res) => {
  try {
    const empresas = await db.collection('empresas').find({ deletedAt: null }).toArray();
    res.status(200).json(empresas);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Obter uma empresa por ID
router.get('/empresas/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const empresa = await db.collection('empresas').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!empresa) {
      return res.status(404).json({ error: 'Empresa não encontrada' });
    }

    res.status(200).json(empresa);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Atualizar uma empresa
router.put('/empresas/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('empresas').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Empresa não encontrada' });
    }

    res.status(200).json({ message: 'Empresa atualizada com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Deletar uma empresa
router.delete('/empresas/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('empresas').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Empresa não encontrada' });
    }

    res.status(200).json({ message: 'Empresa deletada com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'obrigacoes'
router.post('/obrigacoes', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('obrigacoes').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/obrigacoes', async (req, res) => {
  try {
    const obrigacoes = await db.collection('obrigacoes').find({ deletedAt: null }).toArray();
    res.status(200).json(obrigacoes);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/obrigacoes/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const obrigacao = await db.collection('obrigacoes').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!obrigacao) {
      return res.status(404).json({ error: 'Obrigação não encontrada' });
    }

    res.status(200).json(obrigacao);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/obrigacoes/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('obrigacoes').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Obrigação não encontrada' });
    }

    res.status(200).json({ message: 'Obrigação atualizada com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.delete('/obrigacoes/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('obrigacoes').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Obrigação não encontrada' });
    }

    res.status(200).json({ message: 'Obrigação deletada com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'obrigacoes_empresa'
router.post('/obrigacoes_empresa', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('obrigacoes_empresa').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/obrigacoes_empresa', async (req, res) => {
  try {
    const obrigacoesEmpresa = await db.collection('obrigacoes_empresa').find({ deletedAt: null }).toArray();
    res.status(200).json(obrigacoesEmpresa);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/obrigacoes_empresa/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const obrigacaoEmpresa = await db.collection('obrigacoes_empresa').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!obrigacaoEmpresa) {
      return res.status(404).json({ error: 'Obrigação da empresa não encontrada' });
    }

    res.status(200).json(obrigacaoEmpresa);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/obrigacoes_empresa/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('obrigacoes_empresa').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Obrigação da empresa não encontrada' });
    }

    res.status(200).json({ message: 'Obrigação da empresa atualizada com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.delete('/obrigacoes_empresa/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('obrigacoes_empresa').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Obrigação da empresa não encontrada' });
    }

    res.status(200).json({ message: 'Obrigação da empresa deletada com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'relatorios'
router.post('/relatorios', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('relatorios').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/relatorios', async (req, res) => {
  try {
    const relatorios = await db.collection('relatorios').find({ deletedAt: null }).toArray();
    res.status(200).json(relatorios);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/relatorios/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const relatorio = await db.collection('relatorios').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!relatorio) {
      return res.status(404).json({ error: 'Relatório não encontrado' });
    }

    res.status(200).json(relatorio);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/relatorios/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('relatorios').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Relatório não encontrado' });
    }

    res.status(200).json({ message: 'Relatório atualizado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.delete('/relatorios/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('relatorios').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Relatório não encontrado' });
    }

    res.status(200).json({ message: 'Relatório deletado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'relatorios_gerados'
router.post('/relatorios_gerados', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('relatorios_gerados').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/relatorios_gerados', async (req, res) => {
  try {
    const relatoriosGerados = await db.collection('relatorios_gerados').find({ deletedAt: null }).toArray();
    res.status(200).json(relatoriosGerados);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/relatorios_gerados/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const relatorioGerado = await db.collection('relatorios_gerados').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!relatorioGerado) {
      return res.status(404).json({ error: 'Relatório gerado não encontrado' });
    }

    res.status(200).json(relatorioGerado);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/relatorios_gerados/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('relatorios_gerados').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Relatório gerado não encontrado' });
    }

    res.status(200).json({ message: 'Relatório gerado atualizado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.delete('/relatorios_gerados/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('relatorios_gerados').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Relatório gerado não encontrado' });
    }

    res.status(200).json({ message: 'Relatório gerado deletado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Rota temporária para listar coleções do MongoDB
router.get('/db/collections', async (req, res) => {
  try {
    const collections = await db.listCollections().toArray();
    res.status(200).json(collections.map(c => c.name));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'tipos_documentos'
router.post('/tipos_documentos', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('tipos_documentos').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/tipos_documentos', async (req, res) => {
  try {
    const tiposDocumentos = await db.collection('tipos_documentos').find({ deletedAt: null }).toArray();
    res.status(200).json(tiposDocumentos);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/tipos_documentos/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const tipoDocumento = await db.collection('tipos_documentos').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!tipoDocumento) {
      return res.status(404).json({ error: 'Tipo de documento não encontrado' });
    }

    res.status(200).json(tipoDocumento);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/tipos_documentos/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('tipos_documentos').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Tipo de documento não encontrado' });
    }

    res.status(200).json({ message: 'Tipo de documento atualizado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.delete('/tipos_documentos/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('tipos_documentos').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Tipo de documento não encontrado' });
    }

    res.status(200).json({ message: 'Tipo de documento deletado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'tipos_obrigacoes'
router.post('/tipos_obrigacoes', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('tipos_obrigacoes').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/tipos_obrigacoes', async (req, res) => {
  try {
    const tiposObrigacoes = await db.collection('tipos_obrigacoes').find({ deletedAt: null }).toArray();
    res.status(200).json(tiposObrigacoes);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/tipos_obrigacoes/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const tipoObrigacao = await db.collection('tipos_obrigacoes').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!tipoObrigacao) {
      return res.status(404).json({ error: 'Tipo de obrigação não encontrado' });
    }

    res.status(200).json(tipoObrigacao);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/tipos_obrigacoes/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('tipos_obrigacoes').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Tipo de obrigação não encontrado' });
    }

    res.status(200).json({ message: 'Tipo de obrigação atualizado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.delete('/tipos_obrigacoes/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('tipos_obrigacoes').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Tipo de obrigação não encontrado' });
    }

    res.status(200).json({ message: 'Tipo de obrigação deletado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CRUD para a coleção 'tipos_relatorios'
router.post('/tipos_relatorios', async (req, res) => {
  try {
    const data = req.body;
    data.createdAt = new Date();
    data.updatedAt = new Date();

    const result = await db.collection('tipos_relatorios').insertOne(data);
    res.status(201).json(result.ops[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/tipos_relatorios', async (req, res) => {
  try {
    const tiposRelatorios = await db.collection('tipos_relatorios').find({ deletedAt: null }).toArray();
    res.status(200).json(tiposRelatorios);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/tipos_relatorios/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const tipoRelatorio = await db.collection('tipos_relatorios').findOne({ _id: ObjectId(id), deletedAt: null });

    if (!tipoRelatorio) {
      return res.status(404).json({ error: 'Tipo de relatório não encontrado' });
    }

    res.status(200).json(tipoRelatorio);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.put('/tipos_relatorios/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    data.updatedAt = new Date();

    const result = await db.collection('tipos_relatorios').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: data }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Tipo de relatório não encontrado' });
    }

    res.status(200).json({ message: 'Tipo de relatório atualizado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.delete('/tipos_relatorios/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const result = await db.collection('tipos_relatorios').updateOne(
      { _id: ObjectId(id), deletedAt: null },
      { $set: { deletedAt: new Date() } }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ error: 'Tipo de relatório não encontrado' });
    }

    res.status(200).json({ message: 'Tipo de relatório deletado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;