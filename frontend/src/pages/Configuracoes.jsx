import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import {
  User,
  Bell,
  Shield,
  Palette,
  Mail,
  Key,
  MessageSquare,
  Send,
  Hash,
  Users,
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { isAdminUser } from '@/lib/rbac';
import api from '@/services/api';
import ConfiguracoesUsuariosViewer from '@/pages/ConfiguracoesUsuariosViewer';

const channelOptions = [
  { key: 'email', label: 'Email', icon: Mail },
  { key: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
  { key: 'teams', label: 'Teams', icon: Users },
  { key: 'slack', label: 'Slack', icon: Hash },
];

const defaultPreference = {
  name: '',
  email: '',
  whatsapp: '',
  ativo: true,
  channels: ['email'],
  tipos_alerta: ['alerta', 'evento'],
  prioridade_minima: 'alta',
  horario_inicio: '00:00',
  horario_fim: '23:59',
};

const formatDateTime = (value) => {
  if (!value) return '-';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '-' : date.toLocaleString('pt-BR');
};

const Configuracoes = () => {
  const { user } = useAuth();
  const isAdmin = isAdminUser(user);
  const [channels, setChannels] = useState([]);
  const [preference, setPreference] = useState(defaultPreference);
  const [notificationLogs, setNotificationLogs] = useState([]);
  const [notificationsLoading, setNotificationsLoading] = useState(false);
  const [testingChannel, setTestingChannel] = useState(null);

  const loadNotifications = async () => {
    setNotificationsLoading(true);
    try {
      const [channelsRes, preferencesRes, logsRes] = await Promise.all([
        api.get('/notificacoes/channels'),
        api.get('/notificacoes/preferences'),
        api.get('/notificacoes/logs'),
      ]);
      const loadedPreferences = preferencesRes.data || [];
      setChannels(channelsRes.data || []);
      setNotificationLogs(logsRes.data || []);
      setPreference({
        ...defaultPreference,
        name: user?.name || user?.email || '',
        email: user?.email || '',
        ...(loadedPreferences[0] || {}),
      });
    } catch (error) {
      console.error('Erro ao carregar notificacoes:', error);
    } finally {
      setNotificationsLoading(false);
    }
  };

  useEffect(() => {
    loadNotifications();
  }, []);

  const togglePreferenceChannel = (channel) => {
    const current = preference.channels || [];
    setPreference({
      ...preference,
      channels: current.includes(channel)
        ? current.filter((item) => item !== channel)
        : [...current, channel],
    });
  };

  const saveNotificationPreference = async () => {
    await api.put('/notificacoes/preferences', { preferences: [preference] });
    await loadNotifications();
  };

  const testNotification = async (channel) => {
    setTestingChannel(channel);
    try {
      await api.post('/notificacoes/test', {
        channel,
        email: preference.email,
        whatsapp: preference.whatsapp,
        mensagem: `Teste de notificacao via ${channel}`,
      });
      await loadNotifications();
    } finally {
      setTestingChannel(null);
    }
  };

  return (
    <div className="space-y-6" data-testid="configuracoes-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Configuracoes</h1>
        <p className="text-gray-500">Gerencie suas preferencias e configuracoes</p>
      </div>

      <Tabs defaultValue="perfil" className="space-y-6">
        <TabsList>
          <TabsTrigger value="perfil"><User className="h-4 w-4 mr-2" /> Perfil</TabsTrigger>
          <TabsTrigger value="notificacoes"><Bell className="h-4 w-4 mr-2" /> Notificacoes</TabsTrigger>
          <TabsTrigger value="seguranca"><Shield className="h-4 w-4 mr-2" /> Seguranca</TabsTrigger>
          {isAdmin && (
            <TabsTrigger value="usuarios-viewer"><Users className="h-4 w-4 mr-2" /> Usuarios Viewer</TabsTrigger>
          )}
          <TabsTrigger value="aparencia"><Palette className="h-4 w-4 mr-2" /> Aparencia</TabsTrigger>
        </TabsList>

        <TabsContent value="perfil">
          <Card>
            <CardHeader>
              <CardTitle>Informacoes do Perfil</CardTitle>
              <CardDescription>Atualize suas informacoes pessoais</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-20 h-20 bg-blue-900 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                </div>
                <div>
                  <Button variant="outline" size="sm">Alterar Foto</Button>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="nome">Nome Completo</Label>
                  <Input id="nome" defaultValue={user?.name || 'Administrador'} />
                </div>
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" type="email" defaultValue={user?.email || 'admin@empresa.com'} />
                </div>
                <div>
                  <Label htmlFor="telefone">Telefone</Label>
                  <Input id="telefone" placeholder="(00) 00000-0000" />
                </div>
                <div>
                  <Label htmlFor="cargo">Cargo</Label>
                  <Input id="cargo" defaultValue="Administrador" />
                </div>
              </div>
              <Button className="bg-blue-900 hover:bg-blue-800">Salvar Alteracoes</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notificacoes">
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              {channelOptions.map(({ key, label, icon: Icon }) => {
                const channel = channels.find((item) => item.name === key || item.id === key);
                const active = (preference.channels || []).includes(key);
                return (
                  <Card key={key}>
                    <CardContent className="p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <Icon className="h-5 w-5 text-gray-600" />
                        <Badge variant={channel?.configured ? 'default' : 'outline'}>
                          {channel?.configured ? 'Configurado' : 'Log'}
                        </Badge>
                      </div>
                      <div>
                        <p className="font-medium">{label}</p>
                        <p className="text-xs text-gray-500">{active ? 'Ativo para este usuario' : 'Inativo'}</p>
                      </div>
                      <div className="flex items-center justify-between">
                        <Switch checked={active} onCheckedChange={() => togglePreferenceChannel(key)} />
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => testNotification(key)}
                          disabled={testingChannel === key || notificationsLoading}
                        >
                          <Send className="h-4 w-4 mr-1" />
                          Testar
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Preferencias de Notificacao</CardTitle>
                <CardDescription>Canais, destinos e regras usadas pelos alertas e eventos</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label>Nome</Label>
                    <Input value={preference.name || ''} onChange={(e) => setPreference({ ...preference, name: e.target.value })} />
                  </div>
                  <div>
                    <Label>Email destino</Label>
                    <Input type="email" value={preference.email || ''} onChange={(e) => setPreference({ ...preference, email: e.target.value })} />
                  </div>
                  <div>
                    <Label>Telefone WhatsApp</Label>
                    <Input value={preference.whatsapp || ''} onChange={(e) => setPreference({ ...preference, whatsapp: e.target.value })} />
                  </div>
                  <div>
                    <Label>Prioridade minima</Label>
                    <select
                      className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                      value={preference.prioridade_minima || 'alta'}
                      onChange={(e) => setPreference({ ...preference, prioridade_minima: e.target.value })}
                    >
                      <option value="baixa">Baixa</option>
                      <option value="media">Media</option>
                      <option value="alta">Alta</option>
                      <option value="critica">Critica</option>
                    </select>
                  </div>
                  <div>
                    <Label>Horario inicio</Label>
                    <Input type="time" value={preference.horario_inicio || '00:00'} onChange={(e) => setPreference({ ...preference, horario_inicio: e.target.value })} />
                  </div>
                  <div>
                    <Label>Horario fim</Label>
                    <Input type="time" value={preference.horario_fim || '23:59'} onChange={(e) => setPreference({ ...preference, horario_fim: e.target.value })} />
                  </div>
                </div>
                <div className="flex items-center justify-between border rounded-md p-3">
                  <div>
                    <p className="font-medium">Preferencia ativa</p>
                    <p className="text-sm text-gray-500">Desativada, apenas logs administrativos continuam sendo registrados</p>
                  </div>
                  <Switch checked={preference.ativo !== false} onCheckedChange={(v) => setPreference({ ...preference, ativo: v })} />
                </div>
                <Button onClick={saveNotificationPreference} disabled={notificationsLoading} className="bg-blue-900 hover:bg-blue-800">
                  Salvar Preferencias
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Logs Recentes</CardTitle>
                <CardDescription>Resultado dos envios processados pelo worker</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {notificationLogs.slice(0, 8).map((item) => (
                    <div key={item.id} className="flex items-center justify-between border rounded-md p-3">
                      <div>
                        <p className="font-medium">{item.subject || item.tipo || 'Notificacao'}</p>
                        <p className="text-sm text-gray-500">{item.channel} - {item.mode || '-'} - {formatDateTime(item.created_at)}</p>
                      </div>
                      <Badge variant={item.status === 'error' ? 'destructive' : 'outline'}>{item.status}</Badge>
                    </div>
                  ))}
                  {notificationLogs.length === 0 && (
                    <div className="text-center py-8 text-gray-500">Nenhum log de notificacao registrado</div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="seguranca">
          <Card>
            <CardHeader>
              <CardTitle>Seguranca da Conta</CardTitle>
              <CardDescription>Gerencie a seguranca da sua conta</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h3 className="font-medium mb-3 flex items-center gap-2">
                  <Key className="h-4 w-4" /> Alterar Senha
                </h3>
                <div className="space-y-3 max-w-md">
                  <div>
                    <Label htmlFor="senha-atual">Senha Atual</Label>
                    <Input id="senha-atual" type="password" />
                  </div>
                  <div>
                    <Label htmlFor="nova-senha">Nova Senha</Label>
                    <Input id="nova-senha" type="password" />
                  </div>
                  <div>
                    <Label htmlFor="confirmar-senha">Confirmar Nova Senha</Label>
                    <Input id="confirmar-senha" type="password" />
                  </div>
                  <Button className="bg-blue-900 hover:bg-blue-800">Alterar Senha</Button>
                </div>
              </div>
              <div className="border-t pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Autenticacao em Duas Etapas</p>
                    <p className="text-sm text-gray-500">Adicione uma camada extra de seguranca</p>
                  </div>
                  <Switch />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {isAdmin && (
          <TabsContent value="usuarios-viewer">
            <ConfiguracoesUsuariosViewer />
          </TabsContent>
        )}

        <TabsContent value="aparencia">
          <Card>
            <CardHeader>
              <CardTitle>Preferencias de Aparencia</CardTitle>
              <CardDescription>Personalize a aparencia do sistema</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Modo Escuro</p>
                  <p className="text-sm text-gray-500">Usar tema escuro na interface</p>
                </div>
                <Switch />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Menu Compacto</p>
                  <p className="text-sm text-gray-500">Reduzir tamanho do menu lateral</p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Configuracoes;
