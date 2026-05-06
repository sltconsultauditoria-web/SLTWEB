import { useEffect, useState } from 'react';
import { api } from '@/context/AuthContext';
import { Download, FileBarChart, FileSpreadsheet, Loader2, RefreshCw } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import PageHeader from '@/components/ui/page-header';
import KPICard from '@/components/ui/kpi-card';
import LoadingState from '@/components/ui/loading-state';
import ErrorState from '@/components/ui/error-state';
import EmptyState from '@/components/ui/empty-state';

const normalizeList = (payload, key) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.[key])) return payload[key];
  return [];
};

const formatarData = (value) => {
  if (!value) return '-';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '-' : date.toLocaleDateString('pt-BR');
};

const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

const Relatorios = () => {
  const [relatorios, setRelatorios] = useState([]);
  const [relatoriosRecentes, setRelatoriosRecentes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const carregarRelatorios = async () => {
    setLoading(true);
    setError(null);
    try {
      const [disponiveis, recentes] = await Promise.all([
        api.get('/tipos_relatorios'),
        api.get('/relatorios'),
      ]);
      const tipos = normalizeList(disponiveis.data, 'tipos_relatorios');
      const gerados = normalizeList(recentes.data, 'relatorios');
      setRelatorios(tipos.map((item, index) => ({
        id: item.id || index,
        nome: item.nome || item.data?.nome || 'Relatorio',
        descricao: item.descricao || item.data?.descricao || 'Relatorio operacional do sistema',
        cor: item.cor || item.data?.cor || 'bg-blue-500',
      })));
      setRelatoriosRecentes(gerados.map((item, index) => ({
        id: item.id || item._id || index,
        nome: item.nome || item.data?.nome || 'Relatorio gerado',
        data: item.data_geracao || item.created_at || item.data?.data_geracao || '',
        tamanho: item.tamanho || item.data?.tamanho || '',
      })));
    } catch (err) {
      setError(err?.response?.data?.detail || 'Erro ao carregar relatorios');
      setRelatorios([]);
      setRelatoriosRecentes([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarRelatorios();
  }, []);

  const handleExport = async (format) => {
    setExporting(format);
    setError(null);
    setSuccess(null);
    try {
      const response = await api.get(`/relatorios/export/${format}`, {
        responseType: 'blob',
      });
      const isPdf = format === 'pdf';
      const mimeType = isPdf
        ? 'application/pdf'
        : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      const blob = new Blob([response.data], { type: mimeType });
      downloadBlob(blob, `relatorios_sltweb.${isPdf ? 'pdf' : 'xlsx'}`);
      setSuccess(`Export ${isPdf ? 'PDF' : 'Excel'} gerado com sucesso`);
    } catch (err) {
      setError(err?.response?.data?.detail || `Erro ao exportar ${format.toUpperCase()}`);
    } finally {
      setExporting(null);
    }
  };

  return (
    <div className="space-y-6" data-testid="relatorios-page">
      <PageHeader
        title="Relatorios"
        description="Gere e exporte relatorios do sistema."
        actions={[
          <Button key="refresh" variant="outline" onClick={carregarRelatorios} disabled={loading}>
            <RefreshCw className={cn('h-4 w-4 mr-2', loading && 'animate-spin')} />
            Atualizar
          </Button>,
          <Button key="pdf" variant="outline" onClick={() => handleExport('pdf')} disabled={Boolean(exporting)}>
            {exporting === 'pdf' ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Download className="h-4 w-4 mr-2" />}
            PDF
          </Button>,
          <Button key="excel" variant="outline" onClick={() => handleExport('excel')} disabled={Boolean(exporting)}>
            {exporting === 'excel' ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <FileSpreadsheet className="h-4 w-4 mr-2" />}
            Excel
          </Button>,
        ]}
      />

      {error && <ErrorState title="Nao foi possivel carregar relatorios" description={error} onRetry={carregarRelatorios} />}
      {success && (
        <div className="rounded-md border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
          {success}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <KPICard title="Tipos disponiveis" value={relatorios.length} tone="blue" />
        <KPICard title="Gerados recentemente" value={relatoriosRecentes.length} tone="emerald" />
        <KPICard title="Exportacoes" value="2" tone="violet" subtitle="PDF e XLSX disponíveis" />
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {loading ? (
          <LoadingState title="Carregando relatorios" className="md:col-span-2 lg:col-span-3" />
        ) : relatorios.length === 0 ? (
          <EmptyState title="Nenhum tipo de relatorio cadastrado" className="md:col-span-2 lg:col-span-3" />
        ) : (
          relatorios.map((rel) => (
            <Card key={rel.id} className="border-slate-200 shadow-sm hover:shadow-md transition-shadow" data-testid={`relatorio-${rel.id}`}>
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className={cn('rounded-xl p-3', rel.cor)}>
                    <FileBarChart className="h-6 w-6 text-white" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <h3 className="font-semibold text-gray-900">{rel.nome}</h3>
                    <p className="text-sm text-gray-500 mt-1">{rel.descricao}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileBarChart className="h-5 w-5" />
            Relatorios Gerados Recentemente
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {relatoriosRecentes.length === 0 ? (
              <div className="text-center py-8 text-slate-500">Nenhum relatorio gerado ainda</div>
            ) : (
              relatoriosRecentes.map((rel) => (
                <div
                  key={rel.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <FileBarChart className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="font-medium text-gray-900">{rel.nome}</p>
                      <p className="text-sm text-gray-500">Gerado em {formatarData(rel.data)} {rel.tamanho ? `- ${rel.tamanho}` : ''}</p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Relatorios;
