import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Bot, 
  Play, 
  Square, 
  RefreshCw, 
  CheckCircle, 
  XCircle, 
  Clock, 
  AlertTriangle,
  FileText,
  Folder,
  Calendar,
  Activity,
  Settings,
  CloudOff,
  Cloud,
  Loader2
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Robos = () => {
  const [status, setStatus] = useState(null);
  const [sharepointStatus, setSharepointStatus] = useState(null);
  const [history, setHistory] = useState(API.get('/replace_with_real_endpoint'));
  const [files, setFiles] = useState(API.get('/replace_with_real_endpoint'));
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [statusRes, spStatusRes, historyRes, filesRes] = await Promise.all([
        axios.get(`${API}/robots/ingestion/status`),
        axios.get(`${API}/sharepoint/status`),
        axios.get(`${API}/robots/ingestion/history?limit=10`),
        axios.get(`${API}/robots/ingestion/files?limit=20`)
      ]);
      
      setStatus(statusRes.data);
      setSharepointStatus(spStatusRes.data);
      setHistory(historyRes.data.jobs || API.get('/replace_with_real_endpoint'));
      setFiles(filesRes.data.files || API.get('/replace_with_real_endpoint'));
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, API.get('/replace_with_real_endpoint'));

  useEffect(() => {
    loadData();
    
    // Auto-refresh a cada 30 segundos
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, [loadData]);

  const handleRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const handleStartScheduler = async () => {
    setActionLoading('start');
    try {
      await axios.post(`${API}/robots/ingestion/start`);
      await loadData();
    } catch (error) {
      console.error('Erro ao iniciar scheduler:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleStopScheduler = async () => {
    setActionLoading('stop');
    try {
      await axios.post(`${API}/robots/ingestion/stop`);
      await loadData();
    } catch (error) {
      console.error('Erro ao parar scheduler:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleRunNow = async () => {
    setActionLoading('run');
    try {
      await axios.post(`${API}/robots/ingestion/run-now`);
      // Aguardar um pouco e recarregar
      setTimeout(loadData, 2000);
    } catch (error) {
      console.error('Erro ao executar robô:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleString('pt-BR');
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '-';
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    return `${Math.floor(seconds / 60)}m ${(seconds % 60).toFixed(0)}s`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64" data-testid="robos-loading">
        <Loader2 className="h-12 w-12 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="robos-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Bot className="h-7 w-7" />
            Robôs de Automação
          </h1>
          <p className="text-gray-500">Monitoramento e controle dos robôs de ingestão</p>
        </div>
        <Button 
          variant="outline" 
          onClick={handleRefresh} 
          disabled={refreshing}
          data-testid="refresh-button"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
          Atualizar
        </Button>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Status do Robô */}
        <Card data-testid="robot-status-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Status do Robô</p>
                <div className="flex items-center gap-2 mt-1">
                  {status?.running ? (
                    <>
                      <span className="relative flex h-3 w-3">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                      </span>
                      <span className="text-lg font-bold text-green-600">Executando</span>
                    </>
                  ) : (
                    <>
                      <span className="h-3 w-3 rounded-full bg-gray-400"></span>
                      <span className="text-lg font-bold text-gray-600">Parado</span>
                    </>
                  )}
                </div>
              </div>
              <Activity className={`h-8 w-8 ${status?.running ? 'text-green-500' : 'text-gray-400'}`} />
            </div>
          </CardContent>
        </Card>

        {/* Scheduler */}
        <Card data-testid="scheduler-status-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Agendador</p>
                <div className="flex items-center gap-2 mt-1">
                  {status?.scheduler_active ? (
                    <>
                      <CheckCircle className="h-5 w-5 text-green-500" />
                      <span className="text-lg font-bold text-green-600">Ativo</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="h-5 w-5 text-gray-400" />
                      <span className="text-lg font-bold text-gray-600">Inativo</span>
                    </>
                  )}
                </div>
                {status?.next_run && (
                  <p className="text-xs text-gray-400 mt-1">
                    Próxima: {formatDate(status.next_run)}
                  </p>
                )}
              </div>
              <Clock className={`h-8 w-8 ${status?.scheduler_active ? 'text-green-500' : 'text-gray-400'}`} />
            </div>
          </CardContent>
        </Card>

        {/* SharePoint */}
        <Card data-testid="sharepoint-status-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">SharePoint</p>
                <div className="flex items-center gap-2 mt-1">
                  {sharepointStatus?.configured ? (
                    <>
                      <Cloud className="h-5 w-5 text-blue-500" />
                      <span className="text-lg font-bold text-blue-600">Conectado</span>
                    </>
                  ) : (
                    <>
                      <CloudOff className="h-5 w-5 text-orange-500" />
                      <span className="text-lg font-bold text-orange-600">Não Config.</span>
                    </>
                  )}
                </div>
              </div>
              {sharepointStatus?.configured ? (
                <Cloud className="h-8 w-8 text-blue-500" />
              ) : (
                <CloudOff className="h-8 w-8 text-orange-400" />
              )}
            </div>
          </CardContent>
        </Card>

        {/* Estatísticas */}
        <Card data-testid="stats-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Arquivos</p>
                <p className="text-2xl font-bold text-blue-600 mt-1">
                  {status?.statistics?.total_processed || 0}
                </p>
                <p className="text-xs text-gray-400">
                  {status?.statistics?.total_pending || 0} pendentes
                </p>
              </div>
              <FileText className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Controles */}
      <Card data-testid="controls-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Controles do Robô
          </CardTitle>
          <CardDescription>
            Gerencie a execução do robô de ingestão do SharePoint
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            {status?.scheduler_active ? (
              <Button 
                variant="destructive" 
                onClick={handleStopScheduler}
                disabled={actionLoading === 'stop'}
                data-testid="stop-scheduler-button"
              >
                {actionLoading === 'stop' ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Square className="h-4 w-4 mr-2" />
                )}
                Parar Agendador
              </Button>
            ) : (
              <Button 
                className="bg-green-600 hover:bg-green-700"
                onClick={handleStartScheduler}
                disabled={actionLoading === 'start' || !sharepointStatus?.configured}
                data-testid="start-scheduler-button"
              >
                {actionLoading === 'start' ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Play className="h-4 w-4 mr-2" />
                )}
                Iniciar Agendador
              </Button>
            )}
            
            <Button 
              variant="outline"
              onClick={handleRunNow}
              disabled={actionLoading === 'run' || status?.running || !sharepointStatus?.configured}
              data-testid="run-now-button"
            >
              {actionLoading === 'run' ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <RefreshCw className="h-4 w-4 mr-2" />
              )}
              Executar Agora
            </Button>

            {!sharepointStatus?.configured && (
              <div className="flex items-center gap-2 text-orange-600 bg-orange-50 px-4 py-2 rounded-lg">
                <AlertTriangle className="h-4 w-4" />
                <span className="text-sm">Configure o SharePoint para habilitar o robô</span>
              </div>
            )}
          </div>

          {status?.config && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-700 mb-3 flex items-center gap-2">
                <Folder className="h-4 w-4" />
                Pastas Monitoradas
              </h4>
              <div className="flex flex-wrap gap-2">
                {status.config.source_folders?.map((folder, idx) => (
                  <Badge key={idx} variant="secondary" className="text-xs">
                    {folder}
                  </Badge>
                ))}
              </div>
              <div className="mt-3 text-sm text-gray-500">
                <span className="font-medium">Intervalo:</span> {status.config.interval_minutes || status.interval_minutes} minutos | 
                <span className="font-medium ml-2">Lote:</span> {status.config.batch_size} arquivos
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Tabs de detalhes */}
      <Tabs defaultValue="history" className="w-full">
        <TabsList>
          <TabsTrigger value="history" data-testid="tab-history">
            <Calendar className="h-4 w-4 mr-2" />
            Histórico de Execuções
          </TabsTrigger>
          <TabsTrigger value="files" data-testid="tab-files">
            <FileText className="h-4 w-4 mr-2" />
            Arquivos Processados
          </TabsTrigger>
        </TabsList>

        <TabsContent value="history" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Últimas Execuções</CardTitle>
            </CardHeader>
            <CardContent>
              {history.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <Clock className="h-12 w-12 mx-auto mb-3 text-gray-300" />
                  <p>Nenhuma execução registrada</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {history.map((job, idx) => (
                    <div 
                      key={idx}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                      data-testid={`job-${job.job_id}`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`p-2 rounded-full ${job.success ? 'bg-green-100' : 'bg-red-100'}`}>
                          {job.success ? (
                            <CheckCircle className="h-5 w-5 text-green-600" />
                          ) : (
                            <XCircle className="h-5 w-5 text-red-600" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">
                            Job #{job.job_id}
                          </p>
                          <p className="text-sm text-gray-500">
                            {formatDate(job.finished_at)}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-6 text-sm">
                        <div className="text-center">
                          <p className="font-semibold text-blue-600">{job.files_found || 0}</p>
                          <p className="text-gray-400">Encontrados</p>
                        </div>
                        <div className="text-center">
                          <p className="font-semibold text-green-600">{job.files_processed || 0}</p>
                          <p className="text-gray-400">Processados</p>
                        </div>
                        <div className="text-center">
                          <p className="font-semibold text-red-600">{job.files_failed || 0}</p>
                          <p className="text-gray-400">Falhas</p>
                        </div>
                        <div className="text-center">
                          <p className="font-semibold text-gray-600">{formatDuration(job.duration_seconds)}</p>
                          <p className="text-gray-400">Duração</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="files" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Arquivos do SharePoint</CardTitle>
            </CardHeader>
            <CardContent>
              {files.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <FileText className="h-12 w-12 mx-auto mb-3 text-gray-300" />
                  <p>Nenhum arquivo processado ainda</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {files.map((file, idx) => (
                    <div 
                      key={idx}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      data-testid={`file-${idx}`}
                    >
                      <div className="flex items-center gap-3">
                        <FileText className="h-5 w-5 text-blue-500" />
                        <div>
                          <p className="font-medium text-gray-900">{file.name}</p>
                          <p className="text-xs text-gray-500">{file.source_folder || file.path}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <Badge className={file.processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                          {file.processed ? 'Processado' : 'Pendente'}
                        </Badge>
                        {file.processed_at && (
                          <span className="text-xs text-gray-400">
                            {formatDate(file.processed_at)}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Info sobre configuração */}
      {!sharepointStatus?.configured && (
        <Card className="border-orange-200 bg-orange-50">
          <CardContent className="p-6">
            <div className="flex items-start gap-4">
              <AlertTriangle className="h-6 w-6 text-orange-500 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-orange-800">Configuração Necessária</h3>
                <p className="text-sm text-orange-700 mt-1">
                  Para habilitar o robô de ingestão do SharePoint, configure as seguintes variáveis de ambiente no arquivo <code className="bg-orange-100 px-1 rounded">.env</code>:
                </p>
                <pre className="mt-3 p-3 bg-white rounded-lg text-sm text-gray-700 overflow-x-auto">
{`AZURE_TENANT_ID="seu-tenant-id"
AZURE_CLIENT_ID="seu-client-id"
AZURE_CLIENT_SECRET="seu-client-secret"
SHAREPOINT_SITE_URL="https://empresa.sharepoint.com/sites/SeuSite"
AUTO_START_INGESTION="true"`}
                </pre>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Robos;
