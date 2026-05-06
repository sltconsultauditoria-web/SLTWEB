import { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { 
  Users, 
  Plus, 
  Edit, 
  Trash2, 
  Shield, 
  Key,
  RefreshCw,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { isAdminUser } from '@/lib/rbac';

const formatarData = (value) => {
  if (!value) return '-';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '-' : date.toLocaleDateString('pt-BR');
};

const Usuarios = () => {
  const { user, api } = useAuth();
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [selectedUsuario, setSelectedUsuario] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [usuarioToDelete, setUsuarioToDelete] = useState(null);

  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    password: '',
    perfil: 'viewer',
    role: 'viewer',
    ativo: true
  });

  const isAdmin = isAdminUser(user);

  useEffect(() => {
    if (!isAdmin) {
      setLoading(false);
      return;
    }
    loadUsuarios();
  }, [isAdmin]);

  const loadUsuarios = async () => {
    try {
      setLoading(true);
      const response = await api.get('/usuarios');
      setUsuarios(Array.isArray(response.data) ? response.data : response.data?.usuarios || []);
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
      if (error.response?.status === 403 || error.response?.status === 401) {
        alert('Sem permissão para acessar usuários');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (!isEditMode && !isAdmin) {
        alert('Apenas administradores podem criar usuarios');
        return;
      }
      
      if (isEditMode && selectedUsuario) {
        // Editar usuário (sem enviar senha)
        const { password, ...updateData } = formData;
        if (password) {
          updateData.password = password;
        }
        await api.put(`/usuarios/${selectedUsuario.id}`, updateData);
      } else {
        // Criar novo usuário
        const createData = {
          ...formData,
          perfil: 'viewer',
          role: 'viewer',
        };
        await api.post('/usuarios', createData);
      }
      
      setIsModalOpen(false);
      loadUsuarios();
      resetForm();
    } catch (error) {
      console.error('Erro ao salvar usuário:', error);
      alert(error.response?.data?.detail || 'Erro ao salvar usuário');
    }
  };

  const handleEdit = (usuario) => {
    setSelectedUsuario(usuario);
    setFormData({
      nome: usuario.nome,
      email: usuario.email,
      password: '',
      perfil: usuario.perfil || usuario.role || 'viewer',
      role: usuario.role || usuario.perfil || 'viewer',
      ativo: usuario.ativo
    });
    setIsEditMode(true);
    setIsModalOpen(true);
  };

  const handleDelete = async () => {
    if (!usuarioToDelete) return;
    
    try {
      await api.delete(`/usuarios/${usuarioToDelete.id}`);
      setDeleteDialogOpen(false);
      setUsuarioToDelete(null);
      loadUsuarios();
    } catch (error) {
      console.error('Erro ao deletar usuário:', error);
      alert(error.response?.data?.detail || 'Erro ao deletar usuário');
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      email: '',
      password: '',
      perfil: 'viewer',
      role: 'viewer',
      ativo: true
    });
    setIsEditMode(false);
    setSelectedUsuario(null);
  };

  const getPerfilBadge = (perfil) => {
    switch(perfil) {
      case 'super_admin':
        return <Badge className="bg-purple-600">Super Admin</Badge>;
      case 'admin':
        return <Badge className="bg-blue-600">Admin</Badge>;
      case 'user':
        return <Badge variant="outline">Usuário</Badge>;
      case 'viewer':
        return <Badge variant="outline">Visualizacao</Badge>;
      case 'visualizacao':
        return <Badge variant="outline">Visualizacao</Badge>;
      default:
        return <Badge>{perfil}</Badge>;
    }
  };

  const getPerfilLabel = (perfil) => {
    switch(perfil) {
      case 'super_admin':
        return 'Super Administrador';
      case 'admin':
        return 'Administrador';
      case 'user':
        return 'Usuário';
      case 'viewer':
        return 'Visualizacao';
      case 'visualizacao':
        return 'Visualizacao';
      default:
        return perfil;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-900"></div>
      </div>
    );
  }

  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="space-y-6" data-testid="usuarios-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestão de Usuários</h1>
          <p className="text-gray-500">Controle de acessos e permissões</p>
        </div>
        <Dialog open={isModalOpen} onOpenChange={(open) => {
          setIsModalOpen(open);
          if (!open) resetForm();
        }}>
          {isAdmin && (
          <DialogTrigger asChild>
            <Button data-testid="btn-novo-usuario">
              <Plus className="h-4 w-4 mr-2" />
              Novo Usuário
            </Button>
          </DialogTrigger>
          )}
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>{isEditMode ? 'Editar Usuário' : 'Novo Usuário'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label>Nome Completo</Label>
                <Input 
                  required
                  value={formData.nome} 
                  onChange={(e) => setFormData({...formData, nome: e.target.value})} 
                  placeholder="João Silva"
                />
              </div>
              <div>
                <Label>Email</Label>
                <Input 
                  required
                  type="email"
                  value={formData.email} 
                  onChange={(e) => setFormData({...formData, email: e.target.value})} 
                  placeholder="joao@empresa.com"
                  disabled={isEditMode}
                />
              </div>
              {!isEditMode && (
                <div>
                  <Label>Senha</Label>
                  <Input 
                    required={!isEditMode}
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    placeholder="Mínimo 6 caracteres"
                    minLength={6}
                  />
                </div>
              )}
              <div>
                <Label>Perfil de Acesso</Label>
                <Select
                  value={isEditMode ? formData.perfil : 'viewer'}
                  onValueChange={(v) => setFormData({...formData, perfil: v, role: v})}
                  disabled={!isEditMode}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="viewer">Visualizacao</SelectItem>
                    <SelectItem value="user">Usuário</SelectItem>
                    <SelectItem value="admin">Administrador</SelectItem>
                    <SelectItem value="super_admin">Super Administrador</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-center space-x-2">
                <input 
                  type="checkbox" 
                  id="ativo" 
                  checked={formData.ativo}
                  onChange={(e) => setFormData({...formData, ativo: e.target.checked})}
                  className="rounded"
                />
                <Label htmlFor="ativo">Usuário Ativo</Label>
              </div>
              <div className="flex gap-2">
                <Button type="submit" className="flex-1">
                  {isEditMode ? 'Atualizar' : 'Criar'}
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => setIsModalOpen(false)}
                >
                  Cancelar
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Total de Usuários</p>
                <p className="text-3xl font-bold">{usuarios.length}</p>
              </div>
              <Users className="h-10 w-10 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Administradores</p>
                <p className="text-3xl font-bold">
                  {usuarios.filter(u => u.perfil === 'admin' || u.perfil === 'super_admin').length}
                </p>
              </div>
              <Shield className="h-10 w-10 text-purple-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Usuários Ativos</p>
                <p className="text-3xl font-bold text-green-600">
                  {usuarios.filter(u => u.ativo).length}
                </p>
              </div>
              <CheckCircle className="h-10 w-10 text-green-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Usuários */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Usuários Cadastrados</CardTitle>
            <Button variant="outline" size="sm" onClick={loadUsuarios}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Atualizar
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {usuarios.length === 0 ? (
              <p className="text-center text-gray-500 py-8">Nenhum usuário encontrado</p>
            ) : (
              usuarios.map((usuario) => (
                <div 
                  key={usuario.id} 
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <p className="font-medium">{usuario.nome}</p>
                      {getPerfilBadge(usuario.perfil)}
                      {!usuario.ativo && (
                        <Badge variant="destructive">
                          <XCircle className="h-3 w-3 mr-1" />
                          Inativo
                        </Badge>
                      )}
                      {usuario.primeiro_login && (
                        <Badge className="bg-yellow-500">
                          <Key className="h-3 w-3 mr-1" />
                          Primeiro Login
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-gray-500">{usuario.email}</p>
                    <p className="text-xs text-gray-400 mt-1">
                      Criado em: {formatarData(usuario.created_at)}
                    </p>
                  </div>
                  {isAdmin && (
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleEdit(usuario)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="text-red-600 hover:text-red-700"
                        onClick={() => {
                          setUsuarioToDelete(usuario);
                          setDeleteDialogOpen(true);
                        }}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Dialog de Confirmação de Exclusão */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirmar Exclusão</DialogTitle>
            <DialogDescription>
              Tem certeza que deseja excluir o usuário <strong>{usuarioToDelete?.nome}</strong>?
              Esta ação não pode ser desfeita.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialogOpen(false)}>Cancelar</Button>
            <Button onClick={handleDelete} className="bg-red-600 hover:bg-red-700">
              Excluir
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Usuarios;
