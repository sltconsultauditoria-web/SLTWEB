import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Bell,
  AlertTriangle,
  CheckCircle,
  Clock,
  Check,
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  countCriticalAlertas,
  isResolvedAlert,
  isUnreadAlert,
} from '@/lib/alertas';
import { useNotifications } from '@/hooks/useNotifications';
import PageHeader from '@/components/ui/page-header';
import KPICard from '@/components/ui/kpi-card';
import EmptyState from '@/components/ui/empty-state';
import StatusBadge from '@/components/ui/status-badge';

const Alertas = () => {
  const { alertas, markAlertAsRead, markAlertAsResolved } = useNotifications();

  const getPrioridadeConfig = (prioridade) => {
    const configs = {
      critica: { color: 'bg-red-500', textColor: 'text-red-700', bgColor: 'bg-red-50', borderColor: 'border-red-200', icon: AlertTriangle, label: 'Crítica' },
      alta: { color: 'bg-orange-500', textColor: 'text-orange-700', bgColor: 'bg-orange-50', borderColor: 'border-orange-200', icon: AlertTriangle, label: 'Alta' },
      normal: { color: 'bg-yellow-500', textColor: 'text-yellow-700', bgColor: 'bg-yellow-50', borderColor: 'border-yellow-200', icon: Clock, label: 'Normal' },
      baixa: { color: 'bg-green-500', textColor: 'text-green-700', bgColor: 'bg-green-50', borderColor: 'border-green-200', icon: CheckCircle, label: 'Baixa' },
    };
    return configs[prioridade] || configs.normal;
  };

  const getTipoLabel = (tipo) => {
    const labels = {
      vencimento: 'Vencimento',
      fiscal: 'Fiscal',
      erro_processamento: 'Erro',
      sistema: 'Sistema',
    };
    return labels[tipo] || tipo;
  };

  const alertasNaoLidos = alertas.filter(isUnreadAlert);
  const alertasPendentes = alertas.filter((a) => !isResolvedAlert(a));
  const alertasResolvidos = alertas.filter(isResolvedAlert);
  const alertasCriticos = countCriticalAlertas(alertas);

  const AlertaCard = ({ alerta }) => {
    const config = getPrioridadeConfig(alerta.prioridade);
    const Icon = config.icon;

    return (
      <div
        className={`rounded-2xl border p-4 shadow-sm ${config.borderColor} ${config.bgColor} ${!alerta.lido ? 'ring-2 ring-blue-300' : ''}`}
        data-testid={`alerta-${alerta.id}`}
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className={`rounded-full p-2 ${config.color}`}>
              <Icon className="h-4 w-4 text-white" />
            </div>
            <div className="min-w-0">
              <div className="mb-1 flex flex-wrap items-center gap-2">
                <h3 className={`font-semibold ${config.textColor}`}>{alerta.titulo}</h3>
                {!alerta.lido && <StatusBadge status="processing" label="Novo" />}
              </div>
              <p className="mb-2 text-sm text-slate-600">{alerta.descricao}</p>
              <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
                {alerta.empresa && <span className="font-medium">{alerta.empresa}</span>}
                <Badge variant="outline">{getTipoLabel(alerta.tipo)}</Badge>
                <span>{alerta.tempo}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {!alerta.lido && (
              <Button variant="ghost" size="sm" onClick={() => markAlertAsRead(alerta.id)} title="Marcar como lido">
                <Check className="h-4 w-4" />
              </Button>
            )}
            {!alerta.resolvido && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => markAlertAsResolved(alerta.id)}
                className="border-emerald-300 text-emerald-700 hover:bg-emerald-50"
              >
                Resolver
              </Button>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6" data-testid="alertas-page">
      <PageHeader title="Alertas" description="Central de notificacoes e alertas do sistema." />

      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <KPICard title="Críticos" value={alertasCriticos} icon={AlertTriangle} tone="rose" />
        <KPICard title="Não lidos" value={alertasNaoLidos.length} icon={Bell} tone="blue" />
        <KPICard title="Pendentes" value={alertasPendentes.length} icon={Clock} tone="amber" />
        <KPICard title="Resolvidos" value={alertasResolvidos.length} icon={CheckCircle} tone="emerald" />
      </div>

      <Card className="border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            Central de Alertas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="pendentes">
            <TabsList className="mb-4 flex flex-wrap">
              <TabsTrigger value="pendentes">Pendentes ({alertasPendentes.length})</TabsTrigger>
              <TabsTrigger value="nao-lidos">Não Lidos ({alertasNaoLidos.length})</TabsTrigger>
              <TabsTrigger value="resolvidos">Resolvidos ({alertasResolvidos.length})</TabsTrigger>
              <TabsTrigger value="todos">Todos ({alertas.length})</TabsTrigger>
            </TabsList>

            <TabsContent value="pendentes" className="space-y-3">
              {alertasPendentes.map((alerta) => (
                <AlertaCard key={alerta.id} alerta={alerta} />
              ))}
              {alertasPendentes.length === 0 && <EmptyState title="Nenhum alerta pendente!" icon={CheckCircle} />}
            </TabsContent>

            <TabsContent value="nao-lidos" className="space-y-3">
              {alertasNaoLidos.map((alerta) => (
                <AlertaCard key={alerta.id} alerta={alerta} />
              ))}
              {alertasNaoLidos.length === 0 && <EmptyState title="Todos os alertas foram lidos!" icon={CheckCircle} />}
            </TabsContent>

            <TabsContent value="resolvidos" className="space-y-3">
              {alertasResolvidos.map((alerta) => (
                <AlertaCard key={alerta.id} alerta={alerta} />
              ))}
              {alertasResolvidos.length === 0 && <EmptyState title="Nenhum alerta resolvido ainda" icon={Clock} />}
            </TabsContent>

            <TabsContent value="todos" className="space-y-3">
              {alertas.map((alerta) => (
                <AlertaCard key={alerta.id} alerta={alerta} />
              ))}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default Alertas;
