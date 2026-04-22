import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { 
  AlertTriangle, 
  Search, 
  Building2,
  FileText,
  DollarSign,
  Calendar,
  RefreshCw,
  Download,
  ExternalLink,
  Shield,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react';

const Debitos = () => {
  const [selectedEmpresa, setSelectedEmpresa] = useState('');
  const [consultando, setConsultando] = useState(false);
  const [debitos, setDebitos] = useState(null);

  const empresas = [
    { id: 'e1', nome: 'TRES PINHEIROS COMERCIO LTDA', cnpj: '12.345.678/0001-90' },
    { id: 'e2', nome: 'SUPER GALO RESTAURANTE LTDA', cnpj: '98.765.432/0001-10' },
    { id: 'e3', nome: 'MAFE RESTAURANTE EIRELI', cnpj: '11.222.333/0001-44' },
    { id: 'e4', nome: 'TECH SOLUTIONS SA', cnpj: '55.666.777/0001-88' },
  ];

  // Dados simulados de débitos
  const debitosSimulados = {
    'e1': {
      situacao: 'regular',
      federal: [],
      estadual: [],
      municipal: [],
      fgts: [],
      dividaAtiva: []
    },
    'e2': {
      situacao: 'pendencias',
      federal: [
        { id: 1, tributo: 'IRPJ', competencia: '2024', valor: 15420.50, vencimento: '2024-04-30', status: 'vencido', diasAtraso: 240 },
        { id: 2, tributo: 'CSLL', competencia: '2024', valor: 8750.00, vencimento: '2024-04-30', status: 'vencido', diasAtraso: 240 },
      ],
      estadual: [
        { id: 3, tributo: 'ICMS', competencia: '11/2024', valor: 3200.00, vencimento: '2024-12-15', status: 'vencido', diasAtraso: 32 },
      ],
      municipal: [],
      fgts: [
        { id: 4, tributo: 'FGTS', competencia: '10/2024', valor: 1850.00, vencimento: '2024-11-07', status: 'vencido', diasAtraso: 70 },
      ],
      dividaAtiva: [
        { id: 5, tributo: 'INSS', inscricao: '2023/12345', valor: 25000.00, dataInscricao: '2023-06-15', situacao: 'Em cobrança' },
      ]
    },
    'e3': {
      situacao: 'irregular',
      federal: [
        { id: 6, tributo: 'Simples Nacional', competencia: '09/2024', valor: 4500.00, vencimento: '2024-10-20', status: 'vencido', diasAtraso: 88 },
        { id: 7, tributo: 'Simples Nacional', competencia: '10/2024', valor: 4800.00, vencimento: '2024-11-20', status: 'vencido', diasAtraso: 57 },
        { id: 8, tributo: 'Simples Nacional', competencia: '11/2024', valor: 5100.00, vencimento: '2024-12-20', status: 'vencido', diasAtraso: 27 },
      ],
      estadual: [],
      municipal: [
        { id: 9, tributo: 'ISS', competencia: '2024', valor: 2340.00, vencimento: '2024-07-15', status: 'vencido', diasAtraso: 185 },
      ],
      fgts: [],
      dividaAtiva: []
    },
    'e4': {
      situacao: 'regular',
      federal: [],
      estadual: [],
      municipal: [],
      fgts: [],
      dividaAtiva: []
    }
  };

  const consultarDebitos = () => {
    if (!selectedEmpresa) return;
    
    setConsultando(true);
    
    // Simular consulta
    setTimeout(() => {
      setDebitos(debitosSimulados[selectedEmpresa] || debitosSimulados['e1']);
      setConsultando(false);
    }, 2000);
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
  };

  const getSituacaoConfig = (situacao) => {
    const configs = {
      'regular': { color: 'bg-green-500', icon: CheckCircle, label: 'Regular', bgColor: 'bg-green-50', borderColor: 'border-green-200' },
      'pendencias': { color: 'bg-yellow-500', icon: AlertCircle, label: 'Pendências', bgColor: 'bg-yellow-50', borderColor: 'border-yellow-200' },
      'irregular': { color: 'bg-red-500', icon: AlertTriangle, label: 'Irregular', bgColor: 'bg-red-50', borderColor: 'border-red-200' }
    };
    return configs[situacao] || configs['regular'];
  };

  const calcularTotalDebitos = () => {
    if (!debitos) return 0;
    const federal = debitos.federal.reduce((acc, d) => acc + d.valor, 0);
    const estadual = debitos.estadual.reduce((acc, d) => acc + d.valor, 0);
    const municipal = debitos.municipal.reduce((acc, d) => acc + d.valor, 0);
    const fgts = debitos.fgts.reduce((acc, d) => acc + d.valor, 0);
    const dividaAtiva = debitos.dividaAtiva.reduce((acc, d) => acc + d.valor, 0);
    return federal + estadual + municipal + fgts + dividaAtiva;
  };

  const DebitoTable = ({ titulo, debitos, icon: Icon, color }) => (
    <Card className="mb-4">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg flex items-center gap-2">
          <Icon className={`h-5 w-5 ${color}`} />
          {titulo}
          {debitos.length > 0 && (
            <Badge variant="destructive">{debitos.length}</Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {debitos.length === 0 ? (
          <div className="text-center py-4 text-gray-500">
            <CheckCircle className="h-8 w-8 mx-auto mb-2 text-green-500" />
            <p>Nenhum débito encontrado</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-3 py-2 text-left">Tributo</th>
                  <th className="px-3 py-2 text-left">Competência</th>
                  <th className="px-3 py-2 text-left">Vencimento</th>
                  <th className="px-3 py-2 text-right">Valor</th>
                  <th className="px-3 py-2 text-center">Status</th>
                  <th className="px-3 py-2 text-center">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {debitos.map((debito) => (
                  <tr key={debito.id} className="hover:bg-gray-50">
                    <td className="px-3 py-2 font-medium">{debito.tributo}</td>
                    <td className="px-3 py-2">{debito.competencia || debito.inscricao}</td>
                    <td className="px-3 py-2">{debito.vencimento || debito.dataInscricao}</td>
                    <td className="px-3 py-2 text-right font-semibold">{formatCurrency(debito.valor)}</td>
                    <td className="px-3 py-2 text-center">
                      <Badge className={debito.status === 'vencido' ? 'bg-red-500' : 'bg-yellow-500'}>
                        {debito.status || debito.situacao}
                        {debito.diasAtraso && ` (${debito.diasAtraso}d)`}
                      </Badge>
                    </td>
                    <td className="px-3 py-2 text-center">
                      <Button variant="ghost" size="sm">
                        <FileText className="h-4 w-4" />
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6" data-testid="debitos-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Consulta de Débitos</h1>
        <p className="text-gray-500">Consulte débitos federais, estaduais, municipais, FGTS e dívida ativa</p>
      </div>

      {/* Consulta */}
      <Card>
        <CardContent className="p-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <Select value={selectedEmpresa} onValueChange={setSelectedEmpresa}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione a empresa para consultar" />
                </SelectTrigger>
                <SelectContent>
                  {empresas.map(emp => (
                    <SelectItem key={emp.id} value={emp.id}>
                      <div className="flex items-center gap-2">
                        <Building2 className="h-4 w-4" />
                        {emp.nome} - {emp.cnpj}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button 
              className="bg-blue-900 hover:bg-blue-800"
              onClick={consultarDebitos}
              disabled={!selectedEmpresa || consultando}
            >
              {consultando ? (
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Search className="h-4 w-4 mr-2" />
              )}
              {consultando ? 'Consultando...' : 'Consultar Débitos'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Resultado */}
      {debitos && (
        <>
          {/* Resumo */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card className={`${getSituacaoConfig(debitos.situacao).bgColor} border ${getSituacaoConfig(debitos.situacao).borderColor}`}>
              <CardContent className="p-4 flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Situação Fiscal</p>
                  <p className="text-xl font-bold">{getSituacaoConfig(debitos.situacao).label}</p>
                </div>
                {(() => {
                  const Icon = getSituacaoConfig(debitos.situacao).icon;
                  return <Icon className={`h-8 w-8 ${debitos.situacao === 'regular' ? 'text-green-500' : debitos.situacao === 'pendencias' ? 'text-yellow-500' : 'text-red-500'}`} />;
                })()}
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total em Débitos</p>
                  <p className="text-xl font-bold text-red-600">{formatCurrency(calcularTotalDebitos())}</p>
                </div>
                <DollarSign className="h-8 w-8 text-red-400" />
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Pendências</p>
                  <p className="text-xl font-bold">
                    {debitos.federal.length + debitos.estadual.length + debitos.municipal.length + debitos.fgts.length}
                  </p>
                </div>
                <Clock className="h-8 w-8 text-yellow-400" />
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Dívida Ativa</p>
                  <p className="text-xl font-bold text-purple-600">{debitos.dividaAtiva.length}</p>
                </div>
                <AlertTriangle className="h-8 w-8 text-purple-400" />
              </CardContent>
            </Card>
          </div>

          {/* Detalhes */}
          <Tabs defaultValue="federal" className="space-y-4">
            <TabsList>
              <TabsTrigger value="federal">
                Federal {debitos.federal.length > 0 && <Badge variant="destructive" className="ml-2">{debitos.federal.length}</Badge>}
              </TabsTrigger>
              <TabsTrigger value="estadual">
                Estadual {debitos.estadual.length > 0 && <Badge variant="destructive" className="ml-2">{debitos.estadual.length}</Badge>}
              </TabsTrigger>
              <TabsTrigger value="municipal">
                Municipal {debitos.municipal.length > 0 && <Badge variant="destructive" className="ml-2">{debitos.municipal.length}</Badge>}
              </TabsTrigger>
              <TabsTrigger value="fgts">
                FGTS {debitos.fgts.length > 0 && <Badge variant="destructive" className="ml-2">{debitos.fgts.length}</Badge>}
              </TabsTrigger>
              <TabsTrigger value="divida">
                Dívida Ativa {debitos.dividaAtiva.length > 0 && <Badge variant="destructive" className="ml-2">{debitos.dividaAtiva.length}</Badge>}
              </TabsTrigger>
            </TabsList>

            <TabsContent value="federal">
              <DebitoTable titulo="Débitos Federais" debitos={debitos.federal} icon={Shield} color="text-blue-600" />
            </TabsContent>

            <TabsContent value="estadual">
              <DebitoTable titulo="Débitos Estaduais (ICMS)" debitos={debitos.estadual} icon={Building2} color="text-green-600" />
            </TabsContent>

            <TabsContent value="municipal">
              <DebitoTable titulo="Débitos Municipais (ISS)" debitos={debitos.municipal} icon={Building2} color="text-orange-600" />
            </TabsContent>

            <TabsContent value="fgts">
              <DebitoTable titulo="Débitos FGTS" debitos={debitos.fgts} icon={DollarSign} color="text-cyan-600" />
            </TabsContent>

            <TabsContent value="divida">
              <DebitoTable titulo="Inscrições em Dívida Ativa" debitos={debitos.dividaAtiva} icon={AlertTriangle} color="text-purple-600" />
            </TabsContent>
          </Tabs>

          {/* Ações */}
          <Card>
            <CardContent className="p-4 flex gap-4">
              <Button variant="outline">
                <Download className="h-4 w-4 mr-2" />
                Exportar Relatório
              </Button>
              <Button variant="outline">
                <ExternalLink className="h-4 w-4 mr-2" />
                Acessar e-CAC
              </Button>
              <Button variant="outline">
                <RefreshCw className="h-4 w-4 mr-2" />
                Atualizar Consulta
              </Button>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
};

export default Debitos;
