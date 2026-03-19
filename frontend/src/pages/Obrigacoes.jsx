import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Calendar, 
  ChevronLeft, 
  ChevronRight,
  Clock,
  CheckCircle,
  AlertTriangle,
  FileText
} from 'lucide-react';

const Obrigacoes = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [obrigacoes] = useState([
    { id: 1, empresa: 'TRES PINHEIROS', tipo: 'DAS', competencia: '01/2025', vencimento: new Date(2025, 1, 20), status: 'pendente', prioridade: 'alta', valor: 4500 },
    { id: 2, empresa: 'SUPER GALO', tipo: 'DAS', competencia: '01/2025', vencimento: new Date(2025, 1, 20), status: 'pendente', prioridade: 'normal', valor: 8900 },
    { id: 3, empresa: 'TECH SOLUTIONS', tipo: 'DCTF Web', competencia: '12/2024', vencimento: new Date(2025, 1, 22), status: 'em_andamento', prioridade: 'normal', valor: null },
    { id: 4, empresa: 'MAFE REST.', tipo: 'Certidão FGTS', competencia: '-', vencimento: new Date(2025, 1, 25), status: 'pendente', prioridade: 'baixa', valor: null },
    { id: 5, empresa: 'TRES PINHEIROS', tipo: 'DCTF', competencia: '12/2024', vencimento: new Date(2025, 1, 28), status: 'concluida', prioridade: 'normal', valor: null },
    { id: 6, empresa: 'SUPER GALO', tipo: 'ECD', competencia: '2024', vencimento: new Date(2025, 4, 31), status: 'pendente', prioridade: 'baixa', valor: null },
    { id: 7, empresa: 'TRES PINHEIROS', tipo: 'DAS', competencia: '02/2025', vencimento: new Date(2025, 2, 20), status: 'pendente', prioridade: 'normal', valor: 4200 },
  ]);

  const getStatusConfig = (status) => {
    const configs = {
      'pendente': { color: 'bg-yellow-100 text-yellow-800', icon: Clock, label: 'Pendente' },
      'em_andamento': { color: 'bg-blue-100 text-blue-800', icon: FileText, label: 'Em Andamento' },
      'concluida': { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Concluída' },
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
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const target = new Date(date);
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
    return obrigacoes.filter(ob => {
      const obDate = new Date(ob.vencimento);
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

  const obrigacoesPendentes = obrigacoes.filter(ob => ob.status !== 'concluida').sort((a, b) => new Date(a.vencimento) - new Date(b.vencimento));

  return (
    <div className="space-y-6" data-testid="obrigacoes-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Obrigações Fiscais</h1>
        <p className="text-gray-500">Calendário de obrigações e vencimentos</p>
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
                      {ob.valor && (
                        <p className="text-xs text-gray-600 mt-1">
                          R$ {ob.valor.toLocaleString('pt-BR')}
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
                {obrigacoes.map((ob) => {
                  const statusConfig = getStatusConfig(ob.status);
                  return (
                    <tr key={ob.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm font-medium">{ob.empresa}</td>
                      <td className="px-4 py-3 text-sm">{ob.tipo}</td>
                      <td className="px-4 py-3 text-sm">{ob.competencia}</td>
                      <td className="px-4 py-3 text-sm">{ob.vencimento.toLocaleDateString('pt-BR')}</td>
                      <td className="px-4 py-3 text-sm">{ob.valor ? `R$ ${ob.valor.toLocaleString('pt-BR')}` : '-'}</td>
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
