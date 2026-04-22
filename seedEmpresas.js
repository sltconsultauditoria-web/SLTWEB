const mongoose = require('mongoose');
const Empresa = require('./backend/models/Empresa');

mongoose.connect('mongodb://localhost:27017/consultslt_db', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const empresasSeed = [
  { nome: "TRES PINHEIROS", cnpj: "12.345.678/0001-90", regime: "Simples Nacional", receita_bruta: 1500000, fator_r: 15.5, status: "Ativo" },
  { nome: "SUPER GALO", cnpj: "98.765.432/0001-10", regime: "Simples Nacional", receita_bruta: 2300000, fator_r: 28.2, status: "Ativo" },
  { nome: "MAFE", cnpj: "11.222.333/0001-44", regime: "Simples Nacional", receita_bruta: 890000, fator_r: 22.8, status: "Ativo" },
  { nome: "TECH SOL", cnpj: "55.666.777/0001-88", regime: "Lucro Presumido", receita_bruta: 1600000, status: "Ativo" },
  { nome: "DIGI MEI", cnpj: "99.888.777/0001-66", regime: "MEI", receita_bruta: 81000, status: "Ativo" }
];

async function seed() {
  await Empresa.deleteMany({});
  await Empresa.insertMany(empresasSeed);
  console.log("Seed concluído com sucesso!");
  mongoose.connection.close();
}

seed();