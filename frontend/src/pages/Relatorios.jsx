import { useEffect, useState } from 'react';
import { api } from '@/context/AuthContext';
import { AlertCircle, Download, FileBarChart, FileSpreadsheet, Loader2, RefreshCw } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

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
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Relatorios</h1>
          <p className="text-gray-500">Gere e exporte relatorios do sistema</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" onClick={carregarRelatorios} disabled={loading}>
            <RefreshCw className={cn('h-4 w-4 mr-2', loading && 'animate-spin')} />
            Atualizar
          </Button>
          <Button variant="outline" onClick={() => handleExport('pdf')} disabled={Boolean(exporting)}>
            {exporting === 'pdf' ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Download className="h-4 w-4 mr-2" />}
            PDF
          </Button>
          <Button variant="outline" onClick={() => handleExport('excel')} disabled={Boolean(exporting)}>
            {exporting === 'excel' ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <FileSpreadsheet className="h-4 w-4 mr-2" />}
            Excel
          </Button>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}
      {success && (
        <div className="rounded-md border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
          {success}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-5">
            <p className="text-sm text-gray-500">Tipos disponiveis</p>
            <p className="text-3xl font-bold">{relatorios.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-sm text-gray-500">Gerados recentemente</p>
            <p className="text-3xl font-bold">{relatoriosRecentes.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-sm text-gray-500">Exportacoes</p>
            <div className="mt-2 flex gap-2">
              <Badge>PDF</Badge>
              <Badge variant="outline">XLSX</Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {loading ? (
          <Card className="md:col-span-2 lg:col-span-3">
            <CardContent className="flex h-40 items-center justify-center text-gray-500">
              <Loader2 className="h-5 w-5 mr-2 animate-spin" />
              Carregando relatorios
            </CardContent>
          </Card>
        ) : relatorios.length === 0 ? (
          <Card className="md:col-span-2 lg:col-span-3">
            <CardContent className="flex h-40 items-center justify-center text-gray-500">
              Nenhum tipo de relatorio cadastrado
            </CardContent>
          </Card>
        ) : (
          relatorios.map((rel) => (
            <Card key={rel.id} className="hover:shadow-md transition-shadow" data-testid={`relatorio-${rel.id}`}>
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-lg ${rel.cor}`}>
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
              <div className="text-center py-8 text-gray-500">Nenhum relatorio gerado ainda</div>
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
