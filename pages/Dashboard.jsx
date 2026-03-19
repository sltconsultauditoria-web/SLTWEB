import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  Building2, 
  FileText, 
  AlertTriangle, 
  DollarSign,
  TrendingUp,
  Calendar,
  CheckCircle,
  Clock
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
  <Card className="hover:shadow-lg transition-shadow" data-testid={`stat-${title.toLowerCase().replace(/\s/g, '-')}`}>
    <CardContent className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-3xl font-bold mt-1">{value}</p>
          {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const [kpis, setKpis] = useState({
    total_empresas: 0,
    empresas_ativas: 127,
    das_gerados_mes: 98,
    certidoes_emitidas_mes: 245,
    alertas_criticos: 3,
    taxa_conformidade: 94.5,
    receita_mensal: 458000,
    despesa_mensal: 125000
  });
  const [obrigacoes, setObrigacoes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      // Tentar carregar KPIs do backend
      // const response = await axios.get(`${API}/kpis/overview`);
      // setKpis(response.data);
      
      // Dados de exemplo para obrigações
      setObrigacoes([
        { empresa: 'TRES PINHEIROS LTDA', tipo: 'DAS 01/2025', vencimento: '20/02/2025', prioridade: 'alta' },
        { empresa: 'SUPER GALO REST.', tipo: 'DCTF Web', vencimento: '22/02/2025', prioridade: 'normal' },
        { empresa: 'MAFE RESTAURANTE', tipo: 'Certidão FGTS', vencimento: '25/02/2025', prioridade: 'baixa' },
        { empresa: 'TECH SOLUTIONS', tipo: 'DCTF', vencimento: '28/02/2025', prioridade: 'normal' },
      ]);
    } catch (error) {
      console.error('Erro ao carregar KPIs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPrioridadeColor = (prioridade) => {
    switch (prioridade) {
      case 'alta': return 'text-red-600 bg-red-100';
      case 'normal': return 'text-yellow-600 bg-yellow-100';
      case 'baixa': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
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
        <p className="text-gray-500">Visão geral do sistema</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Empresas Ativas"
          value={kpis.empresas_ativas}
          icon={Building2}
          color="bg-blue-500"
          subtitle="+5 este mês"
        />
        <StatCard
          title="DAS Gerados"
          value={kpis.das_gerados_mes}
          icon={FileText}
          color="bg-green-500"
          subtitle="Este mês"
        />
        <StatCard
          title="Certidões Emitidas"
          value={kpis.certidoes_emitidas_mes}
          icon={CheckCircle}
          color="bg-purple-500"
          subtitle="Este mês"
        />
        <StatCard
          title="Alertas Críticos"
          value={kpis.alertas_criticos}
          icon={AlertTriangle}
          color="bg-red-500"
          subtitle="Pendentes"
        />
      </div>

      {/* Segunda linha de KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Taxa Conformidade"
          value={`${kpis.taxa_conformidade}%`}
          icon={TrendingUp}
          color="bg-emerald-500"
        />
        <StatCard
          title="Receitas do Mês"
          value={`R$ ${(kpis.receita_mensal / 1000).toFixed(0)}K`}
          icon={DollarSign}
          color="bg-cyan-500"
        />
        <StatCard
          title="Despesas do Mês"
          value={`R$ ${(kpis.despesa_mensal / 1000).toFixed(0)}K`}
          icon={DollarSign}
          color="bg-orange-500"
        />
        <StatCard
          title="Obrigações Pendentes"
          value={obrigacoes.length}
          icon={Clock}
          color="bg-indigo-500"
        />
      </div>

      {/* Tabelas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Próximos Vencimentos */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Próximos Vencimentos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {obrigacoes.map((ob, index) => (
                <div 
                  key={index} 
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  data-testid={`obrigacao-${index}`}
                >
                  <div>
                    <p className="font-medium text-sm">{ob.empresa}</p>
                    <p className="text-xs text-gray-500">{ob.tipo}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">{ob.vencimento}</p>
                    <span className={`text-xs px-2 py-1 rounded-full ${getPrioridadeColor(ob.prioridade)}`}>
                      {ob.prioridade}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Atividades Recentes */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Atividades Recentes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { acao: 'DAS gerado', empresa: 'TRES PINHEIROS', tempo: 'Há 2 horas', icon: FileText, color: 'text-green-500' },
                { acao: 'Certidão emitida', empresa: 'SUPER GALO', tempo: 'Há 4 horas', icon: CheckCircle, color: 'text-blue-500' },
                { acao: 'Alerta criado', empresa: 'MAFE REST.', tempo: 'Há 6 horas', icon: AlertTriangle, color: 'text-yellow-500' },
                { acao: 'Empresa cadastrada', empresa: 'NOVA EMPRESA', tempo: 'Há 1 dia', icon: Building2, color: 'text-purple-500' },
              ].map((item, index) => (
                <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <item.icon className={`h-5 w-5 ${item.color}`} />
                  <div className="flex-1">
                    <p className="text-sm font-medium">{item.acao}</p>
                    <p className="text-xs text-gray-500">{item.empresa}</p>
                  </div>
                  <span className="text-xs text-gray-400">{item.tempo}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
