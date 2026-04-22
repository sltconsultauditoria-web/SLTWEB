import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  ScanLine, 
  Upload, 
  FileText, 
  CheckCircle, 
  AlertTriangle,
  Loader2,
  Image,
  File,
  Percent,
  Eye
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const OCR = () => {
  const [loading, setLoading] = useState(false);
  const [documentos, setDocumentos] = useState([]);
  const [estatisticas, setEstatisticas] = useState(null);
  const [resultado, setResultado] = useState(null);
  const [arquivos, setArquivos] = useState([]);
  const [tiposSuportados, setTiposSuportados] = useState([]);

  const carregarDados = useCallback(async () => {
    try {
      const [docsRes, statsRes, tiposRes] = await Promise.all([
        axios.get(`${API}/ocr/documentos?limit=20`),
        axios.get(`${API}/ocr/estatisticas`),
        axios.get(`${API}/ocr/tipos-suportados`)
      ]);
      setDocumentos(docsRes.data.documentos || []);
      setEstatisticas(statsRes.data);
      setTiposSuportados(tiposRes.data.tipos || []);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    }
  }, []);

  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const handleFileChange = (e) => {
    if (e.target.files) {
      setArquivos(Array.from(e.target.files));
    }
  };

  const handleProcessar = async () => {
    if (arquivos.length === 0) {
      alert('Selecione pelo menos um arquivo');
      return;
    }

    setLoading(true);
    setResultado(null);

    try {
      // Processar primeiro arquivo como exemplo
      const form = new FormData();
      form.append('arquivo', arquivos[0]);

      const response = await axios.post(`${API}/ocr/processar`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setResultado(response.data);
      carregarDados();
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro no processamento: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 50) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  const getTipoLabel = (codigo) => {
    const tipo = tiposSuportados.find(t => t.codigo === codigo);
    return tipo ? tipo.descricao : codigo;
  };

  return (
    <div className="space-y-6" data-testid="ocr-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <ScanLine className="h-7 w-7 text-indigo-600" />
          OCR e Automação Documental (Kolossus)
        </h1>
        <p className="text-gray-500">Processamento inteligente de documentos fiscais com OCR e NLP</p>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Total Processados</p>
                <p className="text-2xl font-bold text-blue-600">{estatisticas?.total || 0}</p>
              </div>
              <FileText className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Taxa de Sucesso</p>
                <p className="text-2xl font-bold text-green-600">{estatisticas?.taxa_sucesso?.toFixed(1) || 0}%</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500" />
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
              <Percent className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Revisão Necessária</p>
                <p className="text-2xl font-bold text-yellow-600">{estatisticas?.revisao_necessaria || 0}</p>
              </div>
              <AlertTriangle className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upload de Documentos */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5 text-indigo-600" />
              Upload de Documentos
            </CardTitle>
            <CardDescription>Arraste ou selecione documentos para processamento OCR</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div 
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-500 transition-colors cursor-pointer"
              onClick={() => document.getElementById('file-input').click()}
            >
              <input
                type="file"
                multiple
                onChange={handleFileChange}
                className="hidden"
                id="file-input"
                accept=".pdf,.png,.jpg,.jpeg"
              />
              <Upload className="mx-auto text-gray-400 mb-2" size={32} />
              <p className="text-gray-600">Clique para selecionar ou arraste arquivos aqui</p>
              <p className="text-sm text-gray-500 mt-1">Suportados: PDF, PNG, JPG</p>
            </div>

            {arquivos.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">Arquivos selecionados:</h4>
                <ul className="space-y-2">
                  {arquivos.map((file, i) => (
                    <li key={i} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                      {file.type.includes('image') ? (
                        <Image size={20} className="text-gray-400" />
                      ) : (
                        <File size={20} className="text-gray-400" />
                      )}
                      <span className="text-sm text-gray-700">{file.name}</span>
                      <span className="text-xs text-gray-400 ml-auto">
                        {(file.size / 1024).toFixed(1)} KB
                      </span>
                    </li>
                  ))}
                </ul>
                <Button 
                  onClick={handleProcessar} 
                  disabled={loading}
                  className="w-full bg-indigo-600 hover:bg-indigo-700"
                >
                  {loading ? (
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  ) : (
                    <ScanLine className="h-4 w-4 mr-2" />
                  )}
                  Processar com OCR
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Resultado do Processamento */}
        {resultado && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Resultado do Processamento</span>
                <Badge className={getScoreBg(resultado.score_confianca)}>
                  Confiança: {resultado.score_confianca?.toFixed(1)}%
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">ID:</span>
                <span className="font-mono text-xs">{resultado.id}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Tipo Detectado:</span>
                <Badge className="bg-blue-100 text-blue-800">
                  {getTipoLabel(resultado.tipo)}
                </Badge>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Status:</span>
                <Badge className={resultado.status === 'processado' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                  {resultado.status === 'processado' ? 'Processado' : 'Revisão Necessária'}
                </Badge>
              </div>

              {resultado.dados_extraidos && Object.keys(resultado.dados_extraidos).length > 0 && (
                <div className="pt-4 border-t">
                  <h4 className="font-medium mb-2">Dados Extraídos</h4>
                  <div className="bg-gray-50 p-3 rounded space-y-2">
                    {resultado.dados_extraidos.cnpj_formatado && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">CNPJ:</span>
                        <span className="font-medium">{resultado.dados_extraidos.cnpj_formatado}</span>
                      </div>
                    )}
                    {resultado.dados_extraidos.valor && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Valor:</span>
                        <span className="font-medium">R$ {resultado.dados_extraidos.valor}</span>
                      </div>
                    )}
                    {resultado.dados_extraidos.data && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Data:</span>
                        <span className="font-medium">{resultado.dados_extraidos.data}</span>
                      </div>
                    )}
                    {resultado.dados_extraidos.numero_nf && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Nº NF:</span>
                        <span className="font-medium">{resultado.dados_extraidos.numero_nf}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {resultado.validacoes && (
                <div className="pt-4 border-t">
                  <h4 className="font-medium mb-2">Validações</h4>
                  <div className="flex flex-wrap gap-2">
                    {resultado.validacoes.cnpj_valido !== undefined && (
                      <Badge className={resultado.validacoes.cnpj_valido ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                        {resultado.validacoes.cnpj_valido ? '✓' : '✗'} CNPJ
                      </Badge>
                    )}
                    {resultado.validacoes.valor_positivo !== undefined && (
                      <Badge className={resultado.validacoes.valor_positivo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                        {resultado.validacoes.valor_positivo ? '✓' : '✗'} Valor
                      </Badge>
                    )}
                    {resultado.validacoes.data_valida !== undefined && (
                      <Badge className={resultado.validacoes.data_valida ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                        {resultado.validacoes.data_valida ? '✓' : '✗'} Data
                      </Badge>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </div>

      {/* Lista de Documentos Processados */}
      <Card>
        <CardHeader>
          <CardTitle>Documentos Processados</CardTitle>
        </CardHeader>
        <CardContent>
          {documentos.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-3 text-gray-300" />
              <p>Nenhum documento processado ainda</p>
            </div>
          ) : (
            <div className="space-y-3">
              {documentos.map((doc, idx) => (
                <div 
                  key={idx}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className={`p-2 rounded-full ${getScoreBg(doc.score_confianca)}`}>
                      <FileText className={`h-5 w-5 ${getScoreColor(doc.score_confianca)}`} />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{doc.nome_arquivo}</p>
                      <p className="text-sm text-gray-500">
                        {getTipoLabel(doc.tipo_detectado)} | {(doc.tamanho_bytes / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <Badge className={doc.status === 'processado' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                      {doc.status === 'processado' ? 'OK' : 'Revisar'}
                    </Badge>
                    <div className="text-right">
                      <p className={`text-lg font-bold ${getScoreColor(doc.score_confianca)}`}>
                        {doc.score_confianca?.toFixed(0)}%
                      </p>
                      <p className="text-xs text-gray-400">
                        {new Date(doc.created_at).toLocaleDateString('pt-BR')}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Tipos Suportados */}
      <Card>
        <CardHeader>
          <CardTitle>Tipos de Documentos Suportados</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            {tiposSuportados.map((tipo, idx) => (
              <Badge key={idx} variant="outline" className="justify-center py-2">
                {tipo.descricao}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default OCR;
