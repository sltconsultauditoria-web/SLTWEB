import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';
import { 
  Bell, 
  Mail, 
  MessageSquare, 
  Users,
  Settings,
  Send,
  Plus,
  Trash2,
  Edit,
  CheckCircle,
  AlertTriangle,
  Clock,
  History,
  Play,
  Eye
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ConfiguracaoAlertas = () => {
  const [config, setConfig] = useState({
    email_enabled: true,
    whatsapp_enabled: false,
    teams_enabled: false,
    smtp: null,
    twilio: null,
    teams: null
  });
  const [recipients, setRecipients] = useState(API.get('/replace_with_real_endpoint'));
  const [thresholds, setThresholds] = useState(API.get('/replace_with_real_endpoint'));
  const [history, setHistory] = useState(API.get('/replace_with_real_endpoint'));
  const [pendingAlerts, setPendingAlerts] = useState(API.get('/replace_with_real_endpoint'));
  const [loading, setLoading] = useState(true);
  const [testingChannel, setTestingChannel] = useState(null);
  
  // Forms
  const [smtpForm, setSmtpForm] = useState({ host: '', port: 587, username: '', password: '', from_email: '' });
  const [twilioForm, setTwilioForm] = useState({ account_sid: '', auth_token: '', from_number: '' });
  const [teamsForm, setTeamsForm] = useState({ webhook_url: '', channel_name: '' });
  const [recipientForm, setRecipientForm] = useState({ name: '', email: '', whatsapp: '', notify_email: true, notify_whatsapp: false, notify_teams: true, threshold_levels: ['critico', 'alto'] });
  const [isRecipientModalOpen, setIsRecipientModalOpen] = useState(false);
  const [editingRecipient, setEditingRecipient] = useState(null);

  useEffect(() => {
    loadData();
  }, API.get('/replace_with_real_endpoint'));

  const loadData = async () => {
    try {
      const [configRes, recipientsRes, thresholdsRes, historyRes, pendingRes] = await Promise.all([
        axios.get(`${API}/alerts/config`),
        axios.get(`${API}/alerts/recipients`),
        axios.get(`${API}/alerts/thresholds`),
        axios.get(`${API}/alerts/history`),
        axios.get(`${API}/alerts/preview`)
      ]);
      setConfig(configRes.data);
      setRecipients(recipientsRes.data);
      setThresholds(thresholdsRes.data);
      setHistory(historyRes.data);
      setPendingAlerts(pendingRes.data);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveSMTPConfig = async () => {
    try {
      await axios.post(`${API}/alerts/config/smtp`, smtpForm);
      alert('Configuração SMTP salva com sucesso!');
      loadData();
    } catch (error) {
      alert('Erro ao salvar configuração SMTP');
    }
  };

  const saveTwilioConfig = async () => {
    try {
      await axios.post(`${API}/alerts/config/twilio`, twilioForm);
      alert('Configuração Twilio salva com sucesso!');
      loadData();
    } catch (error) {
      alert('Erro ao salvar configuração Twilio');
    }
  };

  const saveTeamsConfig = async () => {
    try {
      await axios.post(`${API}/alerts/config/teams`, teamsForm);
      alert('Configuração Teams salva com sucesso!');
      loadData();
    } catch (error) {
      alert('Erro ao salvar configuração Teams');
    }
  };

  const testNotification = async (channel) => {
    setTestingChannel(channel);
    try {
      let testConfig = API.get('/replace_with_real_endpoint');
      let recipient = '';
      
      if (channel === 'email') {
        testConfig = smtpForm;
        recipient = smtpForm.from_email || smtpForm.username;
      } else if (channel === 'whatsapp') {
        testConfig = twilioForm;
        recipient = twilioForm.from_number;
      } else if (channel === 'teams') {
        testConfig = teamsForm;
        recipient = teamsForm.webhook_url;
      }
      
      const result = await axios.post(`${API}/alerts/test`, {
        channel,
        config: testConfig,
        recipient
      });
      
      if (result.data.success) {
        alert(`Teste de ${channel} enviado com sucesso!${result.data.simulated ? ' (Simulado - configure as credenciais)' : ''}`);
      } else {
        alert(`Erro no teste: ${result.data.error}`);
      }
    } catch (error) {
      alert(`Erro ao testar ${channel}: ${error.message}`);
    } finally {
      setTestingChannel(null);
    }
  };

  const saveRecipient = async () => {
    try {
      if (editingRecipient) {
        await axios.put(`${API}/alerts/recipients/${editingRecipient.id}`, recipientForm);
      } else {
        await axios.post(`${API}/alerts/recipients`, recipientForm);
      }
      setIsRecipientModalOpen(false);
      setEditingRecipient(null);
      setRecipientForm({ name: '', email: '', whatsapp: '', notify_email: true, notify_whatsapp: false, notify_teams: true, threshold_levels: ['critico', 'alto'] });
      loadData();
    } catch (error) {
      alert('Erro ao salvar destinatário');
    }
  };

  const deleteRecipient = async (id) => {
    if (window.confirm('Tem certeza que deseja remover este destinatário?')) {
      await axios.delete(`${API}/alerts/recipients/${id}`);
      loadData();
    }
  };

  const updateThreshold = async (level, field, value) => {
    const updated = thresholds.map(t => 
      t.level === level ? { ...t, [field]: value } : t
    );
    setThresholds(updated);
    await axios.put(`${API}/alerts/thresholds`, updated);
  };

  const runAlertCheck = async () => {
    try {
      const result = await axios.post(`${API}/alerts/check-and-notify`);
      alert(`Verificação concluída! ${result.data.notified} alerta(s) enviado(s).`);
      loadData();
    } catch (error) {
      alert('Erro ao executar verificação');
    }
  };

  const getThresholdColor = (level) => {
    const colors = {
      'critico': 'bg-red-500',
      'alto': 'bg-orange-500',
      'normal': 'bg-yellow-500',
      'baixo': 'bg-green-500'
    };
    return colors[level] || 'bg-gray-500';
  };

  const getThresholdLabel = (level) => {
    const labels = {
      'critico': 'Crítico (0-2 dias)',
      'alto': 'Alto (3-5 dias)',
      'normal': 'Normal (6-10 dias)',
      'baixo': 'Baixo (11-15 dias)'
    };
    return labels[level] || level;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-900"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="config-alertas-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Configuração de Alertas</h1>
          <p className="text-gray-500">Configure notificações por Email, WhatsApp e Teams</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => loadData()}>
            <Eye className="h-4 w-4 mr-2" /> Atualizar
          </Button>
          <Button className="bg-blue-900 hover:bg-blue-800" onClick={runAlertCheck}>
            <Play className="h-4 w-4 mr-2" /> Executar Verificação
          </Button>
        </div>
      </div>

      {/* Alertas Pendentes */}
      {pendingAlerts.length > 0 && (
        <Card className="border-orange-200 bg-orange-50">
          <CardHeader className="pb-2">
            <CardTitle className="text-orange-700 flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              {pendingAlerts.length} Alerta(s) Pendente(s)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
              {pendingAlerts.map((alert, idx) => (
                <div key={idx} className="bg-white p-3 rounded-lg border">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge className={getThresholdColor(alert.threshold_level)}>{alert.threshold_level}</Badge>
                    <span className="text-sm font-medium">{alert.days_until} dias</span>
                  </div>
                  <p className="text-sm font-medium">{alert.obrigacao.tipo}</p>
                  <p className="text-xs text-gray-500">{alert.obrigacao.empresa}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Tabs defaultValue="canais" className="space-y-6">
        <TabsList>
          <TabsTrigger value="canais"><Settings className="h-4 w-4 mr-2" /> Canais</TabsTrigger>
          <TabsTrigger value="destinatarios"><Users className="h-4 w-4 mr-2" /> Destinatários</TabsTrigger>
          <TabsTrigger value="thresholds"><Bell className="h-4 w-4 mr-2" /> Thresholds</TabsTrigger>
          <TabsTrigger value="historico"><History className="h-4 w-4 mr-2" /> Histórico</TabsTrigger>
        </TabsList>

        {/* Canais */}
        <TabsContent value="canais">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Email */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Mail className="h-5 w-5" /> Email (SMTP)
                  {config.email_enabled && config.smtp && (
                    <Badge className="bg-green-500 ml-auto">Configurado</Badge>
                  )}
                </CardTitle>
                <CardDescription>Configure o servidor SMTP para envio de emails</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Servidor SMTP</Label>
                  <Input 
                    placeholder="smtp.seuservidor.com.br" 
                    value={smtpForm.host}
                    onChange={(e) => setSmtpForm({...smtpForm, host: e.target.value})}
                  />
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label>Porta</Label>
                    <Input 
                      type="number" 
                      placeholder="587" 
                      value={smtpForm.port}
                      onChange={(e) => setSmtpForm({...smtpForm, port: parseInt(e.target.value)})}
                    />
                  </div>
                  <div>
                    <Label>TLS</Label>
                    <div className="flex items-center h-10">
                      <Switch defaultChecked />
                    </div>
                  </div>
                </div>
                <div>
                  <Label>Usuário (Email)</Label>
                  <Input 
                    placeholder="seu@email.com" 
                    value={smtpForm.username}
                    onChange={(e) => setSmtpForm({...smtpForm, username: e.target.value})}
                  />
                </div>
                <div>
                  <Label>Senha</Label>
                  <Input 
                    type="password" 
                    placeholder="********" 
                    value={smtpForm.password}
                    onChange={(e) => setSmtpForm({...smtpForm, password: e.target.value})}
                  />
                </div>
                <div>
                  <Label>Email Remetente (opcional)</Label>
                  <Input 
                    placeholder="alertas@empresa.com" 
                    value={smtpForm.from_email}
                    onChange={(e) => setSmtpForm({...smtpForm, from_email: e.target.value})}
                  />
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveSMTPConfig} className="flex-1">
                    Salvar
                  </Button>
                  <Button 
                    variant="outline" 
                    onClick={() => testNotification('email')}
                    disabled={testingChannel === 'email'}
                  >
                    <Send className="h-4 w-4 mr-1" />
                    {testingChannel === 'email' ? 'Enviando...' : 'Testar'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* WhatsApp */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="h-5 w-5" /> WhatsApp (Twilio)
                  {config.whatsapp_enabled && config.twilio && (
                    <Badge className="bg-green-500 ml-auto">Configurado</Badge>
                  )}
                </CardTitle>
                <CardDescription>Configure o Twilio para envio de WhatsApp</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Account SID</Label>
                  <Input 
                    placeholder="AC..." 
                    value={twilioForm.account_sid}
                    onChange={(e) => setTwilioForm({...twilioForm, account_sid: e.target.value})}
                  />
                </div>
                <div>
                  <Label>Auth Token</Label>
                  <Input 
                    type="password" 
                    placeholder="********" 
                    value={twilioForm.auth_token}
                    onChange={(e) => setTwilioForm({...twilioForm, auth_token: e.target.value})}
                  />
                </div>
                <div>
                  <Label>Número WhatsApp Twilio</Label>
                  <Input 
                    placeholder="+14155238886" 
                    value={twilioForm.from_number}
                    onChange={(e) => setTwilioForm({...twilioForm, from_number: e.target.value})}
                  />
                </div>
                <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
                  <p className="font-medium">Como obter:</p>
                  <p>1. Crie conta em twilio.com</p>
                  <p>2. Ative o sandbox do WhatsApp</p>
                  <p>3. Copie Account SID e Auth Token</p>
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveTwilioConfig} className="flex-1">
                    Salvar
                  </Button>
                  <Button 
                    variant="outline" 
                    onClick={() => testNotification('whatsapp')}
                    disabled={testingChannel === 'whatsapp'}
                  >
                    <Send className="h-4 w-4 mr-1" />
                    {testingChannel === 'whatsapp' ? 'Enviando...' : 'Testar'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Teams */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" /> Microsoft Teams
                  {config.teams_enabled && config.teams && (
                    <Badge className="bg-green-500 ml-auto">Configurado</Badge>
                  )}
                </CardTitle>
                <CardDescription>Configure o webhook do Microsoft Teams</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Webhook URL</Label>
                  <Input 
                    placeholder="https://outlook.office.com/webhook/..." 
                    value={teamsForm.webhook_url}
                    onChange={(e) => setTeamsForm({...teamsForm, webhook_url: e.target.value})}
                  />
                </div>
                <div>
                  <Label>Nome do Canal (opcional)</Label>
                  <Input 
                    placeholder="#alertas-fiscais" 
                    value={teamsForm.channel_name}
                    onChange={(e) => setTeamsForm({...teamsForm, channel_name: e.target.value})}
                  />
                </div>
                <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
                  <p className="font-medium">Como obter:</p>
                  <p>1. Abra o Teams no canal desejado</p>
                  <p>2. Clique em ... > Conectores</p>
                  <p>3. Adicione "Incoming Webhook"</p>
                  <p>4. Copie a URL gerada</p>
                </div>
                <div className="flex gap-2">
                  <Button onClick={saveTeamsConfig} className="flex-1">
                    Salvar
                  </Button>
                  <Button 
                    variant="outline" 
                    onClick={() => testNotification('teams')}
                    disabled={testingChannel === 'teams'}
                  >
                    <Send className="h-4 w-4 mr-1" />
                    {testingChannel === 'teams' ? 'Enviando...' : 'Testar'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Destinatários */}
        <TabsContent value="destinatarios">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Destinatários de Alertas</CardTitle>
                <CardDescription>Pessoas que receberão as notificações</CardDescription>
              </div>
              <Dialog open={isRecipientModalOpen} onOpenChange={setIsRecipientModalOpen}>
                <DialogTrigger asChild>
                  <Button onClick={() => {
                    setEditingRecipient(null);
                    setRecipientForm({ name: '', email: '', whatsapp: '', notify_email: true, notify_whatsapp: false, notify_teams: true, threshold_levels: ['critico', 'alto'] });
                  }}>
                    <Plus className="h-4 w-4 mr-2" /> Adicionar
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>{editingRecipient ? 'Editar' : 'Novo'} Destinatário</DialogTitle>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div>
                      <Label>Nome</Label>
                      <Input 
                        value={recipientForm.name}
                        onChange={(e) => setRecipientForm({...recipientForm, name: e.target.value})}
                        placeholder="Nome completo"
                      />
                    </div>
                    <div>
                      <Label>Email</Label>
                      <Input 
                        type="email"
                        value={recipientForm.email}
                        onChange={(e) => setRecipientForm({...recipientForm, email: e.target.value})}
                        placeholder="email@empresa.com"
                      />
                    </div>
                    <div>
                      <Label>WhatsApp</Label>
                      <Input 
                        value={recipientForm.whatsapp}
                        onChange={(e) => setRecipientForm({...recipientForm, whatsapp: e.target.value})}
                        placeholder="+5511999999999"
                      />
                    </div>
                    <div>
                      <Label className="mb-2 block">Canais de Notificação</Label>
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <Checkbox 
                            checked={recipientForm.notify_email}
                            onCheckedChange={(v) => setRecipientForm({...recipientForm, notify_email: v})}
                          />
                          <span>Email</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Checkbox 
                            checked={recipientForm.notify_whatsapp}
                            onCheckedChange={(v) => setRecipientForm({...recipientForm, notify_whatsapp: v})}
                          />
                          <span>WhatsApp</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Checkbox 
                            checked={recipientForm.notify_teams}
                            onCheckedChange={(v) => setRecipientForm({...recipientForm, notify_teams: v})}
                          />
                          <span>Teams</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <Label className="mb-2 block">Receber alertas de nível</Label>
                      <div className="space-y-2">
                        {['critico', 'alto', 'normal', 'baixo'].map(level => (
                          <div key={level} className="flex items-center gap-2">
                            <Checkbox 
                              checked={recipientForm.threshold_levels.includes(level)}
                              onCheckedChange={(checked) => {
                                if (checked) {
                                  setRecipientForm({...recipientForm, threshold_levels: [...recipientForm.threshold_levels, level]});
                                } else {
                                  setRecipientForm({...recipientForm, threshold_levels: recipientForm.threshold_levels.filter(l => l !== level)});
                                }
                              }}
                            />
                            <Badge className={getThresholdColor(level)}>{getThresholdLabel(level)}</Badge>
                          </div>
                        ))}
                      </div>
                    </div>
                    <Button onClick={saveRecipient} className="w-full">
                      {editingRecipient ? 'Salvar Alterações' : 'Adicionar Destinatário'}
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recipients.map((recipient) => (
                  <div key={recipient.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <Users className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium">{recipient.name}</p>
                        <p className="text-sm text-gray-500">{recipient.email}</p>
                        {recipient.whatsapp && <p className="text-xs text-gray-400">{recipient.whatsapp}</p>}
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="flex gap-1">
                        {recipient.notify_email && <Badge variant="outline"><Mail className="h-3 w-3" /></Badge>}
                        {recipient.notify_whatsapp && <Badge variant="outline"><MessageSquare className="h-3 w-3" /></Badge>}
                        {recipient.notify_teams && <Badge variant="outline"><Users className="h-3 w-3" /></Badge>}
                      </div>
                      <div className="flex gap-1">
                        {recipient.threshold_levels?.map(level => (
                          <div key={level} className={`w-3 h-3 rounded-full ${getThresholdColor(level)}`} title={level}></div>
                        ))}
                      </div>
                      <div className="flex gap-1">
                        <Button variant="ghost" size="icon" onClick={() => {
                          setEditingRecipient(recipient);
                          setRecipientForm(recipient);
                          setIsRecipientModalOpen(true);
                        }}>
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" onClick={() => deleteRecipient(recipient.id)}>
                          <Trash2 className="h-4 w-4 text-red-500" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
                {recipients.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <Users className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>Nenhum destinatário cadastrado</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Thresholds */}
        <TabsContent value="thresholds">
          <Card>
            <CardHeader>
              <CardTitle>Configuração de Thresholds</CardTitle>
              <CardDescription>Define quando e como enviar alertas baseado nos dias até o vencimento</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {thresholds.map((threshold) => (
                  <div key={threshold.level} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className={`w-4 h-12 rounded ${getThresholdColor(threshold.level)}`}></div>
                      <div>
                        <p className="font-medium">{getThresholdLabel(threshold.level)}</p>
                        <p className="text-sm text-gray-500">{threshold.min_days} a {threshold.max_days} dias antes do vencimento</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="flex items-center gap-2">
                        <Mail className="h-4 w-4 text-gray-400" />
                        <Switch 
                          checked={threshold.notify_email}
                          onCheckedChange={(v) => updateThreshold(threshold.level, 'notify_email', v)}
                        />
                      </div>
                      <div className="flex items-center gap-2">
                        <MessageSquare className="h-4 w-4 text-gray-400" />
                        <Switch 
                          checked={threshold.notify_whatsapp}
                          onCheckedChange={(v) => updateThreshold(threshold.level, 'notify_whatsapp', v)}
                        />
                      </div>
                      <div className="flex items-center gap-2">
                        <Users className="h-4 w-4 text-gray-400" />
                        <Switch 
                          checked={threshold.notify_teams}
                          onCheckedChange={(v) => updateThreshold(threshold.level, 'notify_teams', v)}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Histórico */}
        <TabsContent value="historico">
          <Card>
            <CardHeader>
              <CardTitle>Histórico de Alertas Enviados</CardTitle>
              <CardDescription>Últimos alertas enviados pelo sistema</CardDescription>
            </CardHeader>
            <CardContent>
              {history.length > 0 ? (
                <div className="space-y-3">
                  {history.slice().reverse().map((item) => (
                    <div key={item.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-4">
                        {item.success ? (
                          <CheckCircle className="h-5 w-5 text-green-500" />
                        ) : (
                          <AlertTriangle className="h-5 w-5 text-red-500" />
                        )}
                        <div>
                          <p className="font-medium">{item.obrigacao_tipo} - {item.empresa}</p>
                          <p className="text-sm text-gray-500">
                            {new Date(item.timestamp).toLocaleString('pt-BR')}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={getThresholdColor(item.threshold_level)}>{item.threshold_level}</Badge>
                        {item.channels_notified?.map(ch => (
                          <Badge key={ch} variant="outline">{ch}</Badge>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <History className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>Nenhum alerta enviado ainda</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ConfiguracaoAlertas;
