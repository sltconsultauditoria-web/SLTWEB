import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Bell, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  X,
  Filter,
  Check
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const Alertas = () => {
  const [alertas, setAlertas] = useState([
    { id: 1, tipo: 'vencimento', prioridade: 'critica', titulo: 'DAS próximo do vencimento', descricao: 'O DAS de 01/2025 da empresa TRES PINHEIROS vence em 2 dias', empresa: 'TRES PINHEIROS', tempo: 'Há 2 horas', lido: false, resolvido: false },
    { id: 2, tipo: 'fiscal', prioridade: 'critica', titulo: 'Inconsistência fiscal detectada', descricao: 'NF-e número 12345 apresenta divergência nos valores', empresa: 'SUPER GALO', tempo: 'Há 4 horas', lido: false, resolvido: false },
    { id: 3, tipo: 'vencimento', prioridade: 'alta', titulo: 'Certidão FGTS expirando', descricao: 'A certidão FGTS expira em 15 dias', empresa: 'MAFE REST.', tempo: 'Há 1 dia', lido: true, resolvido: false },
    { id: 4, tipo: 'sistema', prioridade: 'normal', titulo: 'Atualização do sistema', descricao: 'Nova versão do sistema disponível para atualização', empresa: null, tempo: 'Há 2 dias', lido: true, resolvido: false },
    { id: 5, tipo: 'vencimento', prioridade: 'normal', titulo: 'DCTF Web pendente', descricao: 'DCTF Web de 12/2024 pendente de envio', empresa: 'TECH SOLUTIONS', tempo: 'Há 3 dias', lido: false, resolvido: false },
    { id: 6, tipo: 'fiscal', prioridade: 'baixa', titulo: 'Atualização cadastral', descricao: 'Dados cadastrais desatualizados', empresa: 'DIGI MEI', tempo: 'Há 5 dias', lido: true, resolvido: true },
  ]);

  const getPrioridadeConfig = (prioridade) => {
    const configs = {
      'critica': { color: 'bg-red-500', textColor: 'text-red-700', bgColor: 'bg-red-50', borderColor: 'border-red-200', icon: AlertTriangle, label: 'Crítica' },
      'alta': { color: 'bg-orange-500', textColor: 'text-orange-700', bgColor: 'bg-orange-50', borderColor: 'border-orange-200', icon: AlertTriangle, label: 'Alta' },
      'normal': { color: 'bg-yellow-500', textColor: 'text-yellow-700', bgColor: 'bg-yellow-50', borderColor: 'border-yellow-200', icon: Clock, label: 'Normal' },
      'baixa': { color: 'bg-green-500', textColor: 'text-green-700', bgColor: 'bg-green-50', borderColor: 'border-green-200', icon: CheckCircle, label: 'Baixa' },
    };
    return configs[prioridade] || configs['normal'];
  };

  const getTipoLabel = (tipo) => {
    const labels = {
      'vencimento': '📅 Vencimento',
      'fiscal': '📊 Fiscal',
      'erro_processamento': '⚠️ Erro',
      'sistema': '💻 Sistema'
    };
    return labels[tipo] || tipo;
  };

  const marcarComoLido = (id) => {
    setAlertas(alertas.map(a => a.id === id ? { ...a, lido: true } : a));
  };

  const marcarComoResolvido = (id) => {
    setAlertas(alertas.map(a => a.id === id ? { ...a, resolvido: true, lido: true } : a));
  };

  const alertasNaoLidos = alertas.filter(a => !a.lido && !a.resolvido);
  const alertasPendentes = alertas.filter(a => !a.resolvido);
  const alertasResolvidos = alertas.filter(a => a.resolvido);
  const alertasCriticos = alertas.filter(a => a.prioridade === 'critica' && !a.resolvido);

  const AlertaCard = ({ alerta }) => {
    const config = getPrioridadeConfig(alerta.prioridade);
    const Icon = config.icon;

    return (
      <div 
        className={`p-4 rounded-lg border ${config.borderColor} ${config.bgColor} ${!alerta.lido ? 'ring-2 ring-blue-300' : ''}`}
        data-testid={`alerta-${alerta.id}`}
      >
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-3">
            <div className={`p-2 rounded-full ${config.color}`}>
              <Icon className="h-4 w-4 text-white" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h3 className={`font-semibold ${config.textColor}`}>{alerta.titulo}</h3>
                {!alerta.lido && (
                  <Badge variant="secondary" className="bg-blue-500 text-white text-xs">Novo</Badge>
                )}
              </div>
              <p className="text-sm text-gray-600 mb-2">{alerta.descricao}</p>
              <div className="flex items-center gap-4 text-xs text-gray-500">
                {alerta.empresa && <span className="font-medium">{alerta.empresa}</span>}
                <span>{getTipoLabel(alerta.tipo)}</span>
                <span>{alerta.tempo}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {!alerta.lido && (
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => marcarComoLido(alerta.id)}
                title="Marcar como lido"
              >
                <Check className="h-4 w-4" />
              </Button>
            )}
            {!alerta.resolvido && (
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => marcarComoResolvido(alerta.id)}
                className="text-green-600 border-green-300 hover:bg-green-50"
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Alertas</h1>
          <p className="text-gray-500">Central de notificações e alertas do sistema</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-red-50 border-red-200">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-red-600">Críticos</p>
              <p className="text-2xl font-bold text-red-700">{alertasCriticos.length}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-red-500" />
          </CardContent>
        </Card>
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600">Não Lidos</p>
              <p className="text-2xl font-bold text-blue-700">{alertasNaoLidos.length}</p>
            </div>
            <Bell className="h-8 w-8 text-blue-500" />
          </CardContent>
        </Card>
        <Card className="bg-yellow-50 border-yellow-200">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-yellow-600">Pendentes</p>
              <p className="text-2xl font-bold text-yellow-700">{alertasPendentes.length}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-500" />
          </CardContent>
        </Card>
        <Card className="bg-green-50 border-green-200">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600">Resolvidos</p>
              <p className="text-2xl font-bold text-green-700">{alertasResolvidos.length}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-500" />
          </CardContent>
        </Card>
      </div>

      {/* Alertas List */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            Central de Alertas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="pendentes">
            <TabsList className="mb-4">
              <TabsTrigger value="pendentes">Pendentes ({alertasPendentes.length})</TabsTrigger>
              <TabsTrigger value="nao-lidos">Não Lidos ({alertasNaoLidos.length})</TabsTrigger>
              <TabsTrigger value="resolvidos">Resolvidos ({alertasResolvidos.length})</TabsTrigger>
              <TabsTrigger value="todos">Todos ({alertas.length})</TabsTrigger>
            </TabsList>
            
            <TabsContent value="pendentes" className="space-y-3">
              {alertasPendentes.map(alerta => (
                <AlertaCard key={alerta.id} alerta={alerta} />
              ))}
              {alertasPendentes.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-300" />
                  <p>Nenhum alerta pendente!</p>
                </div>
              )}
            </TabsContent>

            <TabsContent value="nao-lidos" className="space-y-3">
              {alertasNaoLidos.map(alerta => (
                <AlertaCard key={alerta.id} alerta={alerta} />
              ))}
              {alertasNaoLidos.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-300" />
                  <p>Todos os alertas foram lidos!</p>
                </div>
              )}
            </TabsContent>

            <TabsContent value="resolvidos" className="space-y-3">
              {alertasResolvidos.map(alerta => (
                <AlertaCard key={alerta.id} alerta={alerta} />
              ))}
              {alertasResolvidos.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <Clock className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>Nenhum alerta resolvido ainda</p>
                </div>
              )}
            </TabsContent>

            <TabsContent value="todos" className="space-y-3">
              {alertas.map(alerta => (
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
