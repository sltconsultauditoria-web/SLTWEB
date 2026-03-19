import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { 
  Plus, 
  Search, 
  Edit, 
  Trash2, 
  Building2,
  MoreVertical,
  Eye
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import axios from 'axios';
import InputMask from 'react-input-mask';

const Empresas = () => {
  const [empresas, setEmpresas] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingEmpresa, setEditingEmpresa] = useState(null);
  const [formData, setFormData] = useState({
    cnpj: '',
    razao_social: '',
    nome_fantasia: '',
    regime: 'simples',
  });

  useEffect(() => {
    fetchEmpresas();
  }, []);

  const fetchEmpresas = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/empresas');
      setEmpresas(response.data);
    } catch (error) {
      console.error('Erro ao buscar empresas:', error);
    }
  };

  const filteredEmpresas = empresas.filter(emp => {
    // Verifica se os campos necessários estão presentes e válidos
    if (!emp || typeof emp !== 'object') {
      console.error('Empresa inválida:', emp);
      return false;
    }
    if (!emp.razao_social || typeof emp.razao_social !== 'string') {
      console.error('Razão social inválida:', emp);
      return false;
    }
    if (!emp.cnpj || typeof emp.cnpj !== 'string') {
      console.error('CNPJ inválido:', emp);
      return false;
    }
    if (emp.nome_fantasia && typeof emp.nome_fantasia !== 'string') {
      console.error('Nome fantasia inválido:', emp);
      return false;
    }
    return (
      (emp.razao_social.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (emp.cnpj.includes(searchTerm)) ||
      (emp.nome_fantasia?.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  });

  const getRegimeLabel = (regime) => {
    const labels = {
      'simples': 'Simples Nacional',
      'lucro_presumido': 'Lucro Presumido',
      'lucro_real': 'Lucro Real',
      'mei': 'MEI'
    };
    return labels[regime] || regime;
  };

  const getRegimeColor = (regime) => {
    const colors = {
      'simples': 'bg-green-100 text-green-800',
      'lucro_presumido': 'bg-blue-100 text-blue-800',
      'lucro_real': 'bg-purple-100 text-purple-800',
      'mei': 'bg-yellow-100 text-yellow-800'
    };
    return colors[regime] || 'bg-gray-100 text-gray-800';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Dados enviados:', formData);
    try {
      if (editingEmpresa) {
        const response = await axios.put(`http://localhost:8000/api/empresas/${editingEmpresa.id}`, formData);
        setEmpresas(empresas.map(emp => emp.id === editingEmpresa.id ? response.data : emp));
      } else {
        const response = await axios.post('http://localhost:8000/api/empresas', formData);
        console.log('Resposta do backend:', response.data);
        setEmpresas([...empresas, response.data]);
      }
      setIsModalOpen(false);
      setEditingEmpresa(null);
      setFormData({ cnpj: '', razao_social: '', nome_fantasia: '', regime: 'simples' });
    } catch (error) {
      console.error('Erro ao salvar empresa:', error);
    }
  };

  const handleEdit = (empresa) => {
    setEditingEmpresa(empresa);
    setFormData({
      cnpj: empresa.cnpj,
      razao_social: empresa.razao_social,
      nome_fantasia: empresa.nome_fantasia || '',
      regime: empresa.regime
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta empresa?')) {
      try {
        await axios.delete(`http://localhost:8000/api/empresas/${id}`);
        setEmpresas(empresas.filter(emp => emp.id !== id));
      } catch (error) {
        console.error('Erro ao excluir empresa:', error);
      }
    }
  };

  const handleView = (empresa) => {
    alert(`Detalhes da Empresa:\n\nCNPJ: ${empresa.cnpj}\nRazão Social: ${empresa.razao_social}\nNome Fantasia: ${empresa.nome_fantasia}\nRegime: ${getRegimeLabel(empresa.regime)}`);
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
  };

  return (
    <div className="space-y-6" data-testid="empresas-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Empresas</h1>
          <p className="text-gray-500">Gerencie as empresas cadastradas</p>
        </div>
        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
          <DialogTrigger asChild>
            <Button 
              className="bg-blue-900 hover:bg-blue-800"
              onClick={() => {
                setEditingEmpresa(null);
                setFormData({ cnpj: '', razao_social: '', nome_fantasia: '', regime: 'simples' });
              }}
              data-testid="add-empresa-button"
            >
              <Plus className="h-4 w-4 mr-2" />
              Nova Empresa
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>{editingEmpresa ? 'Editar Empresa' : 'Nova Empresa'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="cnpj">CNPJ</Label>
                <InputMask
                  mask="99.999.999/9999-99"
                  value={formData.cnpj}
                  onChange={(e) => setFormData({...formData, cnpj: e.target.value})}
                >
                  {(inputProps) => (
                    <Input
                      {...inputProps}
                      id="cnpj"
                      placeholder="00.000.000/0000-00"
                      required
                      data-testid="cnpj-input"
                    />
                  )}
                </InputMask>
              </div>
              <div>
                <Label htmlFor="razao_social">Razão Social</Label>
                <Input
                  id="razao_social"
                  value={formData.razao_social}
                  onChange={(e) => setFormData({...formData, razao_social: e.target.value})}
                  placeholder="Razão Social da Empresa"
                  required
                  data-testid="razao-social-input"
                />
              </div>
              <div>
                <Label htmlFor="nome_fantasia">Nome Fantasia</Label>
                <Input
                  id="nome_fantasia"
                  value={formData.nome_fantasia}
                  onChange={(e) => setFormData({...formData, nome_fantasia: e.target.value})}
                  placeholder="Nome Fantasia"
                  data-testid="nome-fantasia-input"
                />
              </div>
              <div>
                <Label htmlFor="regime">Regime Tributário</Label>
                <Select value={formData.regime} onValueChange={(value) => setFormData({...formData, regime: value})}>
                  <SelectTrigger data-testid="regime-select">
                    <SelectValue placeholder="Selecione o regime" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="simples">Simples Nacional</SelectItem>
                    <SelectItem value="lucro_presumido">Lucro Presumido</SelectItem>
                    <SelectItem value="lucro_real">Lucro Real</SelectItem>
                    <SelectItem value="mei">MEI</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setIsModalOpen(false)}>
                  Cancelar
                </Button>
                <Button type="submit" className="bg-blue-900 hover:bg-blue-800" data-testid="save-empresa-button">
                  {editingEmpresa ? 'Salvar' : 'Cadastrar'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Search */}
      <Card>
        <CardContent className="p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Buscar por CNPJ, Razão Social ou Nome Fantasia..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
              data-testid="search-input"
            />
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Empresa</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CNPJ</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Regime</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Receita Bruta</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fator R</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredEmpresas.map((empresa) => (
                  <tr key={empresa.id} className="hover:bg-gray-50" data-testid={`empresa-row-${empresa.id}`}>
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <Building2 className="h-5 w-5 text-blue-600" />
                        </div>
                        <div className="ml-3">
                          <p className="text-sm font-medium text-gray-900">{empresa.nome_fantasia || empresa.razao_social}</p>
                          <p className="text-xs text-gray-500">{empresa.razao_social}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{empresa.cnpj}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getRegimeColor(empresa.regime)}`}>
                        {getRegimeLabel(empresa.regime)}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{formatCurrency(empresa.receita_bruta)}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{empresa.fator_r > 0 ? `${empresa.fator_r}%` : '-'}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${empresa.ativo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {empresa.ativo ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon" data-testid={`actions-${empresa.id}`}>
                            <MoreVertical className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => handleEdit(empresa)}>
                            <Edit className="h-4 w-4 mr-2" /> Editar
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleView(empresa)}>
                            <Eye className="h-4 w-4 mr-2" /> Visualizar
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleDelete(empresa.id)} className="text-red-600">
                            <Trash2 className="h-4 w-4 mr-2" /> Excluir
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {filteredEmpresas.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <Building2 className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Nenhuma empresa encontrada</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Empresas;
