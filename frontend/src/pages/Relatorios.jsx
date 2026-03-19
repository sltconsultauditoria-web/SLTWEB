import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  FileBarChart, 
  Download, 
  Calendar,
  Building2,
  Receipt,
  TrendingUp,
  FileText,
  PieChart
} from 'lucide-react';

const Relatorios = () => {
  const relatorios = [
    { id: 1, nome: 'Resumo Mensal de Impostos', descricao: 'Consolidação de todos os impostos do mês', icon: Receipt, cor: 'bg-blue-500' },
    { id: 2, nome: 'DAS por Empresa', descricao: 'Detalhamento de DAS por empresa', icon: Building2, cor: 'bg-green-500' },
    { id: 3, nome: 'Obrigações Pendentes', descricao: 'Lista de obrigações a vencer', icon: Calendar, cor: 'bg-yellow-500' },
    { id: 4, nome: 'Faturamento por Período', descricao: 'Análise de faturamento mensal', icon: TrendingUp, cor: 'bg-purple-500' },
    { id: 5, nome: 'Certidões Emitidas', descricao: 'Histórico de certidões', icon: FileText, cor: 'bg-cyan-500' },
    { id: 6, nome: 'Distribuição por Regime', descricao: 'Empresas por regime tributário', icon: PieChart, cor: 'bg-orange-500' },
  ];

  const relatoriosRecentes = [
    { nome: 'Resumo Mensal - Dezembro/2024', data: '15/01/2025', tamanho: '245 KB' },
    { nome: 'DAS por Empresa - 2024', data: '10/01/2025', tamanho: '1.2 MB' },
    { nome: 'Obrigações Pendentes', data: '08/01/2025', tamanho: '89 KB' },
  ];

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
