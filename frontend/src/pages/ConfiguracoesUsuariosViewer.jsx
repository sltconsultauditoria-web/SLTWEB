import { useEffect, useMemo, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { Edit, Loader2, Plus, RefreshCw, Search, Trash2, UserRound } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { useAuth } from '@/context/AuthContext';
import { isAdminUser, userRole } from '@/lib/rbac';
import { cn } from '@/lib/utils';

const emptyForm = {
  nome: '',
  email: '',
  senha: '',
};

const normalizeList = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.viewers)) return payload.viewers;
  if (Array.isArray(payload?.usuarios)) return payload.usuarios;
  return [];
};

const formatDate = (value) => {
  if (!value) return '-';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '-' : date.toLocaleDateString('pt-BR');
};

const RoleBadge = ({ role }) => {
  const normalized = String(role || 'viewer').toLowerCase();
  const admin = normalized.includes('admin');
  return (
    <Badge className={cn(admin ? 'bg-red-600 hover:bg-red-600' : 'bg-blue-600 hover:bg-blue-600')}>
      {admin ? 'ADMIN' : 'VIEWER'}
    </Badge>
  );
};

const ConfiguracoesUsuariosViewer = () => {
  const { user, api } = useAuth();
  const isAdmin = isAdminUser(user);
  const [viewers, setViewers] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [selectedViewer, setSelectedViewer] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const filteredViewers = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return viewers;
    return viewers.filter((viewer) => {
      const nome = String(viewer.nome || viewer.name || '').toLowerCase();
      const email = String(viewer.email || '').toLowerCase();
      return nome.includes(term) || email.includes(term);
    });
  }, [search, viewers]);

  const loadViewers = async (clearFeedback = true) => {
    setLoading(true);
    if (clearFeedback) {
      setFeedback(null);
    }
    try {
      const response = await api.get('/usuarios/viewers');
      const items = normalizeList(response.data).filter((item) => userRole(item) === 'viewer');
      setViewers(items);
    } catch (error) {
      setFeedback({
        type: 'error',
        message: error?.response?.data?.detail || 'Erro ao carregar viewers',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isAdmin) {
      setLoading(false);
      return;
    }
    loadViewers();
  }, [isAdmin]);

  const openCreateModal = () => {
    setSelectedViewer(null);
    setForm(emptyForm);
    setModalOpen(true);
  };

  const openEditModal = (viewer) => {
    setSelectedViewer(viewer);
    setForm({
      nome: viewer.nome || viewer.name || '',
      email: viewer.email || '',
      senha: '',
    });
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelectedViewer(null);
    setForm(emptyForm);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setFeedback(null);

    const payload = {
      nome: form.nome.trim(),
      email: form.email.trim().toLowerCase(),
      role: 'viewer',
      perfil: 'viewer',
    };
    if (form.senha) {
      payload.senha = form.senha;
    }

    try {
      if (selectedViewer) {
        await api.put(`/usuarios/viewers/${selectedViewer.id}`, payload);
        setFeedback({ type: 'success', message: 'Viewer atualizado com sucesso' });
      } else {
        await api.post('/usuarios/viewers', { ...payload, senha: form.senha });
        setFeedback({ type: 'success', message: 'Viewer criado com sucesso' });
      }
      closeModal();
      await loadViewers(false);
    } catch (error) {
      setFeedback({
        type: 'error',
        message: error?.response?.data?.detail || 'Erro ao salvar viewer',
      });
    } finally {
      setSaving(false);
    }
  };

  const confirmDelete = (viewer) => {
    setSelectedViewer(viewer);
    setDeleteOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedViewer) return;
    setSaving(true);
    setFeedback(null);
    try {
      await api.delete(`/usuarios/viewers/${selectedViewer.id}`);
      setFeedback({ type: 'success', message: 'Viewer excluido com sucesso' });
      setDeleteOpen(false);
      setSelectedViewer(null);
      await loadViewers(false);
    } catch (error) {
      setFeedback({
        type: 'error',
        message: error?.response?.data?.detail || 'Erro ao excluir viewer',
      });
    } finally {
      setSaving(false);
    }
  };

  if (!isAdmin && !loading) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="space-y-6" data-testid="usuarios-viewer-page">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestao de Usuarios Viewer</h1>
          <p className="text-gray-500">Controle contas de visualizacao sem permissao administrativa</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={loadViewers} disabled={loading}>
            <RefreshCw className={cn('h-4 w-4 mr-2', loading && 'animate-spin')} />
            Atualizar
          </Button>
          <Button onClick={openCreateModal} className="bg-blue-900 hover:bg-blue-800" data-testid="btn-criar-viewer">
            <Plus className="h-4 w-4 mr-2" />
            Criar Viewer
          </Button>
        </div>
      </div>

      {feedback && (
        <div
          className={cn(
            'rounded-md border px-4 py-3 text-sm',
            feedback.type === 'error'
              ? 'border-red-200 bg-red-50 text-red-700'
              : 'border-green-200 bg-green-50 text-green-700'
          )}
          role="status"
        >
          {feedback.message}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Viewers ativos</p>
                <p className="text-3xl font-bold">{viewers.filter((item) => item.ativo !== false).length}</p>
              </div>
              <UserRound className="h-9 w-9 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-sm text-gray-500">Total listado</p>
            <p className="text-3xl font-bold">{viewers.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-sm text-gray-500">Permissao fixa</p>
            <div className="mt-2">
              <RoleBadge role="viewer" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <CardTitle>Usuarios Viewer</CardTitle>
              <CardDescription>Somente contas com role/perfil viewer aparecem nesta lista</CardDescription>
            </div>
            <div className="relative w-full md:w-80">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
              <Input
                className="pl-9"
                placeholder="Buscar por nome ou email"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex h-48 items-center justify-center text-gray-500">
              <Loader2 className="h-5 w-5 mr-2 animate-spin" />
              Carregando viewers
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nome</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Criado em</TableHead>
                  <TableHead className="w-28 text-right">Acoes</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredViewers.map((viewer) => (
                  <TableRow key={viewer.id || viewer.email}>
                    <TableCell className="font-medium">{viewer.nome || viewer.name || '-'}</TableCell>
                    <TableCell>{viewer.email}</TableCell>
                    <TableCell><RoleBadge role={viewer.role || viewer.perfil} /></TableCell>
                    <TableCell>
                      <Badge variant={viewer.ativo === false ? 'destructive' : 'outline'}>
                        {viewer.ativo === false ? 'Inativo' : 'Ativo'}
                      </Badge>
                    </TableCell>
                    <TableCell>{formatDate(viewer.created_at)}</TableCell>
                    <TableCell>
                      <div className="flex justify-end gap-2">
                        <Button variant="outline" size="sm" onClick={() => openEditModal(viewer)} aria-label="Editar viewer">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          className="text-red-600 hover:text-red-700"
                          onClick={() => confirmDelete(viewer)}
                          aria-label="Excluir viewer"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
                {filteredViewers.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={6} className="h-32 text-center text-gray-500">
                      Nenhum viewer encontrado
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <Dialog open={modalOpen} onOpenChange={(open) => (open ? setModalOpen(true) : closeModal())}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{selectedViewer ? 'Editar Viewer' : 'Criar Viewer'}</DialogTitle>
            <DialogDescription>O perfil e fixo como VIEWER e nao pode ser alterado pela interface.</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="viewer-nome">Nome</Label>
              <Input
                id="viewer-nome"
                value={form.nome}
                onChange={(event) => setForm({ ...form, nome: event.target.value })}
                required
              />
            </div>
            <div>
              <Label htmlFor="viewer-email">Email</Label>
              <Input
                id="viewer-email"
                type="email"
                value={form.email}
                onChange={(event) => setForm({ ...form, email: event.target.value })}
                disabled={Boolean(selectedViewer)}
                required
              />
            </div>
            <div>
              <Label htmlFor="viewer-senha">{selectedViewer ? 'Nova senha' : 'Senha'}</Label>
              <Input
                id="viewer-senha"
                type="password"
                value={form.senha}
                onChange={(event) => setForm({ ...form, senha: event.target.value })}
                minLength={6}
                required={!selectedViewer}
              />
            </div>
            <div className="flex items-center justify-between rounded-md border p-3">
              <span className="text-sm text-gray-600">Role aplicada no envio</span>
              <RoleBadge role="viewer" />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={closeModal} disabled={saving}>
                Cancelar
              </Button>
              <Button type="submit" disabled={saving} className="bg-blue-900 hover:bg-blue-800">
                {saving && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                Salvar
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      <Dialog open={deleteOpen} onOpenChange={setDeleteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Excluir viewer</DialogTitle>
            <DialogDescription>
              Confirme a exclusao de <strong>{selectedViewer?.email}</strong>. Esta acao remove o acesso do usuario.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteOpen(false)} disabled={saving}>
              Cancelar
            </Button>
            <Button onClick={handleDelete} disabled={saving} className="bg-red-600 hover:bg-red-700">
              {saving && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
              Excluir
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ConfiguracoesUsuariosViewer;
