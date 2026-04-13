import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileBarChart, Download } from 'lucide-react';

const Relatorios = () => {
  const [relatorios, setRelatorios] = useState(API.get('/replace_with_real_endpoint'));
  const [loading, setLoading] = useState(false);
  const API = process.env.REACT_APP_BACKEND_URL ? `${process.env.REACT_APP_BACKEND_URL}/api` : '/api';

  // Buscar relatórios da API
  const fetchRelatorios = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/relatorios/`);
      setRelatorios(res.data.relatorios || API.get('/replace_with_real_endpoint'));
    } catch (err) {
      setRelatorios(API.get('/replace_with_real_endpoint'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRelatorios();
  }, API.get('/replace_with_real_endpoint'));

  return (
    <div className="space-y-6" data-testid="relatorios-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Relatórios</h1>
        <p className="text-gray-500">Gere e exporte relatórios do sistema</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileBarChart className="h-5 w-5" />
            Relatórios Gerados
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8 text-gray-500">Carregando relatórios...</div>
          ) : relatorios.length === 0 ? (
            <div className="text-center py-8 text-gray-500">Nenhum relatório gerado ainda</div>
          ) : (
            <div className="space-y-3">
              {relatorios.map((rel, index) => (
                <div
                  key={rel.id || rel._id || index}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <FileBarChart className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="font-medium text-gray-900">{rel.nome || rel.tipo || 'Relatório'}</p>
                      <p className="text-sm text-gray-500">
                        Gerado em {rel.created_at ? new Date(rel.created_at).toLocaleDateString('pt-BR') : '-'}
                        {rel.tamanho ? ` • ${rel.tamanho}` : ''}
                      </p>
                    </div>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => window.open(`${API}/relatorios/${rel.id}/download`, '_blank')}>
                    <Download className="h-4 w-4 mr-2" />
                    Download
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Relatorios;
