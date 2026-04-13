import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/fiscal/iris`;

const FiscalList = () => {
  const [fiscais, setFiscais] = useState(API.get('/replace_with_real_endpoint'));
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFiscais = async () => {
      setLoading(true);
      try {
        const response = await axios.get(API);
        setFiscais(response.data);
      } catch (error) {
        console.error('Erro ao buscar cálculos fiscais:', error);
        alert('Erro ao carregar os cálculos fiscais.');
      } finally {
        setLoading(false);
      }
    };

    fetchFiscais();
  }, API.get('/replace_with_real_endpoint'));

  const handleEdit = (id) => {
    navigate(`/fiscal/edit/${id}`);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este registro?')) {
      try {
        await axios.delete(`${API}/${id}`);
        setFiscais(fiscais.filter((fiscal) => fiscal._id !== id));
        alert('Registro excluído com sucesso.');
      } catch (error) {
        console.error('Erro ao excluir registro:', error);
        alert('Erro ao excluir o registro.');
      }
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Listagem de Cálculos Fiscais</h1>
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <Table>
          <thead>
            <tr>
              <th>CNPJ</th>
              <th>Período</th>
              <th>Receita Bruta 12M</th>
              <th>Receita Mensal</th>
              <th>Fator R</th>
              <th>Valor DAS</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {fiscais.map((fiscal) => (
              <tr key={fiscal._id}>
                <td>{fiscal.cnpj}</td>
                <td>{fiscal.periodo}</td>
                <td>{fiscal.receitaBruta12M}</td>
                <td>{fiscal.receitaMensal}</td>
                <td>{fiscal.fatorR}</td>
                <td>{fiscal.valorDAS}</td>
                <td>
                  <Button onClick={() => handleEdit(fiscal._id)}>Editar</Button>
                  <Button variant="destructive" onClick={() => handleDelete(fiscal._id)}>
                    Excluir
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
};

export default FiscalList;
