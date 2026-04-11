import React, { useState, useEffect } from 'react';

export default function EmpresaForm({ empresa, onSave }) {
  const [form, setForm] = useState({
    nome: '', cnpj: '', regime: '', receita_bruta: '', fator_r: '', status: 'Ativo'
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    if (empresa) setForm(empresa);
  }, [empresa]);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const validateForm = () => {
    if (!form.nome || !form.cnpj || !form.regime || !form.receita_bruta) {
      setError('Todos os campos obrigatórios devem ser preenchidos.');
      return false;
    }
    setError(null);
    return true;
  };

  const handleSubmit = e => {
    e.preventDefault();
    if (validateForm()) {
      onSave(form);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input name="nome" value={form.nome} onChange={handleChange} placeholder="Nome" required />
      <input name="cnpj" value={form.cnpj} onChange={handleChange} placeholder="CNPJ" required />
      <input name="regime" value={form.regime} onChange={handleChange} placeholder="Regime" required />
      <input name="receita_bruta" type="number" value={form.receita_bruta} onChange={handleChange} placeholder="Receita Bruta" required />
      <input name="fator_r" type="number" value={form.fator_r} onChange={handleChange} placeholder="Fator R" />
      <select name="status" value={form.status} onChange={handleChange}>
        <option value="Ativo">Ativo</option>
        <option value="Inativo">Inativo</option>
      </select>
      <button type="submit">Salvar</button>
    </form>
  );
}
