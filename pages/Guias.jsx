import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
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
  Receipt, 
  Download, 
  Send, 
  Calculator,
  FileText,
  CheckCircle,
  RefreshCw,
  Calendar,
  Building2,
  Printer
} from 'lucide-react';

const Guias = () => {
  const [selectedEmpresa, setSelectedEmpresa] = useState('');
  const [selectedPeriodo, setSelectedPeriodo] = useState('');
  const [selectedRegime, setSelectedRegime] = useState('simples');
  const [novaDataVencimento, setNovaDataVencimento] = useState('');
  const [calculado, setCalculado] = useState(false);
  const [dadosDAS, setDadosDAS] = useState(null);
  const [recalculando, setRecalculando] = useState(false);

  const empresas = [
    { id: 'e1', nome: 'TRES PINHEIROS COMERCIO LTDA', regime: 'simples', cnpj: '12.345.678/0001-90' },
    { id: 'e2', nome: 'SUPER GALO RESTAURANTE LTDA', regime: 'simples', cnpj: '98.765.432/0001-10' },
    { id: 'e3', nome: 'MAFE RESTAURANTE EIRELI', regime: 'simples', cnpj: '11.222.333/0001-44' },
    { id: 'e4', nome: 'COMERCIO DIGITAL MEI', regime: 'mei', cnpj: '99.888.777/0001-66' },
    { id: 'e5', nome: 'JOAO SILVA MEI', regime: 'mei', cnpj: '88.777.666/0001-55' },
  ];

  const periodos = [
    '01/2025', '02/2025', '03/2025',
    '12/2024', '11/2024', '10/2024'
  ];

  // Tabelas do Simples Nacional
  const tabelasSimples = {
    'I': { nome: 'Comércio', aliquotaInicial: 4.0, deducao: 0 },
    'II': { nome: 'Indústria', aliquotaInicial: 4.5, deducao: 0 },
    'III': { nome: 'Serviços (locacao, cessão)', aliquotaInicial: 6.0, deducao: 0 },
    'IV': { nome: 'Serviços (construção)', aliquotaInicial: 4.5, deducao: 0 },
    'V': { nome: 'Serviços (profissionais)', aliquotaInicial: 15.5, deducao: 0 }
  };

  // Valores fixos MEI 2025
  const valoresMEI = {
    inss: 75.90, // 5% do salário mínimo (R$ 1.518,00)
    icms: 1.00,
    iss: 5.00
  };

  const guiasGeradas = [
    { id: 1, empresa: 'TRES PINHEIROS', tipo: 'DAS', regime: 'simples', competencia: '12/2024', valor: 4200, vencimento: '20/01/2025', status: 'pago' },
    { id: 2, empresa: 'SUPER GALO', tipo: 'DAS', regime: 'simples', competencia: '12/2024', valor: 8500, vencimento: '20/01/2025', status: 'pago' },
    { id: 3, empresa: 'TRES PINHEIROS', tipo: 'DAS', regime: 'simples', competencia: '01/2025', valor: 4500, vencimento: '20/02/2025', status: 'pendente' },
    { id: 4, empresa: 'COMERCIO DIGITAL', tipo: 'DAS-MEI', regime: 'mei', competencia: '01/2025', valor: 76.90, vencimento: '20/02/2025', status: 'pendente' },
    { id: 5, empresa: 'JOAO SILVA', tipo: 'DAS-MEI', regime: 'mei', competencia: '01/2025', valor: 81.90, vencimento: '20/02/2025', status: 'pendente' },
  ];

  const calcularDAS = () => {
    if (!selectedEmpresa || !selectedPeriodo) return;
    
    const empresa = empresas.find(e => e.id === selectedEmpresa);
    const isMEI = empresa?.regime === 'mei';
    
    if (isMEI) {
      // Cálculo MEI
      const atividade = Math.random() > 0.5 ? 'comercio' : 'servicos';
      let valor = valoresMEI.inss;
      if (atividade === 'comercio') valor += valoresMEI.icms;
      if (atividade === 'servicos') valor += valoresMEI.iss;
      
      setDadosDAS({
        tipo: 'DAS-MEI',
        regime: 'MEI',
        inss: valoresMEI.inss,
        icms: atividade === 'comercio' ? valoresMEI.icms : 0,
        iss: atividade === 'servicos' ? valoresMEI.iss : 0,
        valor,
        atividade: atividade === 'comercio' ? 'Comércio/Indústria' : 'Serviços',
        vencimento: `20/${selectedPeriodo.split('/')[0]}/2025`,
        competencia: selectedPeriodo
      });
    } else {
      // Cálculo Simples Nacional
      const receitaBruta = Math.random() * 100000 + 50000;
      const anexo = ['I', 'II', 'III', 'IV', 'V'][Math.floor(Math.random() * 5)];
      const tabela = tabelasSimples[anexo];
      const fatorR = 15 + Math.random() * 20;
      
      // Cálculo simplificado da alíquota efetiva
      let aliquotaEfetiva = tabela.aliquotaInicial + (receitaBruta / 1000000) * 2;
      if (anexo === 'V' && fatorR >= 28) {
        aliquotaEfetiva = 15.5; // Fator R >= 28% vai para anexo III
      }
      
      const valor = receitaBruta * (aliquotaEfetiva / 100);
      
      setDadosDAS({
        tipo: 'DAS',
        regime: 'Simples Nacional',
        receitaBruta,
        anexo,
        nomeAnexo: tabela.nome,
        aliquotaEfetiva,
        fatorR,
        valor,
        vencimento: `20/${selectedPeriodo.split('/')[0]}/2025`,
        competencia: selectedPeriodo
      });
    }
    setCalculado(true);
  };

  const recalcularDAS = () => {
    if (!novaDataVencimento || !dadosDAS) return;
    
    setRecalculando(true);
    
    // Simular recálculo com juros e multa
    setTimeout(() => {
      const diasAtraso = Math.floor(Math.random() * 30) + 1;
      const multa = dadosDAS.valor * 0.0033 * diasAtraso; // 0.33% ao dia até 20%
      const juros = dadosDAS.valor * 0.01 * Math.ceil(diasAtraso / 30); // 1% ao mês (SELIC)
      
      setDadosDAS({
        ...dadosDAS,
        vencimentoOriginal: dadosDAS.vencimento,
        vencimento: novaDataVencimento,
        diasAtraso,
        multa: Math.min(multa, dadosDAS.valor * 0.2), // Máx 20%
        juros,
        valorAtualizado: dadosDAS.valor + Math.min(multa, dadosDAS.valor * 0.2) + juros,
        recalculado: true
      });
      setRecalculando(false);
    }, 1000);
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
  };

  const empresasFiltradas = selectedRegime === 'todos' 
    ? empresas 
    : empresas.filter(e => e.regime === selectedRegime);

  return (
    <div className="space-y-6" data-testid="guias-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">DAS / Guias</h1>
        <p className="text-gray-500">Emissão de guias de pagamento - Simples Nacional e MEI</p>
      </div>

      <Tabs defaultValue="calcular" className="space-y-6">
        <TabsList>
          <TabsTrigger value="calcular"><Calculator className="h-4 w-4 mr-2" /> Calcular DAS</TabsTrigger>
          <TabsTrigger value="recalcular"><RefreshCw className="h-4 w-4 mr-2" /> Recalcular</TabsTrigger>
          <TabsTrigger value="historico"><Receipt className="h-4 w-4 mr-2" /> Histórico</TabsTrigger>
        </TabsList>

        {/* Calcular DAS */}
        <TabsContent value="calcular">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calculator className="h-5 w-5" />
                  Calcular DAS
                </CardTitle>
                <CardDescription>Simples Nacional ou MEI</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Regime Tributário</Label>
                  <Select value={selectedRegime} onValueChange={(v) => { setSelectedRegime(v); setSelectedEmpresa(''); setCalculado(false); }}>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o regime" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="todos">Todos</SelectItem>
                      <SelectItem value="simples">Simples Nacional</SelectItem>
                      <SelectItem value="mei">MEI</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>Empresa</Label>
                  <Select value={selectedEmpresa} onValueChange={(v) => { setSelectedEmpresa(v); setCalculado(false); }}>
                    <SelectTrigger data-testid="empresa-select">
                      <SelectValue placeholder="Selecione a empresa" />
                    </SelectTrigger>
                    <SelectContent>
                      {empresasFiltradas.map(emp => (
                        <SelectItem key={emp.id} value={emp.id}>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className={emp.regime === 'mei' ? 'bg-yellow-100' : 'bg-green-100'}>
                              {emp.regime.toUpperCase()}
                            </Badge>
                            {emp.nome}
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>Período (Competência)</Label>
                  <Select value={selectedPeriodo} onValueChange={(v) => { setSelectedPeriodo(v); setCalculado(false); }}>
                    <SelectTrigger data-testid="periodo-select">
                      <SelectValue placeholder="Selecione o período" />
                    </SelectTrigger>
                    <SelectContent>
                      {periodos.map(p => (
                        <SelectItem key={p} value={p}>{p}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <Button 
                  className="w-full bg-blue-900 hover:bg-blue-800"
                  onClick={calcularDAS}
                  disabled={!selectedEmpresa || !selectedPeriodo}
                  data-testid="calcular-button"
                >
                  <Calculator className="h-4 w-4 mr-2" />
                  Calcular DAS
                </Button>
              </CardContent>
            </Card>

            {/* Resultado */}
            {calculado && dadosDAS && (
              <Card className="border-2 border-blue-200">
                <CardHeader className={dadosDAS.regime === 'MEI' ? 'bg-yellow-50' : 'bg-green-50'}>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center gap-2">
                      <FileText className="h-5 w-5" />
                      {dadosDAS.tipo}
                    </span>
                    <Badge className={dadosDAS.regime === 'MEI' ? 'bg-yellow-500' : 'bg-green-500'}>
                      {dadosDAS.regime}
                    </Badge>
                  </CardTitle>
                  <CardDescription>Competência: {dadosDAS.competencia}</CardDescription>
                </CardHeader>
                <CardContent className="pt-6 space-y-4">
                  {dadosDAS.regime === 'MEI' ? (
                    // Resultado MEI
                    <div className="space-y-3">
                      <div className="grid grid-cols-2 gap-3 text-sm">
                        <div className="p-3 bg-gray-50 rounded">
                          <p className="text-gray-500">INSS (5% SM)</p>
                          <p className="font-semibold">{formatCurrency(dadosDAS.inss)}</p>
                        </div>
                        <div className="p-3 bg-gray-50 rounded">
                          <p className="text-gray-500">Atividade</p>
                          <p className="font-semibold">{dadosDAS.atividade}</p>
                        </div>
                        {dadosDAS.icms > 0 && (
                          <div className="p-3 bg-gray-50 rounded">
                            <p className="text-gray-500">ICMS</p>
                            <p className="font-semibold">{formatCurrency(dadosDAS.icms)}</p>
                          </div>
                        )}
                        {dadosDAS.iss > 0 && (
                          <div className="p-3 bg-gray-50 rounded">
                            <p className="text-gray-500">ISS</p>
                            <p className="font-semibold">{formatCurrency(dadosDAS.iss)}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  ) : (
                    // Resultado Simples Nacional
                    <div className="space-y-3">
                      <div className="grid grid-cols-2 gap-3 text-sm">
                        <div className="p-3 bg-gray-50 rounded">
                          <p className="text-gray-500">Receita Bruta</p>
                          <p className="font-semibold">{formatCurrency(dadosDAS.receitaBruta)}</p>
                        </div>
                        <div className="p-3 bg-gray-50 rounded">
                          <p className="text-gray-500">Anexo</p>
                          <p className="font-semibold">{dadosDAS.anexo} - {dadosDAS.nomeAnexo}</p>
                        </div>
                        <div className="p-3 bg-gray-50 rounded">
                          <p className="text-gray-500">Alíquota Efetiva</p>
                          <p className="font-semibold">{dadosDAS.aliquotaEfetiva.toFixed(2)}%</p>
                        </div>
                        <div className="p-3 bg-gray-50 rounded">
                          <p className="text-gray-500">Fator R</p>
                          <p className="font-semibold">{dadosDAS.fatorR.toFixed(2)}%</p>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="pt-4 border-t">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-gray-700">Valor do {dadosDAS.tipo}</span>
                      <span className="text-3xl font-bold text-blue-900">{formatCurrency(dadosDAS.valor)}</span>
                    </div>
                    <p className="text-sm text-gray-500">
                      <Calendar className="h-4 w-4 inline mr-1" />
                      Vencimento: {dadosDAS.vencimento}
                    </p>
                  </div>

                  <div className="flex gap-2 pt-4">
                    <Button className="flex-1 bg-green-600 hover:bg-green-700">
                      <FileText className="h-4 w-4 mr-2" />
                      Gerar {dadosDAS.tipo}
                    </Button>
                    <Button variant="outline">
                      <Printer className="h-4 w-4 mr-2" />
                      Imprimir
                    </Button>
                    <Button variant="outline">
                      <Send className="h-4 w-4 mr-2" />
                      Email
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>

        {/* Recalcular DAS */}
        <TabsContent value="recalcular">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <RefreshCw className="h-5 w-5" />
                  Recalcular DAS
                </CardTitle>
                <CardDescription>Recalcule com nova data de vencimento (juros e multa)</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-sm">
                  <p className="font-medium text-yellow-800">Primeiro calcule o DAS original</p>
                  <p className="text-yellow-700">Use a aba "Calcular DAS" para gerar o valor original, depois retorne aqui para recalcular.</p>
                </div>

                {calculado && dadosDAS && (
                  <>
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-500">DAS Original</p>
                      <p className="font-semibold">{formatCurrency(dadosDAS.valor)}</p>
                      <p className="text-sm text-gray-500">Vencimento: {dadosDAS.vencimentoOriginal || dadosDAS.vencimento}</p>
                    </div>

                    <div>
                      <Label>Nova Data de Vencimento</Label>
                      <Input 
                        type="date" 
                        value={novaDataVencimento}
                        onChange={(e) => setNovaDataVencimento(e.target.value)}
                      />
                    </div>

                    <Button 
                      className="w-full bg-orange-600 hover:bg-orange-700"
                      onClick={recalcularDAS}
                      disabled={!novaDataVencimento || recalculando}
                    >
                      <RefreshCw className={`h-4 w-4 mr-2 ${recalculando ? 'animate-spin' : ''}`} />
                      {recalculando ? 'Recalculando...' : 'Recalcular com Juros e Multa'}
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>

            {/* Resultado Recalculado */}
            {dadosDAS?.recalculado && (
              <Card className="border-2 border-orange-200">
                <CardHeader className="bg-orange-50">
                  <CardTitle className="flex items-center gap-2 text-orange-700">
                    <RefreshCw className="h-5 w-5" />
                    DAS Recalculado
                  </CardTitle>
                  <CardDescription>Com juros e multa por atraso</CardDescription>
                </CardHeader>
                <CardContent className="pt-6 space-y-4">
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="p-3 bg-gray-50 rounded">
                      <p className="text-gray-500">Valor Original</p>
                      <p className="font-semibold">{formatCurrency(dadosDAS.valor)}</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded">
                      <p className="text-gray-500">Dias em Atraso</p>
                      <p className="font-semibold text-red-600">{dadosDAS.diasAtraso} dias</p>
                    </div>
                    <div className="p-3 bg-red-50 rounded">
                      <p className="text-gray-500">Multa (0,33%/dia)</p>
                      <p className="font-semibold text-red-600">+ {formatCurrency(dadosDAS.multa)}</p>
                    </div>
                    <div className="p-3 bg-red-50 rounded">
                      <p className="text-gray-500">Juros (SELIC)</p>
                      <p className="font-semibold text-red-600">+ {formatCurrency(dadosDAS.juros)}</p>
                    </div>
                  </div>

                  <div className="pt-4 border-t">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-gray-700">Valor Atualizado</span>
                      <span className="text-3xl font-bold text-orange-600">{formatCurrency(dadosDAS.valorAtualizado)}</span>
                    </div>
                    <p className="text-sm text-gray-500">
                      <Calendar className="h-4 w-4 inline mr-1" />
                      Novo Vencimento: {dadosDAS.vencimento}
                    </p>
                  </div>

                  <div className="flex gap-2 pt-4">
                    <Button className="flex-1 bg-orange-600 hover:bg-orange-700">
                      <FileText className="h-4 w-4 mr-2" />
                      Gerar DAS Atualizado
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>

        {/* Histórico */}
        <TabsContent value="historico">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Receipt className="h-5 w-5" />
                Guias Geradas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empresa</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Regime</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Competência</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Valor</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vencimento</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ações</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    {guiasGeradas.map((guia) => (
                      <tr key={guia.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2">
                            <Building2 className="h-4 w-4 text-gray-400" />
                            <span className="font-medium">{guia.empresa}</span>
                          </div>
                        </td>
                        <td className="px-4 py-3">{guia.tipo}</td>
                        <td className="px-4 py-3">
                          <Badge className={guia.regime === 'mei' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}>
                            {guia.regime.toUpperCase()}
                          </Badge>
                        </td>
                        <td className="px-4 py-3">{guia.competencia}</td>
                        <td className="px-4 py-3 font-semibold">{formatCurrency(guia.valor)}</td>
                        <td className="px-4 py-3">{guia.vencimento}</td>
                        <td className="px-4 py-3">
                          <Badge className={guia.status === 'pago' ? 'bg-green-500' : 'bg-yellow-500'}>
                            {guia.status === 'pago' ? <CheckCircle className="h-3 w-3 mr-1" /> : null}
                            {guia.status}
                          </Badge>
                        </td>
                        <td className="px-4 py-3">
                          <Button variant="ghost" size="sm">
                            <Download className="h-4 w-4" />
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Guias;
