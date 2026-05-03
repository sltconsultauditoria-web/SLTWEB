import { useEffect, useState } from 'react';
import { api } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  FileBarChart, 
  Download
} from 'lucide-react';

const Relatorios = () => {
  const [relatorios, setRelatorios] = useState([]);
  const [relatoriosRecentes, setRelatoriosRecentes] = useState([]);

  useEffect(() => {
    const carregarRelatorios = async () => {
      try {
        const [disponiveis, recentes] = await Promise.all([
          api.get('/tipos_relatorios/'),
          api.get('/relatorios/'),
        ]);
        const tipos = Array.isArray(disponiveis.data) ? disponiveis.data : [];
        const gerados = Array.isArray(recentes.data) ? recentes.data : [];
        setRelatorios(tipos.map((item, index) => ({
          id: item.id || index,
          nome: item.nome || item.data?.nome || 'Relatorio',
          descricao: item.descricao || item.data?.descricao || '',
          icon: FileBarChart,
          cor: item.cor || item.data?.cor || 'bg-blue-500',
        })));
        setRelatoriosRecentes(gerados.map((item) => ({
          nome: item.nome || item.data?.nome || 'Relatorio gerado',
          data: item.data_geracao || item.data?.data_geracao || '',
          tamanho: item.tamanho || item.data?.tamanho || '',
        })));
      } catch (error) {
        console.error('Erro ao carregar relatorios:', error);
        setRelatorios([]);
        setRelatoriosRecentes([]);
      }
    };
    carregarRelatorios();
  }, []);

  return (
    <div className="space-y-6" data-testid="relatorios-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Relatórios</h1>
        <p className="text-gray-500">Gere e exporte relatórios do sistema</p>
      </div>

      {/* Relatórios Disponíveis */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {relatorios.map((rel) => {
          const Icon = rel.icon;
          return (
            <Card key={rel.id} className="hover:shadow-lg transition-shadow cursor-pointer" data-testid={`relatorio-${rel.id}`}>
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-lg ${rel.cor}`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{rel.nome}</h3>
                    <p className="text-sm text-gray-500 mt-1">{rel.descricao}</p>
                    <Button variant="link" className="p-0 h-auto mt-2 text-blue-600">
                      Gerar Relatório →
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Relatórios Recentes */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileBarChart className="h-5 w-5" />
            Relatórios Gerados Recentemente
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {relatoriosRecentes.map((rel, index) => (
              <div 
                key={index}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <FileBarChart className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">{rel.nome}</p>
                    <p className="text-sm text-gray-500">Gerado em {rel.data} • {rel.tamanho}</p>
                  </div>
                </div>
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Relatorios;
