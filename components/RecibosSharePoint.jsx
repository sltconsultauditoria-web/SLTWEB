/**
 * Componente de Recibos do SharePoint
 * Lista e permite download de recibos armazenados no SharePoint
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Loader2,
  AlertCircle,
  Download,
  Eye,
  FileText,
  Calendar,
  HardDrive,
} from 'lucide-react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export function RecibosSharePoint() {
  const [recibos, setRecibos] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [selectedEmpresa, setSelectedEmpresa] = useState('');
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const accessToken = localStorage.getItem('access_token');

  // Carregar empresas ao montar componente
  useEffect(() => {
    carregarEmpresas();
  }, []);

  // Carregar recibos quando empresa é selecionada
  useEffect(() => {
    if (selectedEmpresa) {
      carregarRecibos(selectedEmpresa);
    }
  }, [selectedEmpresa]);

  const carregarEmpresas = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/auth/empresas`, {
        params: { access_token: accessToken },
      });

      setEmpresas(response.data.empresas || []);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar empresas: ' + (err.response?.data?.detail || err.message));
      console.error('Erro ao carregar empresas:', err);
    } finally {
      setLoading(false);
    }
  };

  const carregarRecibos = async (empresaId) => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/auth/recibos`, {
        params: {
          access_token: accessToken,
          empresa_id: empresaId,
          limite: 100,
        },
      });

      setRecibos(response.data.recibos || []);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar recibos: ' + (err.response?.data?.detail || err.message));
      console.error('Erro ao carregar recibos:', err);
    } finally {
      setLoading(false);
    }
  };

  const baixarRecibo = async (nomeArquivo) => {
    try {
      setDownloading(nomeArquivo);

      // Obter URL de download do recibo
      const response = await axios.get(
        `${API_URL}/api/auth/recibos/${nomeArquivo}`,
        {
          params: { access_token: accessToken },
        }
      );

      // Criar link de download
      const link = document.createElement('a');
      link.href = response.data.download_url || URL.createObjectURL(
        new Blob([response.data], { type: 'application/pdf' })
      );
      link.setAttribute('download', nomeArquivo);
      document.body.appendChild(link);
      link.click();
      link.parentElement.removeChild(link);

      setSuccess(`Recibo ${nomeArquivo} baixado com sucesso`);
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Erro ao baixar recibo: ' + (err.response?.data?.detail || err.message));
      console.error('Erro ao baixar recibo:', err);
    } finally {
      setDownloading(null);
    }
  };

  const visualizarRecibo = async (nomeArquivo) => {
    try {
      // Abrir recibo em nova aba
      const url = `${API_URL}/api/auth/recibos/${nomeArquivo}?access_token=${accessToken}`;
      window.open(url, '_blank');
    } catch (err) {
      setError('Erro ao visualizar recibo');
      console.error('Erro ao visualizar recibo:', err);
    }
  };

  const formatarTamanho = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const formatarData = (dataString) => {
    return new Date(dataString).toLocaleDateString('pt-BR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="space-y-6">
      {/* Card de Seleção de Empresa */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Recibos do SharePoint
          </CardTitle>
          <CardDescription>
            Selecione uma empresa para visualizar seus recibos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {success && (
              <Alert className="bg-green-50 border-green-200">
                <AlertDescription className="text-green-800">{success}</AlertDescription>
              </Alert>
            )}

            <div className="flex gap-4">
              <div className="flex-1">
                <Select value={selectedEmpresa} onValueChange={setSelectedEmpresa}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione uma empresa..." />
                  </SelectTrigger>
                  <SelectContent>
                    {empresas.map((empresa) => (
                      <SelectItem key={empresa} value={empresa}>
                        {empresa}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <Button
                onClick={() => carregarEmpresas()}
                disabled={loading}
                variant="outline"
              >
                {loading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  'Atualizar'
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabela de Recibos */}
      {selectedEmpresa && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">
              Recibos de {selectedEmpresa}
            </CardTitle>
            <CardDescription>
              Total: {recibos.length} recibo(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex justify-center py-8">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
              </div>
            ) : recibos.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>Nenhum recibo encontrado para esta empresa</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome do Arquivo</TableHead>
                      <TableHead className="flex items-center gap-1">
                        <HardDrive className="h-4 w-4" />
                        Tamanho
                      </TableHead>
                      <TableHead className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        Modificado
                      </TableHead>
                      <TableHead className="text-right">Ações</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {recibos.map((recibo) => (
                      <TableRow key={recibo.id}>
                        <TableCell className="font-medium">
                          {recibo.nome}
                        </TableCell>
                        <TableCell>
                          {formatarTamanho(recibo.tamanho)}
                        </TableCell>
                        <TableCell>
                          {formatarData(recibo.modificado)}
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex gap-2 justify-end">
                            <Button
                              onClick={() => visualizarRecibo(recibo.nome)}
                              disabled={downloading === recibo.nome}
                              variant="outline"
                              size="sm"
                              title="Visualizar"
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button
                              onClick={() => baixarRecibo(recibo.nome)}
                              disabled={downloading === recibo.nome}
                              variant="default"
                              size="sm"
                              title="Baixar"
                            >
                              {downloading === recibo.nome ? (
                                <Loader2 className="h-4 w-4 animate-spin" />
                              ) : (
                                <Download className="h-4 w-4" />
                              )}
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Informações de Segurança */}
      <Card className="bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-sm">🔒 Segurança</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-blue-900 space-y-2">
          <p>✓ Autenticação OAuth com Entra ID (Azure AD)</p>
          <p>✓ Acesso apenas de leitura aos recibos</p>
          <p>✓ Conformidade com LGPD e segurança de dados</p>
          <p>✓ Auditoria de todas as leituras registrada</p>
        </CardContent>
      </Card>
    </div>
  );
}

export default RecibosSharePoint;
