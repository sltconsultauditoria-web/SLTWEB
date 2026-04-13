import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
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
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  FileCheck, 
  Download, 
  RefreshCw,
  Calendar,
  Building2,
  Plus,
  AlertTriangle,
  CheckCircle,
  Clock,
  ExternalLink,
  Search,
  Bell
} from 'lucide-react';

const Certidoes = () => {
  const [certidoes, setCertidoes] = useState([
    { id: 1, empresa: 'TRES PINHEIROS', cnpj: '12.345.678/0001-90', tipo: 'CND Federal', dataEmissao: '2024-12-01', dataValidade: '2025-05-30', situacao: 'regular', arquivo: 'cnd_federal_tres_pinheiros.pdf' },
    { id: 2, empresa: 'TRES PINHEIROS', cnpj: '12.345.678/0001-90', tipo: 'CRF FGTS', dataEmissao: '2024-12-10', dataValidade: '2025-01-09', situacao: 'regular', arquivo: 'crf_fgts_tres_pinheiros.pdf' },
    { id: 3, empresa: 'TRES PINHEIROS', cnpj: '12.345.678/0001-90', tipo: 'CND Estadual', dataEmissao: '2024-11-15', dataValidade: '2025-02-15', situacao: 'regular', arquivo: 'cnd_estadual_tres_pinheiros.pdf' },
    { id: 4, empresa: 'SUPER GALO', cnpj: '98.765.432/0001-10', tipo: 'CND Federal', dataEmissao: '2024-11-20', dataValidade: '2025-05-19', situacao: 'regular', arquivo: 'cnd_federal_super_galo.pdf' },
    { id: 5, empresa: 'SUPER GALO', cnpj: '98.765.432/0001-10', tipo: 'CRF FGTS', dataEmissao: '2024-10-05', dataValidade: '2024-12-04', situacao: 'vencida', arquivo: null },
    { id: 6, empresa: 'MAFE REST.', cnpj: '11.222.333/0001-44', tipo: 'CND Federal', dataEmissao: '2024-12-15', dataValidade: '2025-06-14', situacao: 'regular', arquivo: 'cnd_federal_mafe.pdf' },
    { id: 7, empresa: 'MAFE REST.', cnpj: '11.222.333/0001-44', tipo: 'CND Municipal', dataEmissao: '2024-09-01', dataValidade: '2024-12-01', situacao: 'vencida', arquivo: null },
    { id: 8, empresa: 'TECH SOLUTIONS', cnpj: '55.666.777/0001-88', tipo: 'CNDT Trabalhista', dataEmissao: '2024-12-10', dataValidade: '2025-06-09', situacao: 'regular', arquivo: 'cndt_tech.pdf' },
  ]);

  const [consultando, setConsultando] = useState(API.get('/replace_with_real_endpoint'));
  const [filtroEmpresa, setFiltroEmpresa] = useState('todas');
  const [filtroSituacao, setFiltroSituacao] = useState('todas');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const tiposCertidao = [
    { id: 'cnd_federal', nome: 'CND Federal (União)', url: 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Emitir' },
    { id: 'crf_fgts', nome: 'CRF FGTS', url: 'https://consulta-crf.caixa.gov.br/' },
    { id: 'cnd_estadual', nome: 'CND Estadual (ICMS)', url: null },
    { id: 'cnd_municipal', nome: 'CND Municipal (ISS)', url: null },
    { id: 'cndt', nome: 'CNDT Trabalhista', url: 'https://www.tst.jus.br/certidao' },
    { id: 'inss', nome: 'CND INSS', url: 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Emitir' },
  ];

  const empresas = ['TRES PINHEIROS', 'SUPER GALO', 'MAFE REST.', 'TECH SOLUTIONS'];

  const getDiasParaVencer = (dataValidade) => {
    const hoje = new Date();
    const validade = new Date(dataValidade);
    const diff = Math.ceil((validade - hoje) / (1000 * 60 * 60 * 24));
    return diff;
  };

  const getSituacaoConfig = (situacao, dataValidade) => {
    const dias = getDiasParaVencer(dataValidade);
    
    if (situacao === 'vencida' || dias < 0) {
      return { color: 'bg-red-500', icon: AlertTriangle, label: 'Vencida', textColor: 'text-red-700' };
    }
    if (dias <= 15) {
      return { color: 'bg-yellow-500', icon: Clock, label: 'Expirando', textColor: 'text-yellow-700' };
    }
    if (dias <= 30) {
      return { color: 'bg-orange-500', icon: Clock, label: 'Atenção', textColor: 'text-orange-700' };
    }
    return { color: 'bg-green-500', icon: CheckCircle, label: 'Válida', textColor: 'text-green-700' };
  };

  const consultarCertidao = async (certidaoId, tipo) => {
    setConsultando({ ...consultando, [certidaoId]: true });
    
    // Simular consulta
    setTimeout(() => {
      setCertidoes(certidoes.map(c => {
        if (c.id === certidaoId) {
          return {
            ...c,
            dataEmissao: new Date().toISOString().split('T')[0],
            dataValidade: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            situacao: 'regular',
            arquivo: `${tipo.toLowerCase().replace(/\s/g, '_')}_${c.empresa.toLowerCase().replace(/\s/g, '_')}.pdf`
          };
        }
        return c;
      }));
      setConsultando({ ...consultando, [certidaoId]: false });
    }, 2000);
  };

  const consultarTodasCertidoes = async (empresa) => {
    const certidoesDaEmpresa = certidoes.filter(c => c.empresa === empresa);
    for (const cert of certidoesDaEmpresa) {
      await consultarCertidao(cert.id, cert.tipo);
    }
  };

  const filteredCertidoes = certidoes.filter(c => {
    if (filtroEmpresa !== 'todas' && c.empresa !== filtroEmpresa) return false;
    if (filtroSituacao !== 'todas') {
      const config = getSituacaoConfig(c.situacao, c.dataValidade);
      if (filtroSituacao === 'vencidas' && config.label !== 'Vencida') return false;
      if (filtroSituacao === 'expirando' && config.label !== 'Expirando' && config.label !== 'Atenção') return false;
      if (filtroSituacao === 'validas' && config.label !== 'Válida') return false;
    }
    return true;
  });

  const stats = {
    total: certidoes.length,
    validas: certidoes.filter(c => getSituacaoConfig(c.situacao, c.dataValidade).label === 'Válida').length,
    expirando: certidoes.filter(c => ['Expirando', 'Atenção'].includes(getSituacaoConfig(c.situacao, c.dataValidade).label)).length,
    vencidas: certidoes.filter(c => getSituacaoConfig(c.situacao, c.dataValidade).label === 'Vencida').length,
  };

  return (
    <div className="space-y-6" data-testid="certidoes-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestor de Certidões</h1>
          <p className="text-gray-500">Consulta e download automático de CNDs</p>
        </div>
        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
          <DialogTrigger asChild>
            <Button className="bg-blue-900 hover:bg-blue-800">
              <Plus className="h-4 w-4 mr-2" />
              Nova Certidão
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Consultar Nova Certidão</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label>Empresa</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione a empresa" />
                  </SelectTrigger>
                  <SelectContent>
                    {empresas.map(emp => (
                      <SelectItem key={emp} value={emp}>{emp}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Tipo de Certidão</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {tiposCertidao.map(tipo => (
                      <SelectItem key={tipo.id} value={tipo.id}>{tipo.nome}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <Button className="w-full bg-blue-900 hover:bg-blue-800">
                <Search className="h-4 w-4 mr-2" />
                Consultar
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total</p>
              <p className="text-2xl font-bold">{stats.total}</p>
            </div>
            <FileCheck className="h-8 w-8 text-blue-400" />
          </CardContent>
        </Card>
        <Card className="bg-green-50 border-green-200">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600">Válidas</p>
              <p className="text-2xl font-bold text-green-700">{stats.validas}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-500" />
          </CardContent>
        </Card>
        <Card className="bg-yellow-50 border-yellow-200">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-yellow-600">Expirando</p>
              <p className="text-2xl font-bold text-yellow-700">{stats.expirando}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-500" />
          </CardContent>
        </Card>
        <Card className="bg-red-50 border-red-200">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-red-600">Vencidas</p>
              <p className="text-2xl font-bold text-red-700">{stats.vencidas}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-red-500" />
          </CardContent>
        </Card>
      </div>

      {/* Filtros */}
      <Card>
        <CardContent className="p-4 flex gap-4">
          <div className="flex-1">
            <Select value={filtroEmpresa} onValueChange={setFiltroEmpresa}>
              <SelectTrigger>
                <SelectValue placeholder="Filtrar por empresa" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="todas">Todas as empresas</SelectItem>
                {empresas.map(emp => (
                  <SelectItem key={emp} value={emp}>{emp}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex-1">
            <Select value={filtroSituacao} onValueChange={setFiltroSituacao}>
              <SelectTrigger>
                <SelectValue placeholder="Filtrar por situação" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="todas">Todas as situações</SelectItem>
                <SelectItem value="validas">Válidas</SelectItem>
                <SelectItem value="expirando">Expirando (até 30 dias)</SelectItem>
                <SelectItem value="vencidas">Vencidas</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            Atualizar Todas
          </Button>
        </CardContent>
      </Card>

      {/* Lista de Certidões */}
      <Card>
        <CardHeader>
          <CardTitle>Certidões Cadastradas</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empresa</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Emissão</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Validade</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Dias</th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {filteredCertidoes.map((cert) => {
                  const config = getSituacaoConfig(cert.situacao, cert.dataValidade);
                  const dias = getDiasParaVencer(cert.dataValidade);
                  const Icon = config.icon;
                  
                  return (
                    <tr key={cert.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <Building2 className="h-4 w-4 text-gray-400" />
                          <div>
                            <p className="font-medium">{cert.empresa}</p>
                            <p className="text-xs text-gray-500">{cert.cnpj}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant="outline">{cert.tipo}</Badge>
                      </td>
                      <td className="px-4 py-3 text-sm">{new Date(cert.dataEmissao).toLocaleDateString('pt-BR')}</td>
                      <td className="px-4 py-3 text-sm">{new Date(cert.dataValidade).toLocaleDateString('pt-BR')}</td>
                      <td className="px-4 py-3">
                        <Badge className={config.color}>
                          <Icon className="h-3 w-3 mr-1" />
                          {config.label}
                        </Badge>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`font-semibold ${config.textColor}`}>
                          {dias > 0 ? `${dias} dias` : `${Math.abs(dias)} dias atrás`}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center justify-center gap-1">
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => consultarCertidao(cert.id, cert.tipo)}
                            disabled={consultando[cert.id]}
                            title="Renovar/Consultar"
                          >
                            <RefreshCw className={`h-4 w-4 ${consultando[cert.id] ? 'animate-spin' : ''}`} />
                          </Button>
                          {cert.arquivo && (
                            <Button variant="ghost" size="sm" title="Download">
                              <Download className="h-4 w-4" />
                            </Button>
                          )}
                          <Button variant="ghost" size="sm" title="Acessar portal">
                            <ExternalLink className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Links Rápidos */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ExternalLink className="h-5 w-5" />
            Portais de Consulta
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {tiposCertidao.filter(t => t.url).map(tipo => (
              <a 
                key={tipo.id}
                href={tipo.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <FileCheck className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="font-medium">{tipo.nome}</p>
                  <p className="text-xs text-gray-500">Clique para acessar</p>
                </div>
                <ExternalLink className="h-4 w-4 ml-auto text-gray-400" />
              </a>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Certidoes;
