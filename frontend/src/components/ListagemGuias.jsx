import React, { useEffect, useState } from 'react';
import api from '@/services/api';

const ListagemGuias = () => {
  const [guias, setGuias] = useState([]);

  useEffect(() => {
    const fetchGuias = async () => {
      try {
        const response = await api.get('/guias');
        setGuias(Array.isArray(response.data) ? response.data : response.data?.data || []);
      } catch (error) {
        console.error('Erro ao buscar guias:', error);
      }
    };

    fetchGuias();
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold mb-4">Listagem de Guias</h1>
      <div className="overflow-x-auto rounded-lg border bg-white">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Empresa</th>
              <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Tipo</th>
              <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Regime</th>
              <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Competencia</th>
              <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Valor</th>
              <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Vencimento</th>
              <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {guias.map((guia, index) => (
              <tr key={guia.id || guia._id || index} className="hover:bg-gray-50">
                <td className="px-4 py-3">{guia.empresa || '-'}</td>
                <td className="px-4 py-3">{guia.tipo || '-'}</td>
                <td className="px-4 py-3">{guia.regime_tributario || guia.regime || '-'}</td>
                <td className="px-4 py-3">{guia.competencia || '-'}</td>
                <td className="px-4 py-3">
                  R$ {Number(guia.valor || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </td>
                <td className="px-4 py-3">{guia.vencimento || '-'}</td>
                <td className="px-4 py-3">{guia.status || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ListagemGuias;
