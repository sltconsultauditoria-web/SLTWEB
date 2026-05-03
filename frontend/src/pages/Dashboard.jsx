import { useEffect, useMemo, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  AlertTriangle,
  Building2,
  Calendar,
  CheckCircle,
  Clock,
  FileCheck,
  FileText,
  ScanLine,
  ShieldCheck,
  TrendingUp
} from 'lucide-react';
import { api } from '@/context/AuthContext';

const toArray = (value) => {
  if (Array.isArray(value)) return value;
  if (Array.isArray(value?.data)) return value.data;
  return [];
};

const toNumber = (value) => {
  const number = Number(value);
  return Number.isFinite(number) ? number : 0;
};

const hasValue = (value) => value !== undefined && value !== null && value !== '';

const metricValue = (primary, fallback) => (hasValue(primary) ? toNumber(primary) : fallback);

const formatarNumero = (value) => new Intl.NumberFormat('pt-BR').format(toNumber(value));

const formatarPercentual = (value) => `${toNumber(value).toLocaleString('pt-BR', {
  maximumFractionDigits: 1
})}%`;

const formatarData = (value) => {
  if (!value) return '-';
  const data = value instanceof Date ? value : new Date(value);
  return Number.isNaN(data.getTime()) ? '-' : data.toLocaleDateString('pt-BR');
};

const isStatus = (item, statuses) => {
  const status = String(item?.status || item?.data?.status || '').toLowerCase();
  return statuses.includes(status);
};

const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
  <Card className="hover:shadow-lg transition-shadow" data-testid={`stat-${title.toLowerCase().replace(/\s/g, '-')}`}>
    <CardContent className="p-6">
      <div className="flex items-center justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-3xl font-bold mt-1 text-gray-900">{value}</p>
          {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </CardContent>
  </Card>
);

const EmptyState = ({ text }) => (
  <div className="text-center py-8 text-gray-500">
    <Clock className="h-10 w-10 mx-auto mb-3 text-gray-300" />
    <p className="text-sm">{text}</p>
  </div>
);

const Dashboard = () => {
  const [dashboard, setDashboard] = useState({});
  const [ocrStats, setOcrStats] = useState({});
  const [alertas, setAlertas] = useState([]);
  const [obrigacoes, setObrigacoes] = useState([]);
  const [documentos, setDocumentos] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setErro('');

    try {
      const [dashboardRes, ocrRes, alertasRes, obrigacoesRes, documentosRes, empresasRes] = await Promise.all([
        api.get('/dashboard'),
        api.get('/ocr/estatisticas').catch(() => ({ data: {} })),
        api.get('/alertas'),
        api.get('/obrigacoes'),
        api.get('/documentos'),
        api.get('/empresas')
      ]);

      setDashboard(dashboardRes.data || {});
      setOcrStats(ocrRes.data || {});
      setAlertas(toArray(alertasRes.data));
      setObrigacoes(toArray(obrigacoesRes.data));
      setDocumentos(toArray(documentosRes.data));
      setEmpresas(toArray(empresasRes.data));
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
      setErro('Nao foi possivel carregar os dados do dashboard.');
    } finally {
      setLoading(false);
    }
  };

  const metrics = useMemo(() => {
    const empresasAtivas = metricValue(dashboard.empresas_ativas, empresas.filter((empresa) => empresa.ativo !== false).length);
    const documentosProcessados =
      metricValue(dashboard.documentos_processados, documentos.filter((documento) => isStatus(documento, ['processado', 'concluido', 'sucesso'])).length);
    const documentosOcr = metricValue(dashboard.ocr_processados, toNumber(ocrStats.total));
    const ocrErro =
      metricValue(dashboard.ocr_erros, hasValue(ocrStats.erros) ? toNumber(ocrStats.erros) : toNumber(ocrStats.com_erro));
    const ocrPendentes =
      metricValue(dashboard.ocr_pendentes, hasValue(ocrStats.pendentes) ? toNumber(ocrStats.pendentes) : toNumber(ocrStats.revisao_necessaria));
    const obrigacoesPendentes =
      metricValue(dashboard.obrigacoes_pendentes, obrigacoes.filter((obrigacao) => isStatus(obrigacao, ['pendente'])).length);
    const alertasCriticos =
      metricValue(dashboard.alertas_criticos, alertas.filter((alerta) => String(alerta.prioridade || '').toLowerCase() === 'alta' && !alerta.resolvido).length);

    return {
      empresasAtivas,
      documentosProcessados,
      documentosOcr,
      ocrErro,
      ocrPendentes,
      ocrProcessados: Math.max(documentosOcr - ocrErro - ocrPendentes, 0),
      obrigacoesPendentes,
      alertasCriticos,
      guiasGeradas: metricValue(dashboard.das_gerados_mes, toNumber(dashboard.guias)),
      certidoesEmitidas: metricValue(dashboard.certidoes_emitidas_mes, toNumber(dashboard.certidoes)),
      taxaConformidade: toNumber(dashboard.taxa_conformidade)
    };
  }, [alertas, dashboard, documentos, empresas, obrigacoes, ocrStats]);

  const proximosVencimentos = useMemo(() => {
    const origem = toArray(dashboard.proximos_vencimentos).length ? toArray(dashboard.proximos_vencimentos) : obrigacoes;
    return origem
      .filter((item) => item)
      .sort((a, b) => new Date(a.vencimento || a.data_vencimento || 0) - new Date(b.vencimento || b.data_vencimento || 0))
      .slice(0, 6);
  }, [dashboard.proximos_vencimentos, obrigacoes]);

  const documentosRecentes = useMemo(() => {
    const origem = toArray(dashboard.documentos_recentes).length ? toArray(dashboard.documentos_recentes) : documentos;
    return origem.slice(0, 5);
  }, [dashboard.documentos_recentes, documentos]);

  const getPrioridadeColor = (prioridade) => {
    switch (String(prioridade || '').toLowerCase()) {
      case 'critica':
      case 'alta':
        return 'text-red-600 bg-red-100';
      case 'normal':
        return 'text-yellow-600 bg-yellow-100';
      case 'baixa':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-900"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="dashboard-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500">Visao geral do sistema com dados do MongoDB</p>
      </div>

      {erro && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-4 flex items-center gap-3 text-red-700">
            <AlertTriangle className="h-5 w-5" />
            <span className="text-sm font-medium">{erro}</span>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Empresas Ativas" value={formatarNumero(metrics.empresasAtivas)} icon={Building2} color="bg-blue-500" />
        <StatCard title="Documentos Processados" value={formatarNumero(metrics.documentosProcessados)} icon={FileText} color="bg-green-500" />
        <StatCard title="Documentos OCR" value={formatarNumero(metrics.documentosOcr)} icon={ScanLine} color="bg-indigo-500" />
        <StatCard title="OCR com Erro" value={formatarNumero(metrics.ocrErro)} icon={AlertTriangle} color="bg-red-500" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <StatCard title="Obrigacoes Pendentes" value={formatarNumero(metrics.obrigacoesPendentes)} icon={Clock} color="bg-orange-500" />
        <StatCard title="Alertas Criticos" value={formatarNumero(metrics.alertasCriticos)} icon={AlertTriangle} color="bg-rose-500" />
        <StatCard title="Guias/DAS Gerados" value={formatarNumero(metrics.guiasGeradas)} icon={FileCheck} color="bg-cyan-500" />
        <StatCard title="Certidoes Emitidas" value={formatarNumero(metrics.certidoesEmitidas)} icon={CheckCircle} color="bg-purple-500" />
        <StatCard title="Conformidade Fiscal" value={formatarPercentual(metrics.taxaConformidade)} icon={TrendingUp} color="bg-emerald-500" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard title="OCR Processados" value={formatarNumero(metrics.ocrProcessados)} icon={ShieldCheck} color="bg-emerald-500" subtitle="Concluidos com sucesso" />
        <StatCard title="OCR Pendentes" value={formatarNumero(metrics.ocrPendentes)} icon={Clock} color="bg-yellow-500" subtitle="Recebidos ou em revisao" />
        <StatCard title="Taxa OCR" value={formatarPercentual(dashboard.taxa_ocr_sucesso || ocrStats.taxa_sucesso)} icon={ScanLine} color="bg-blue-500" subtitle="Baseada nos documentos OCR" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Proximos Vencimentos
            </CardTitle>
          </CardHeader>
          <CardContent>
            {proximosVencimentos.length === 0 ? (
              <EmptyState text="Nenhuma obrigacao encontrada." />
            ) : (
              <div className="space-y-3">
                {proximosVencimentos.map((ob, index) => (
                  <div key={ob.id || index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg" data-testid={`obrigacao-${index}`}>
                    <div className="min-w-0">
                      <p className="font-medium text-sm truncate">{ob.empresa || ob.empresa_nome || 'Empresa nao informada'}</p>
                      <p className="text-xs text-gray-500 truncate">{ob.tipo || ob.nome || 'Obrigacao'}</p>
                    </div>
                    <div className="text-right shrink-0 ml-4">
                      <p className="text-sm font-medium">{formatarData(ob.vencimento || ob.data_vencimento)}</p>
                      <span className={`text-xs px-2 py-1 rounded-full ${getPrioridadeColor(ob.prioridade)}`}>
                        {ob.prioridade || 'normal'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Documentos Recentes
            </CardTitle>
          </CardHeader>
          <CardContent>
            {documentosRecentes.length === 0 ? (
              <EmptyState text="Nenhum documento encontrado." />
            ) : (
              <div className="space-y-3">
                {documentosRecentes.map((doc, index) => (
                  <div key={doc.id || index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3 min-w-0">
                      <FileText className="h-5 w-5 text-gray-400 shrink-0" />
                      <div className="min-w-0">
                        <p className="text-sm font-medium truncate">{doc.nome || doc.nome_arquivo || doc.file_name || 'Documento'}</p>
                        <p className="text-xs text-gray-500 truncate">{doc.tipo || doc.content_type || doc.status || 'Sem tipo'}</p>
                      </div>
                    </div>
                    <span className="text-xs text-gray-400 shrink-0 ml-4">{formatarData(doc.created_at || doc.data)}</span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
