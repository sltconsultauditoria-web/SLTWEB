import { useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Calculator, 
  TrendingUp, 
  FileText, 
  RefreshCw,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Loader2,
  DollarSign,
  Percent,
  Building2,
  Shield
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Fiscal = () => {
  const [activeTab, setActiveTab] = useState('simples');
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);

  // Simples Nacional State
  const [simplesData, setSimplesData] = useState({
    cnpj: '12.345.678/0001-00',
    periodo: '2025-12',
    receita_bruta_12m: 300000,
    receita_mensal: 30000,
    anexo: 'anexo_iii'
  });

  // Fator R State
  const [fatorRData, setFatorRData] = useState({
    cnpj: '12.345.678/0001-00',
    periodo: '2025-12',
    folha_salarios_12m: 80000,
    receita_bruta_12m: 250000
  });

  // e-CAC State
  const [cnpjEcac, setCnpjEcac] = useState('12345678000100');
  const [dadosEcac, setDadosEcac] = useState(null);

  const handleCalcularSimples = async () => {
    setLoading(true);
    setResultado(null);
    try {
      const response = await axios.post(`${API}/fiscal/calcular/simples-nacional`, simplesData);
      setResultado(response.data);
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao calcular: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleCalcularFatorR = async () => {
    setLoading(true);
    setResultado(null);
    try {
      const response = await axios.post(`${API}/fiscal/calcular/fator-r`, fatorRData);
      setResultado(response.data);
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao calcular: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleConsultarCertidoes = async () => {
    setLoading(true);
    setDadosEcac(null);
    try {
      const response = await axios.get(`${API}/fiscal/ecac/certidoes/${cnpjEcac.replace(/\D/g, '')}`);
      setDadosEcac(response.data);
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro na consulta: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleConsultarPendencias = async () => {
    setLoading(true);
    setDadosEcac(null);
    try {
      const response = await axios.get(`${API}/fiscal/ecac/pendencias/${cnpjEcac.replace(/\D/g, '')}`);
      setDadosEcac(response.data);
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro na consulta: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  return (
    <div className="space-y-6" data-testid="fiscal-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Calculator className="h-7 w-7 text-blue-600" />
          Módulo Fiscal (IRIS)
        </h1>
        <p className="text-gray-500">Cálculos de Simples Nacional, Fator R e Integração e-CAC</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="simples" data-testid="tab-simples">
            <DollarSign className="h-4 w-4 mr-2" />
            Simples Nacional
          </TabsTrigger>
          <TabsTrigger value="fator_r" data-testid="tab-fator-r">
            <Percent className="h-4 w-4 mr-2" />
            Fator R
          </TabsTrigger>
          <TabsTrigger value="ecac" data-testid="tab-ecac">
            <Shield className="h-4 w-4 mr-2" />
            e-CAC
          </TabsTrigger>
        </TabsList>

        {/* Simples Nacional */}
        <TabsContent value="simples" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-green-600" />
                Cálculo do DAS (Simples Nacional)
              </CardTitle>
              <CardDescription>
                Calcula o valor do DAS com base nas tabelas atualizadas da LC 123/2006
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="cnpj-simples">CNPJ</Label>
                  <Input
                    id="cnpj-simples"
                    value={simplesData.cnpj}
                    onChange={(e) => setSimplesData({...simplesData, cnpj: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="periodo-simples">Período (YYYY-MM)</Label>
                  <Input
                    id="periodo-simples"
                    value={simplesData.periodo}
                    onChange={(e) => setSimplesData({...simplesData, periodo: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="rbt12">Receita Bruta 12 Meses (R$)</Label>
                  <Input
                    id="rbt12"
                    type="number"
                    value={simplesData.receita_bruta_12m}
                    onChange={(e) => setSimplesData({...simplesData, receita_bruta_12m: parseFloat(e.target.value)})}
                  />
                </div>
                <div>
                  <Label htmlFor="receita-mensal">Receita Mensal (R$)</Label>
                  <Input
                    id="receita-mensal"
                    type="number"
                    value={simplesData.receita_mensal}
                    onChange={(e) => setSimplesData({...simplesData, receita_mensal: parseFloat(e.target.value)})}
                  />
                </div>
                <div>
                  <Label htmlFor="anexo">Anexo</Label>
                  <select
                    id="anexo"
                    className="w-full p-2 border rounded-md"
                    value={simplesData.anexo}
                    onChange={(e) => setSimplesData({...simplesData, anexo: e.target.value})}
                  >
                    <option value="anexo_i">Anexo I - Comércio</option>
                    <option value="anexo_ii">Anexo II - Indústria</option>
                    <option value="anexo_iii">Anexo III - Serviços (Fator R ≥ 28%)</option>
                    <option value="anexo_iv">Anexo IV - Serviços Específicos</option>
                    <option value="anexo_v">Anexo V - Serviços (Fator R menor que 28%)</option>
                  </select>
                </div>
              </div>
              
              <Button 
                onClick={handleCalcularSimples} 
                disabled={loading}
                className="w-full md:w-auto"
                data-testid="btn-calcular-simples"
              >
                {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Calculator className="h-4 w-4 mr-2" />}
                Calcular DAS
              </Button>

              {resultado && resultado.status === 'SUCESSO' && (
                <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-3">Resultado do Cálculo</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-white rounded-lg">
                      <p className="text-sm text-gray-500">Anexo</p>
                      <p className="text-xl font-bold text-blue-600">{resultado.anexo?.toUpperCase().replace('_', ' ')}</p>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg">
                      <p className="text-sm text-gray-500">Alíquota Efetiva</p>
                      <p className="text-xl font-bold text-blue-600">{resultado.aliquota_efetiva?.toFixed(2)}%</p>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg">
                      <p className="text-sm text-gray-500">Valor do DAS</p>
                      <p className="text-xl font-bold text-green-600">{formatCurrency(resultado.valor_das)}</p>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg">
                      <p className="text-sm text-gray-500">Sublimite</p>
                      <Badge className={resultado.excede_sublimite_estadual ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}>
                        {resultado.excede_sublimite_estadual ? 'Excedido' : 'OK'}
                      </Badge>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Fator R */}
        <TabsContent value="fator_r" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-purple-600" />
                Cálculo do Fator R
              </CardTitle>
              <CardDescription>
                Determina o enquadramento no Anexo III ou V baseado na relação Folha/Receita
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="cnpj-fator">CNPJ</Label>
                  <Input
                    id="cnpj-fator"
                    value={fatorRData.cnpj}
                    onChange={(e) => setFatorRData({...fatorRData, cnpj: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="periodo-fator">Período (YYYY-MM)</Label>
                  <Input
                    id="periodo-fator"
                    value={fatorRData.periodo}
                    onChange={(e) => setFatorRData({...fatorRData, periodo: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="folha">Folha de Salários 12M (R$)</Label>
                  <Input
                    id="folha"
                    type="number"
                    value={fatorRData.folha_salarios_12m}
                    onChange={(e) => setFatorRData({...fatorRData, folha_salarios_12m: parseFloat(e.target.value)})}
                  />
                </div>
                <div>
                  <Label htmlFor="rbt12-fator">Receita Bruta 12M (R$)</Label>
                  <Input
                    id="rbt12-fator"
                    type="number"
                    value={fatorRData.receita_bruta_12m}
                    onChange={(e) => setFatorRData({...fatorRData, receita_bruta_12m: parseFloat(e.target.value)})}
                  />
                </div>
              </div>
              
              <Button 
                onClick={handleCalcularFatorR} 
                disabled={loading}
                className="w-full md:w-auto bg-purple-600 hover:bg-purple-700"
                data-testid="btn-calcular-fator-r"
              >
                {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Percent className="h-4 w-4 mr-2" />}
                Calcular Fator R
              </Button>

              {resultado && resultado.status === 'SUCESSO' && resultado.fator_r !== undefined && (
                <div className={`mt-6 p-4 border rounded-lg ${resultado.beneficia_anexo_iii ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'}`}>
                  <h4 className={`font-semibold mb-3 ${resultado.beneficia_anexo_iii ? 'text-green-800' : 'text-yellow-800'}`}>
                    Resultado do Cálculo
                  </h4>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="text-center p-3 bg-white rounded-lg">
                      <p className="text-sm text-gray-500">Fator R</p>
                      <p className="text-2xl font-bold text-purple-600">{resultado.fator_r_percentual?.toFixed(2)}%</p>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg">
                      <p className="text-sm text-gray-500">Enquadramento</p>
                      <p className="text-xl font-bold text-blue-600">{resultado.enquadramento?.replace('_', ' ')}</p>
                    </div>
                    <div className="text-center p-3 bg-white rounded-lg col-span-2 md:col-span-1">
                      <p className="text-sm text-gray-500">Status</p>
                      <Badge className={resultado.beneficia_anexo_iii ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                        {resultado.beneficia_anexo_iii ? '✅ Alíquotas Reduzidas' : '⚠️ Alíquotas Majoradas'}
                      </Badge>
                    </div>
                  </div>
                  <p className="mt-4 text-sm text-gray-600">{resultado.descricao}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* e-CAC */}
        <TabsContent value="ecac" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5 text-orange-600" />
                Integração e-CAC (Simulação)
              </CardTitle>
              <CardDescription>
                Consulta de certidões e pendências fiscais via e-CAC
                <Badge className="ml-2 bg-yellow-100 text-yellow-800">MOCK/SIMULAÇÃO</Badge>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-4 items-end">
                <div className="flex-1">
                  <Label htmlFor="cnpj-ecac">CNPJ</Label>
                  <Input
                    id="cnpj-ecac"
                    value={cnpjEcac}
                    onChange={(e) => setCnpjEcac(e.target.value)}
                    placeholder="00.000.000/0000-00"
                  />
                </div>
                <Button 
                  onClick={handleConsultarCertidoes} 
                  disabled={loading}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4 mr-2" />}
                  Certidões
                </Button>
                <Button 
                  onClick={handleConsultarPendencias} 
                  disabled={loading}
                  variant="outline"
                >
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <AlertTriangle className="h-4 w-4 mr-2" />}
                  Pendências
                </Button>
              </div>

              {dadosEcac && dadosEcac.certidoes && (
                <div className="mt-6 space-y-3">
                  <h4 className="font-semibold text-gray-800">Certidões</h4>
                  {dadosEcac.certidoes.map((cert, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        {cert.status === 'Válida' ? (
                          <CheckCircle className="h-5 w-5 text-green-600" />
                        ) : cert.status === 'Vencida' ? (
                          <XCircle className="h-5 w-5 text-red-600" />
                        ) : (
                          <AlertTriangle className="h-5 w-5 text-yellow-600" />
                        )}
                        <div>
                          <p className="font-medium text-gray-900">{cert.tipo}</p>
                          {cert.data_validade && (
                            <p className="text-sm text-gray-500">
                              Validade: {new Date(cert.data_validade).toLocaleDateString('pt-BR')}
                            </p>
                          )}
                        </div>
                      </div>
                      <Badge className={
                        cert.status === 'Válida' ? 'bg-green-100 text-green-800' :
                        cert.status === 'Vencida' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }>
                        {cert.status}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}

              {dadosEcac && dadosEcac.score_risco !== undefined && (
                <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-semibold text-gray-800 mb-3">Pendências Fiscais</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className={`p-3 rounded-lg ${dadosEcac.malha_fiscal ? 'bg-red-100' : 'bg-green-100'}`}>
                      <p className="text-sm text-gray-600">Malha Fiscal</p>
                      <p className="font-bold">{dadosEcac.malha_fiscal ? 'SIM' : 'NÃO'}</p>
                    </div>
                    <div className={`p-3 rounded-lg ${dadosEcac.divida_ativa ? 'bg-red-100' : 'bg-green-100'}`}>
                      <p className="text-sm text-gray-600">Dívida Ativa</p>
                      <p className="font-bold">{dadosEcac.divida_ativa ? 'SIM' : 'NÃO'}</p>
                    </div>
                    <div className={`p-3 rounded-lg ${dadosEcac.pendencias_cadin ? 'bg-red-100' : 'bg-green-100'}`}>
                      <p className="text-sm text-gray-600">CADIN</p>
                      <p className="font-bold">{dadosEcac.pendencias_cadin ? 'SIM' : 'NÃO'}</p>
                    </div>
                    <div className={`p-3 rounded-lg bg-gray-100`}>
                      <p className="text-sm text-gray-600">Mensagens</p>
                      <p className="font-bold">{dadosEcac.caixa_postal_mensagens}</p>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center justify-between p-3 bg-white rounded-lg">
                    <span className="font-medium">Score de Risco:</span>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl font-bold">{dadosEcac.score_risco}%</span>
                      <Badge className={
                        dadosEcac.nivel_risco === 'CRÍTICO' ? 'bg-red-600 text-white' :
                        dadosEcac.nivel_risco === 'ALTO' ? 'bg-orange-500 text-white' :
                        dadosEcac.nivel_risco === 'MÉDIO' ? 'bg-yellow-500 text-white' :
                        'bg-green-500 text-white'
                      }>
                        {dadosEcac.nivel_risco}
                      </Badge>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Fiscal;
