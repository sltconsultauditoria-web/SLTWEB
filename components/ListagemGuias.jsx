import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ListagemGuias = () => {
  const [guias, setGuias] = useState([]);

  useEffect(() => {
    const fetchGuias = async () => {
      try {
        const response = await axios.get('/api/guias');
        setGuias(response.data);
      } catch (error) {
        console.error('Erro ao buscar guias:', error);
      }
    };

    fetchGuias();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Listagem de Guias</h1>
      <table className="table-auto w-full border-collapse border border-gray-300">
        <thead>
          <tr>
            <th className="border border-gray-300 px-4 py-2">Empresa</th>
            <th className="border border-gray-300 px-4 py-2">Tipo</th>
            <th className="border border-gray-300 px-4 py-2">Regime</th>
            <th className="border border-gray-300 px-4 py-2">Competência</th>
            <th className="border border-gray-300 px-4 py-2">Valor</th>
            <th className="border border-gray-300 px-4 py-2">Vencimento</th>
            <th className="border border-gray-300 px-4 py-2">Status</th>
            <th className="border border-gray-300 px-4 py-2">Ações</th>
          </tr>
        </thead>
        <tbody>
          {guias.map((guia) => (
            <tr key={guia._id}>
              <td className="border border-gray-300 px-4 py-2">{guia.empresa}</td>
              <td className="border border-gray-300 px-4 py-2">{guia.tipo}</td>
              <td className="border border-gray-300 px-4 py-2">{guia.regime}</td>
              <td className="border border-gray-300 px-4 py-2">{guia.competencia}</td>
              <td className="border border-gray-300 px-4 py-2">R$ {guia.valor.toFixed(2)}</td>
              <td className="border border-gray-300 px-4 py-2">{guia.vencimento}</td>
              <td className="border border-gray-300 px-4 py-2">{guia.status}</td>
              <td className="border border-gray-300 px-4 py-2">
                <button className="bg-blue-500 text-white px-2 py-1 rounded">Editar</button>
                <button className="bg-red-500 text-white px-2 py-1 rounded ml-2">Excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ListagemGuias;