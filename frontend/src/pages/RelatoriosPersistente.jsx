import { useState, useEffect } from 'react';
import api from '@/services/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileBarChart, Download } from 'lucide-react';

const formatarData = (value) => {
  if (!value) return '-';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '-' : date.toLocaleDateString('pt-BR');
};

const Relatorios = () => {
  const [relatorios, setRelatorios] = useState([]);
  const [loading, setLoading] = useState(false);

  // Buscar relatórios da API
  const fetchRelatorios = async () => {
    setLoading(true);
    try {
      const res = await api.get('/relatorios');
      setRelatorios(Array.isArray(res.data) ? res.data : res.data?.relatorios || []);
    } catch (err) {
      setRelatorios([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRelatorios();
  }, []);

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
                        Gerado em {formatarData(rel.created_at)}
                        {rel.tamanho ? ` • ${rel.tamanho}` : ''}
                      </p>
                    </div>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => window.open(`/api/relatorios/${rel.id}/download`, '_blank')}>
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
