import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Shield, 
  Upload, 
  FileText, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Loader2,
  BarChart3,
  TrendingUp,
  Search
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Auditoria = () => {
  const [loading, setLoading] = useState(false);
  const [auditorias, setAuditorias] = useState([]);
  const [estatisticas, setEstatisticas] = useState(null);
  const [auditoriaSelecionada, setAuditoriaSelecionada] = useState(null);

  // Form de nova auditoria
  const [formData, setFormData] = useState({
    cnpj: '12.345.678/0001-00',
    periodo: '2025-12',
    tipo: 'sped_fiscal'
  });
  const [arquivo, setArquivo] = useState(null);

  const carregarDados = useCallback(async () => {
    try {
      const [auditoriasRes, estatisticasRes] = await Promise.all([
        axios.get(`${API}/auditoria/`),
        axios.get(`${API}/auditoria/estatisticas`)
      ]);
      setAuditorias(auditoriasRes.data.auditorias || []);
      setEstatisticas(estatisticasRes.data);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    }
  }, []);

  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const handleExecutarAuditoria = async (e) => {
    e.preventDefault();
    if (!arquivo) {
      alert('Selecione um arquivo SPED');
      return;
    }

    setLoading(true);
    try {
      const form = new FormData();
      form.append('cnpj', formData.cnpj);
      form.append('periodo', formData.periodo);
      form.append('tipo', formData.tipo);
      form.append('arquivo', arquivo);

      const response = await axios.post(`${API}/auditoria/executar`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setAuditoriaSelecionada(response.data);
      carregarDados();
      alert('Auditoria executada com sucesso!');
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro na auditoria: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleVerDetalhes = async (auditoria) => {
    try {
      const response = await axios.get(`${API}/auditoria/${auditoria.id}`);
      setAuditoriaSelecionada(response.data);
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 90) return 'bg-green-100';
    if (score >= 70) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="space-y-6" data-testid="auditoria-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Shield className="h-7 w-7 text-purple-600" />
          Auditoria Fiscal (Kolossus)
        </h1>
        <p className="text-gray-500">Análise de conformidade SPED e cruzamento fiscal</p>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Total Auditorias</p>
                <p className="text-2xl font-bold text-blue-600">{estatisticas?.total_auditorias || 0}</p>
              </div>
              <BarChart3 className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Score Médio</p>
                <p className={`text-2xl font-bold ${getScoreColor(estatisticas?.score_medio || 0)}`}>
                  {estatisticas?.score_medio?.toFixed(1) || 0}%
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Itens Críticos</p>
                <p className="text-2xl font-bold text-red-600">{estatisticas?.total_criticos || 0}</p>
              </div>
              <XCircle className="h-8 w-8 text-red-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Avisos</p>
                <p className="text-2xl font-bold text-yellow-600">{estatisticas?.total_avisos || 0}</p>
              </div>
              <AlertTriangle className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Formulário de Nova Auditoria */}
        <Card>
          <CardHeader>
            <CardTitle>Executar Nova Auditoria</CardTitle>
            <CardDescription>Faça upload de um arquivo SPED para análise</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleExecutarAuditoria} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="cnpj">CNPJ</Label>
                  <Input
                    id="cnpj"
                    value={formData.cnpj}
                    onChange={(e) => setFormData({...formData, cnpj: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="periodo">Período</Label>
                  <Input
                    id="periodo"
                    value={formData.periodo}
                    onChange={(e) => setFormData({...formData, periodo: e.target.value})}
                    placeholder="YYYY-MM"
                  />
                </div>
              </div>
              <div>
                <Label htmlFor="tipo">Tipo de SPED</Label>
                <select
                  id="tipo"
                  className="w-full p-2 border rounded-md"
                  value={formData.tipo}
                  onChange={(e) => setFormData({...formData, tipo: e.target.value})}
                >
                  <option value="sped_fiscal">SPED Fiscal (ICMS/IPI)</option>
                  <option value="sped_contribuicoes">SPED Contribuições (PIS/COFINS)</option>
                </select>
              </div>
              <div>
                <Label htmlFor="arquivo">Arquivo SPED (.txt)</Label>
                <Input
                  id="arquivo"
                  type="file"
                  accept=".txt"
                  onChange={(e) => setArquivo(e.target.files[0])}
                />
              </div>
              <Button type="submit" disabled={loading} className="w-full bg-purple-600 hover:bg-purple-700">
                {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Upload className="h-4 w-4 mr-2" />}
                Executar Auditoria
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Resultado da Auditoria Selecionada */}
        {auditoriaSelecionada && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Resultado da Auditoria</span>
                <Badge className={getScoreBg(auditoriaSelecionada.score_conformidade)}>
                  Score: {auditoriaSelecionada.score_conformidade?.toFixed(1)}%
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">CNPJ:</span>
                  <span className="font-medium">{auditoriaSelecionada.cnpj}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Tipo:</span>
                  <span className="font-medium">{auditoriaSelecionada.tipo}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Período:</span>
                  <span className="font-medium">{auditoriaSelecionada.periodo_referencia}</span>
                </div>

                <div className="pt-4 border-t">
                  <h4 className="font-medium mb-2">Não Conformidades ({auditoriaSelecionada.total_nao_conformidades})</h4>
                  <div className="flex gap-2">
                    <Badge className="bg-red-100 text-red-800">
                      Críticos: {auditoriaSelecionada.por_severidade?.critico || 0}
                    </Badge>
                    <Badge className="bg-yellow-100 text-yellow-800">
                      Avisos: {auditoriaSelecionada.por_severidade?.aviso || 0}
                    </Badge>
                    <Badge className="bg-blue-100 text-blue-800">
                      Info: {auditoriaSelecionada.por_severidade?.informativo || 0}
                    </Badge>
                  </div>
                </div>

                {auditoriaSelecionada.nao_conformidades && auditoriaSelecionada.nao_conformidades.length > 0 && (
                  <div className="pt-4 border-t space-y-2">
                    <h4 className="font-medium">Detalhes</h4>
                    {auditoriaSelecionada.nao_conformidades.slice(0, 5).map((nc, idx) => (
                      <div key={idx} className="p-2 bg-gray-50 rounded text-sm">
                        <div className="flex items-center gap-2">
                          {nc.severidade === 'Crítico' ? (
                            <XCircle className="h-4 w-4 text-red-600" />
                          ) : (
                            <AlertTriangle className="h-4 w-4 text-yellow-600" />
                          )}
                          <span className="font-medium">{nc.regra}</span>
                        </div>
                        <p className="text-gray-600 mt-1">{nc.descricao}</p>
                      </div>
                    ))}
                  </div>
                )}

                {auditoriaSelecionada.recomendacao && (
                  <div className="pt-4 border-t">
                    <h4 className="font-medium mb-2">Recomendação</h4>
                    <p className="text-sm text-gray-600 bg-blue-50 p-3 rounded">
                      {auditoriaSelecionada.recomendacao}
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Lista de Auditorias */}
      <Card>
        <CardHeader>
          <CardTitle>Histórico de Auditorias</CardTitle>
        </CardHeader>
        <CardContent>
          {auditorias.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-3 text-gray-300" />
              <p>Nenhuma auditoria realizada ainda</p>
            </div>
          ) : (
            <div className="space-y-3">
              {auditorias.map((auditoria, idx) => (
                <div 
                  key={idx}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
                  onClick={() => handleVerDetalhes(auditoria)}
                >
                  <div className="flex items-center gap-4">
                    <div className={`p-2 rounded-full ${getScoreBg(auditoria.score_conformidade)}`}>
                      {auditoria.score_conformidade >= 90 ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : auditoria.score_conformidade >= 70 ? (
                        <AlertTriangle className="h-5 w-5 text-yellow-600" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-600" />
                      )}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{auditoria.tipo}</p>
                      <p className="text-sm text-gray-500">
                        {auditoria.cnpj} | {auditoria.periodo_referencia}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`text-xl font-bold ${getScoreColor(auditoria.score_conformidade)}`}>
                      {auditoria.score_conformidade?.toFixed(0)}%
                    </p>
                    <p className="text-xs text-gray-400">
                      {new Date(auditoria.created_at).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Auditoria;
