import { useCallback, useEffect, useMemo, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  ArrowLeft,
  CalendarDays,
  Download,
  Filter,
  RefreshCw,
  Clock3,
  AlertTriangle,
  FileText,
  Bell,
} from 'lucide-react';

const initialFilters = {
  status: '',
  inicio: '',
  fim: '',
};

const severityStyles = {
  critica: 'bg-red-100 text-red-800 border-red-200',
  alta: 'bg-orange-100 text-orange-800 border-orange-200',
  media: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  baixa: 'bg-green-100 text-green-800 border-green-200',
};

const statusStyles = {
  novo: 'bg-blue-100 text-blue-800 border-blue-200',
  processado: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  resolvido: 'bg-gray-100 text-gray-800 border-gray-200',
  pendente: 'bg-amber-100 text-amber-800 border-amber-200',
  erro: 'bg-red-100 text-red-800 border-red-200',
  aberto: 'bg-orange-100 text-orange-800 border-orange-200',
};

const formatDateTime = (value) => {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '-';
  return date.toLocaleString('pt-BR');
};

const TimelineEmpresa = () => {
  const { empresaId } = useParams();
  const [empresa, setEmpresa] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [resumo, setResumo] = useState({});
  const [filters, setFilters] = useState(initialFilters);
  const [loading, setLoading] = useState(true);
  const [exportingPdf, setExportingPdf] = useState(false);
  const [exportingExcel, setExportingExcel] = useState(false);

  const loadTimeline = useCallback(async (nextFilters = initialFilters) => {
    if (!empresaId) return;
    setLoading(true);
    try {
      const params = {};
      if (nextFilters.status) params.status = nextFilters.status;
      if (nextFilters.inicio) params.inicio = nextFilters.inicio;
      if (nextFilters.fim) params.fim = nextFilters.fim;
      const response = await api.get(`/empresas/${empresaId}/timeline`, { params });
      setEmpresa(response.data?.empresa || null);
      setTimeline(Array.isArray(response.data?.timeline) ? response.data.timeline : []);
      setResumo(response.data?.resumo || {});
    } catch (error) {
      setEmpresa(null);
      setTimeline([]);
      setResumo({});
    } finally {
      setLoading(false);
    }
  }, [empresaId]);

  useEffect(() => {
    loadTimeline(initialFilters);
  }, [loadTimeline]);

  const stats = useMemo(() => ({
    total: resumo.total || timeline.length,
    eventos: resumo.eventos || timeline.filter((item) => item.fonte === 'pipeline_events').length,
    alertas: resumo.alertas || timeline.filter((item) => item.fonte === 'alertas').length,
    criticos: resumo.criticos || timeline.filter((item) => item.severidade === 'critica').length,
    altos: resumo.altos || timeline.filter((item) => item.severidade === 'alta').length,
  }), [resumo, timeline]);

  const handleApplyFilters = async (event) => {
    event.preventDefault();
    await loadTimeline(filters);
  };

  const handleExport = async (format) => {
    const setter = format === 'pdf' ? setExportingPdf : setExportingExcel;
    setter(true);
    try {
      const response = await api.get(`/relatorios/export/${format}`, {
        params: {
          empresa_id: empresaId,
          status: filters.status || undefined,
          inicio: filters.inicio || undefined,
          fim: filters.fim || undefined,
        },
        responseType: 'blob',
      });
      const mimeType = format === 'pdf'
        ? 'application/pdf'
        : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      const blob = new Blob([response.data], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `timeline_${empresa?.razao_social || empresa?.nome_fantasia || empresaId}.${format === 'pdf' ? 'pdf' : 'xlsx'}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Erro ao exportar relatorio:', error);
    } finally {
      setter(false);
    }
  };

  const clearFilters = async () => {
    setFilters(initialFilters);
    await loadTimeline(initialFilters);
  };

  const iconForEntry = (entry) => {
    if (entry.fonte === 'alertas') return Bell;
    if (entry.fonte === 'documentos') return FileText;
    if (entry.fonte === 'obrigacoes' || entry.fonte === 'guias') return CalendarDays;
    if (entry.fonte === 'debitos') return AlertTriangle;
    return Clock3;
  };

  const getSummaryLabel = (value) => (value || 0).toLocaleString('pt-BR');

  return (
    <div className="space-y-6" data-testid="timeline-empresa-page">
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-2">
          <Link to="/empresas" className="inline-flex items-center gap-2 text-sm text-blue-700 hover:text-blue-800">
            <ArrowLeft className="h-4 w-4" />
            Voltar para Empresas
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Timeline da empresa
            </h1>
            <p className="text-gray-500">
              {empresa?.razao_social || empresa?.nome_fantasia || empresa?.cnpj || 'Consolidado de eventos fiscais'}
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => loadTimeline(filters)} disabled={loading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Atualizar
          </Button>
          <Button variant="outline" onClick={() => handleExport('pdf')} disabled={exportingPdf}>
            <Download className="h-4 w-4 mr-2" />
            PDF
          </Button>
          <Button variant="outline" onClick={() => handleExport('excel')} disabled={exportingExcel}>
            <Download className="h-4 w-4 mr-2" />
            Excel
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Total</p>
            <p className="text-2xl font-bold">{getSummaryLabel(stats.total)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Eventos</p>
            <p className="text-2xl font-bold">{getSummaryLabel(stats.eventos)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Alertas</p>
            <p className="text-2xl font-bold">{getSummaryLabel(stats.alertas)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Críticos</p>
            <p className="text-2xl font-bold text-red-600">{getSummaryLabel(stats.criticos)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Altos</p>
            <p className="text-2xl font-bold text-orange-600">{getSummaryLabel(stats.altos)}</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filtros
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end" onSubmit={handleApplyFilters}>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Status</label>
              <Select
                value={filters.status || 'all'}
                onValueChange={(value) => setFilters((prev) => ({ ...prev, status: value === 'all' ? '' : value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Todos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos</SelectItem>
                  <SelectItem value="novo">Novo</SelectItem>
                  <SelectItem value="processado">Processado</SelectItem>
                  <SelectItem value="resolvido">Resolvido</SelectItem>
                  <SelectItem value="pendente">Pendente</SelectItem>
                  <SelectItem value="erro">Erro</SelectItem>
                  <SelectItem value="aberto">Aberto</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Início</label>
              <Input
                type="date"
                value={filters.inicio}
                onChange={(e) => setFilters((prev) => ({ ...prev, inicio: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Fim</label>
              <Input
                type="date"
                value={filters.fim}
                onChange={(e) => setFilters((prev) => ({ ...prev, fim: e.target.value }))}
              />
            </div>
            <div className="flex gap-2">
              <Button type="submit" className="flex-1">
                Aplicar
              </Button>
              <Button type="button" variant="outline" onClick={clearFilters}>
                Limpar
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Linha do tempo</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="py-12 text-center text-gray-500">Carregando timeline...</div>
          ) : timeline.length === 0 ? (
            <div className="py-12 text-center text-gray-500">
              Nenhum evento encontrado para os filtros atuais.
            </div>
          ) : (
            <div className="space-y-5">
              {timeline.map((entry) => {
                const Icon = iconForEntry(entry);
                return (
                  <div key={`${entry.fonte}-${entry.id}-${entry.data}`} className="relative pl-6">
                    <span className="absolute left-0 top-2 h-3 w-3 rounded-full bg-blue-600" />
                    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
                      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                        <div className="space-y-2">
                          <div className="flex items-center gap-2">
                            <Icon className="h-4 w-4 text-gray-500" />
                            <h3 className="font-semibold text-gray-900">{entry.titulo}</h3>
                          </div>
                          <p className="text-sm text-gray-600">{entry.descricao || 'Sem descrição'}</p>
                          <p className="text-xs text-gray-500">
                            {formatDateTime(entry.data)} • {entry.fonte}
                          </p>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          <Badge className={severityStyles[entry.severidade] || 'bg-gray-100 text-gray-800'}>
                            {entry.severidade || 'media'}
                          </Badge>
                          <Badge className={statusStyles[entry.status] || 'bg-gray-100 text-gray-800'}>
                            {entry.status || 'novo'}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default TimelineEmpresa;
