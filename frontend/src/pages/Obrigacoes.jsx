import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Calendar, 
  ChevronLeft, 
  ChevronRight,
  Clock,
  CheckCircle,
  AlertTriangle,
  FileText,
  Search,
  BookOpen
} from 'lucide-react';

const parseData = (value) => {
  if (!value) return null;
  if (value instanceof Date) return Number.isNaN(value.getTime()) ? null : value;

  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
};

const formatarData = (value) => {
  const data = parseData(value);
  return data ? data.toLocaleDateString('pt-BR') : '-';
};

const formatarMoeda = (value) => {
  const number = Number(value || 0);
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(Number.isFinite(number) ? number : 0);
};

const Obrigacoes = () => {
  const navigate = useNavigate();
  const [currentDate, setCurrentDate] = useState(new Date());
  const [obrigacoes, setObrigacoes] = useState([]);
  const [dashboardFiscal, setDashboardFiscal] = useState({});
  const [search, setSearch] = useState('');
  const [empresaFilter, setEmpresaFilter] = useState('todos');
  const [regimeFilter, setRegimeFilter] = useState('todos');
  const [statusFilter, setStatusFilter] = useState('todos');
  const [competenciaFilter, setCompetenciaFilter] = useState('');

  useEffect(() => {
    const carregarObrigacoes = async () => {
      try {
        const [response, dashboardResponse, calendarioResponse] = await Promise.all([
          api.get('/obrigacoes'),
          api.get('/obrigacoes/dashboard').catch(() => ({ data: {} })),
          api.get('/obrigacoes/calendario').catch(() => ({ data: {} })),
        ]);
        const items = Array.isArray(response.data) ? response.data : [];
        setDashboardFiscal(dashboardResponse.data?.data || dashboardResponse.data || {});
        setObrigacoes(items.map((item) => {
          const data = item.data || item;
          return {
            id: item.id || item.mongo_id,
            empresa: data.empresa || data.empresa_nome || data.empresa_id || '',
            codigo: data.codigo_catalogo || data.obrigacao_codigo || data.codigo || '',
            regime: data.regime || data.regime_tributario || '',
            tipo: data.obrigacao_nome || data.tipo || data.nome || 'Obrigacao',
            competencia: data.competencia || '-',
            vencimento: data.vencimento || data.data_vencimento || new Date().toISOString(),
            status: data.status || 'pendente',
            prioridade: data.prioridade || 'normal',
            valor: data.valor || null,
            orgao: data.orgao_responsavel || '',
          };
        }));
      } catch (error) {
        console.error('Erro ao carregar obrigacoes:', error);
        setObrigacoes([]);
      }
    };
    carregarObrigacoes();
  }, []);

  const empresasDisponiveis = useMemo(() => {
    const uniques = new Map();
    obrigacoes.forEach((item) => {
      const label = item.empresa || item.empresa_nome || 'Sem empresa';
      const key = String(item.empresa_id || label).toLowerCase();
      if (!uniques.has(key)) uniques.set(key, label);
    });
    return Array.from(uniques.entries()).map(([value, label]) => ({ value, label }));
  }, [obrigacoes]);

  const obrigacoesFiltradas = useMemo(() => {
    const term = search.trim().toLowerCase();
    return obrigacoes.filter((ob) => {
      const matchesEmpresa =
        empresaFilter === 'todos' ||
        String(ob.empresa_id || ob.empresa || ob.empresa_nome || '').toLowerCase() === empresaFilter;
      const matchesRegime =
        regimeFilter === 'todos' || String(ob.regime || ob.regime_tributario || '').toLowerCase() === regimeFilter;
      const matchesStatus = statusFilter === 'todos' || String(ob.status || '').toLowerCase() === statusFilter;
      const matchesCompetencia = !competenciaFilter || String(ob.competencia || '').toLowerCase().includes(competenciaFilter.toLowerCase());
      const matchesTerm =
        !term ||
        String(ob.tipo || ob.nome || '').toLowerCase().includes(term) ||
        String(ob.empresa || ob.empresa_nome || '').toLowerCase().includes(term) ||
        String(ob.codigo_catalogo || ob.obrigacao_codigo || '').toLowerCase().includes(term);
      return matchesEmpresa && matchesRegime && matchesStatus && matchesCompetencia && matchesTerm;
    });
  }, [competenciaFilter, empresaFilter, obrigacoes, regimeFilter, search, statusFilter]);

  const getStatusConfig = (status) => {
    const configs = {
      'pendente': { color: 'bg-yellow-100 text-yellow-800', icon: Clock, label: 'Pendente' },
      'em_dia': { color: 'bg-emerald-100 text-emerald-800', icon: CheckCircle, label: 'Em dia' },
      'vence_hoje': { color: 'bg-orange-100 text-orange-800', icon: AlertTriangle, label: 'Vence hoje' },
      'vencendo': { color: 'bg-orange-100 text-orange-800', icon: Clock, label: 'Vencendo' },
      'em_andamento': { color: 'bg-blue-100 text-blue-800', icon: FileText, label: 'Em Andamento' },
      'concluida': { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Concluída' },
      'entregue': { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Entregue' },
      'atrasada': { color: 'bg-red-100 text-red-800', icon: AlertTriangle, label: 'Atrasada' }
    };
    return configs[status] || configs['pendente'];
  };

  const getPrioridadeColor = (prioridade) => {
    const colors = {
      'alta': 'border-l-red-500',
      'normal': 'border-l-yellow-500',
      'baixa': 'border-l-green-500'
    };
    return colors[prioridade] || 'border-l-gray-300';
  };

  const getDaysUntil = (date) => {
    const target = parseData(date);
    if (!target) return 0;

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    target.setHours(0, 0, 0, 0);
    const diff = Math.ceil((target - today) / (1000 * 60 * 60 * 24));
    return diff;
  };

  const getDaysUntilText = (date) => {
    const days = getDaysUntil(date);
    if (days < 0) return <span className="text-red-600 font-semibold">Vencido há {Math.abs(days)} dias</span>;
    if (days === 0) return <span className="text-red-600 font-semibold">Vence hoje!</span>;
    if (days === 1) return <span className="text-orange-600">Vence amanhã</span>;
    if (days <= 7) return <span className="text-orange-500">Vence em {days} dias</span>;
    if (days <= 30) return <span className="text-yellow-600">Vence em {days} dias</span>;
    return <span className="text-gray-500">Vence em {days} dias</span>;
  };

  // Calendar logic
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

  const prevMonth = () => setCurrentDate(new Date(year, month - 1));
  const nextMonth = () => setCurrentDate(new Date(year, month + 1));

  const getObrigacoesForDay = (day) => {
    return obrigacoesFiltradas.filter(ob => {
      const obDate = parseData(ob.vencimento);
      if (!obDate) return false;
      return obDate.getDate() === day && obDate.getMonth() === month && obDate.getFullYear() === year;
    });
  };

  const renderCalendarDays = () => {
    const days = [];
    const today = new Date();
    
    // Empty cells before first day
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="h-24 bg-gray-50"></div>);
    }
    
    // Days of month
    for (let day = 1; day <= daysInMonth; day++) {
      const obrigacoesDia = getObrigacoesForDay(day);
      const isToday = today.getDate() === day && today.getMonth() === month && today.getFullYear() === year;
      
      days.push(
        <div 
          key={day} 
          className={`h-24 border border-gray-200 p-1 ${isToday ? 'bg-blue-50 ring-2 ring-blue-400' : 'bg-white'}`}
        >
          <div className={`text-sm font-medium mb-1 ${isToday ? 'text-blue-600' : 'text-gray-700'}`}>
            {day}
          </div>
          <div className="space-y-1 overflow-hidden">
            {obrigacoesDia.slice(0, 2).map((ob, idx) => (
              <div 
                key={idx}
                className={`text-xs px-1 py-0.5 rounded truncate ${
                  ob.status === 'concluida' ? 'bg-green-100 text-green-700' :
                  ob.prioridade === 'alta' ? 'bg-red-100 text-red-700' :
                  'bg-yellow-100 text-yellow-700'
                }`}
                title={`${ob.empresa} - ${ob.tipo}`}
              >
                {ob.tipo}
              </div>
            ))}
            {obrigacoesDia.length > 2 && (
              <div className="text-xs text-gray-500">+{obrigacoesDia.length - 2} mais</div>
            )}
          </div>
        </div>
      );
    }
    
    return days;
  };

  const obrigacoesPendentes = obrigacoesFiltradas.filter(ob => !['concluida', 'entregue'].includes(ob.status)).sort((a, b) => new Date(a.vencimento) - new Date(b.vencimento));

  return (
    <div className="space-y-6" data-testid="obrigacoes-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Obrigações Fiscais</h1>
        <p className="text-gray-500">Calendário de obrigações e vencimentos</p>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            <div className="relative md:col-span-2">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input className="pl-10" placeholder="Buscar por obrigação, empresa ou código" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>
            <Select value={empresaFilter} onValueChange={setEmpresaFilter}>
              <SelectTrigger><SelectValue placeholder="Empresa" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="todos">Todas as empresas</SelectItem>
                {empresasDisponiveis.map((item) => <SelectItem key={item.value} value={item.value}>{item.label}</SelectItem>)}
              </SelectContent>
            </Select>
            <Select value={regimeFilter} onValueChange={setRegimeFilter}>
              <SelectTrigger><SelectValue placeholder="Regime" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="todos">Todos os regimes</SelectItem>
                <SelectItem value="simples_nacional">Simples Nacional</SelectItem>
                <SelectItem value="lucro_real">Lucro Real</SelectItem>
                <SelectItem value="lucro_presumido">Lucro Presumido</SelectItem>
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger><SelectValue placeholder="Status" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="todos">Todos os status</SelectItem>
                <SelectItem value="em_dia">Em dia</SelectItem>
                <SelectItem value="vencendo">Vencendo</SelectItem>
                <SelectItem value="vence_hoje">Vence hoje</SelectItem>
                <SelectItem value="atrasada">Atrasada</SelectItem>
                <SelectItem value="entregue">Entregue</SelectItem>
              </SelectContent>
            </Select>
            <div className="flex items-center gap-2">
              <Input placeholder="Competência AAAA-MM" value={competenciaFilter} onChange={(e) => setCompetenciaFilter(e.target.value)} />
              <Button variant="outline" onClick={() => navigate('/catalogo-obrigacoes')}>
                <BookOpen className="h-4 w-4 mr-2" />
                Catálogo
              </Button>
            </div>
          </div>
      </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Total</p>
            <p className="text-2xl font-bold">{dashboardFiscal.total ?? obrigacoesFiltradas.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Em dia</p>
            <p className="text-2xl font-bold">{dashboardFiscal.em_dia ?? 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Vencendo</p>
            <p className="text-2xl font-bold">{dashboardFiscal.vencendo ?? 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-sm text-gray-500">Atrasadas</p>
            <p className="text-2xl font-bold">{dashboardFiscal.atrasadas ?? 0}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              {monthNames[month]} {year}
            </CardTitle>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="icon" onClick={prevMonth}>
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="icon" onClick={nextMonth}>
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-7 gap-0">
              {['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'].map(day => (
                <div key={day} className="h-8 flex items-center justify-center bg-gray-100 text-xs font-medium text-gray-600">
                  {day}
                </div>
              ))}
              {renderCalendarDays()}
            </div>
            <div className="mt-4 flex items-center gap-4 text-xs">
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 bg-red-100 rounded"></div>
                <span>Prioridade Alta</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 bg-yellow-100 rounded"></div>
                <span>Normal</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 bg-green-100 rounded"></div>
                <span>Concluída</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Upcoming */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Próximos Vencimentos
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
          {obrigacoesPendentes.slice(0, 6).map((ob) => {
              const statusConfig = getStatusConfig(ob.status);
              const StatusIcon = statusConfig.icon;
              
              return (
                <div 
                  key={ob.id}
                  className={`p-3 rounded-lg border-l-4 bg-gray-50 ${getPrioridadeColor(ob.prioridade)}`}
                  data-testid={`obrigacao-${ob.id}`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium text-sm">{ob.tipo}</p>
                      <p className="text-xs text-gray-500">{ob.empresa}</p>
                      {ob.codigo && <p className="text-xs text-gray-400">{ob.codigo}</p>}
                      {ob.valor && (
                        <p className="text-xs text-gray-600 mt-1">
                          {formatarMoeda(ob.valor)}
                        </p>
                      )}
                    </div>
                    <Badge className={statusConfig.color}>
                      <StatusIcon className="h-3 w-3 mr-1" />
                      {statusConfig.label}
                    </Badge>
                  </div>
                  <div className="mt-2 text-xs">
                    {getDaysUntilText(ob.vencimento)}
                  </div>
                </div>
              );
            })}
          </CardContent>
        </Card>
      </div>

      {/* Full List */}
      <Card>
        <CardHeader>
          <CardTitle>Todas as Obrigações</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empresa</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Competência</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vencimento</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Valor</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prazo</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {obrigacoesFiltradas.map((ob) => {
                  const statusConfig = getStatusConfig(ob.status);
                  return (
                    <tr key={ob.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm font-medium">{ob.empresa}</td>
                      <td className="px-4 py-3 text-sm">{ob.tipo}</td>
                      <td className="px-4 py-3 text-sm">{ob.competencia}</td>
                      <td className="px-4 py-3 text-sm">{formatarData(ob.vencimento)}</td>
                      <td className="px-4 py-3 text-sm">{ob.valor ? formatarMoeda(ob.valor) : '-'}</td>
                      <td className="px-4 py-3">
                        <Badge className={statusConfig.color}>{statusConfig.label}</Badge>
                      </td>
                      <td className="px-4 py-3 text-sm">{getDaysUntilText(ob.vencimento)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Obrigacoes;
