import { useState, useCallback, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Upload, 
  FileText, 
  CheckCircle, 
  Clock, 
  AlertTriangle,
  Download,
  Eye,
  Trash2,
  File
} from 'lucide-react';
import axios from 'axios';
import { Viewer } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';

const Documentos = () => {
  const [documentos, setDocumentos] = useState([
    { id: 1, nome: 'nfe_12345.pdf', tipo: 'NF-e', empresa: 'TRES PINHEIROS', status: 'processado', tempo: '8.5s', data: '17/12/2024 14:30' },
    { id: 2, nome: 'das_202501.pdf', tipo: 'DAS', empresa: 'SUPER GALO', status: 'processado', tempo: '5.2s', data: '17/12/2024 14:15' },
    { id: 3, nome: 'dctf_202412.pdf', tipo: 'DCTF', empresa: 'TRES PINHEIROS', status: 'processado', tempo: '12.3s', data: '17/12/2024 13:45' },
    { id: 4, nome: 'certidao_fgts.pdf', tipo: 'Certidão', empresa: 'MAFE REST.', status: 'processando', tempo: null, data: '17/12/2024 13:30' },
    { id: 5, nome: 'balancete_2024.pdf', tipo: 'Balancete', empresa: 'TECH SOLUTIONS', status: 'erro', tempo: null, data: '17/12/2024 12:00', erro: 'Arquivo corrompido' },
  ]);
  const [isDragging, setIsDragging] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, API.get('/replace_with_real_endpoint'));

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, API.get('/replace_with_real_endpoint'));

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  }, API.get('/replace_with_real_endpoint'));

  const handleFileInput = (e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
  };

  const handleFiles = (files) => {
    files.forEach(file => {
      const newDoc = {
        id: Date.now() + Math.random(),
        nome: file.name,
        tipo: 'PDF',
        empresa: 'A definir',
        status: 'processando',
        tempo: null,
        data: new Date().toLocaleString('pt-BR')
      };
      setDocumentos(prev => [newDoc, ...prev]);
      
      // Simular processamento
      setTimeout(() => {
        setDocumentos(prev => prev.map(doc => 
          doc.id === newDoc.id 
            ? { ...doc, status: 'processado', tempo: `${(Math.random() * 10 + 2).toFixed(1)}s` }
            : doc
        ));
      }, 3000);
    });
  };

  const handleDownload = async (documentoId) => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/documentos/${documentoId}/download`, {
        responseType: 'blob',
      });

      // Criar um link para download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${documentoId}.pdf`); // Nome do arquivo
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('Erro ao realizar o download:', error);
      alert('Erro ao realizar o download do documento.');
    }
  };

  const getStatusConfig = (status) => {
    const configs = {
      'processado': { color: 'bg-green-100 text-green-800', icon: CheckCircle },
      'processando': { color: 'bg-blue-100 text-blue-800', icon: Clock },
      'erro': { color: 'bg-red-100 text-red-800', icon: AlertTriangle }
    };
    return configs[status] || configs['processando'];
  };

  const stats = {
    total: documentos.length,
    processados: documentos.filter(d => d.status === 'processado').length,
    processando: documentos.filter(d => d.status === 'processando').length,
    erros: documentos.filter(d => d.status === 'erro').length
  };

  const handleView = (documento) => {
    setSelectedDoc(documento);
    setIsModalOpen(true);
  };

  const handleDelete = async (documentoId) => {
    try {
      await axios.delete(`${BACKEND_URL}/api/documentos/${documentoId}`);
      setDocumentos((prev) => prev.filter((doc) => doc.id !== documentoId));
      alert('Documento excluído com sucesso!');
    } catch (error) {
      console.error('Erro ao excluir o documento:', error);
      alert('Erro ao excluir o documento.');
    }
  };

  return (
    <div className="space-y-6" data-testid="documentos-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Documentos</h1>
        <p className="text-gray-500">Upload e processamento de documentos fiscais</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total</p>
              <p className="text-2xl font-bold">{stats.total}</p>
            </div>
            <FileText className="h-8 w-8 text-gray-400" />
          </CardContent>
        </Card>
        <Card className="bg-green-50">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600">Processados</p>
              <p className="text-2xl font-bold text-green-700">{stats.processados}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-500" />
          </CardContent>
        </Card>
        <Card className="bg-blue-50">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600">Processando</p>
              <p className="text-2xl font-bold text-blue-700">{stats.processando}</p>
            </div>
            <Clock className="h-8 w-8 text-blue-500" />
          </CardContent>
        </Card>
        <Card className="bg-red-50">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-red-600">Erros</p>
              <p className="text-2xl font-bold text-red-700">{stats.erros}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-red-500" />
          </CardContent>
        </Card>
      </div>

      {/* Upload Area */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Upload de Documentos
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            data-testid="upload-area"
          >
            <Upload className={`h-12 w-12 mx-auto mb-4 ${isDragging ? 'text-blue-500' : 'text-gray-400'}`} />
            <p className="text-lg font-medium text-gray-700 mb-2">
              {isDragging ? 'Solte os arquivos aqui' : 'Arraste arquivos ou clique para selecionar'}
            </p>
            <p className="text-sm text-gray-500 mb-4">Suporta PDF, XML, JPG, PNG (máx. 10MB)</p>
            <input
              type="file"
              multiple
              accept=".pdf,.xml,.jpg,.jpeg,.png"
              onChange={handleFileInput}
              className="hidden"
              id="file-upload"
              data-testid="file-input"
            />
            <label htmlFor="file-upload">
              <Button asChild className="bg-blue-900 hover:bg-blue-800">
                <span>Selecionar Arquivos</span>
              </Button>
            </label>
          </div>
        </CardContent>
      </Card>

      {/* Documents List */}
      <Card>
        <CardHeader>
          <CardTitle>Documentos Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {documentos.map((doc) => {
              const statusConfig = getStatusConfig(doc.status);
              const StatusIcon = statusConfig.icon;
              
              return (
                <div 
                  key={doc.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  data-testid={`documento-${doc.id}`}
                >
                  <div className="flex items-center gap-4">
                    <div className="p-2 bg-white rounded-lg shadow-sm">
                      <File className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{doc.nome}</p>
                      <div className="flex items-center gap-2 text-sm text-gray-500">
                        <span>{doc.tipo}</span>
                        <span>•</span>
                        <span>{doc.empresa}</span>
                        <span>•</span>
                        <span>{doc.data}</span>
                        {doc.tempo && (
                          <>
                            <span>•</span>
                            <span className="text-green-600">{doc.tempo}</span>
                          </>
                        )}
                      </div>
                      {doc.erro && (
                        <p className="text-sm text-red-600 mt-1">{doc.erro}</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge className={statusConfig.color}>
                      <StatusIcon className="h-3 w-3 mr-1" />
                      {doc.status === 'processado' ? 'Processado' : 
                       doc.status === 'processando' ? 'Processando...' : 'Erro'}
                    </Badge>
                    <div className="flex items-center gap-1">
                      <Button variant="ghost" size="icon" title="Visualizar" onClick={() => handleView(doc)}>
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" title="Download" onClick={() => handleDownload(doc.id)}>
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" title="Excluir" className="text-red-600 hover:text-red-700" onClick={() => handleDelete(doc.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Modal for Viewing Document */}
      {isModalOpen && (
        <Modal documento={selectedDoc} onClose={() => setIsModalOpen(false)}>
          <div className="p-4">
            <h2 className="text-xl font-bold mb-4">Detalhes do Documento</h2>
            <p><strong>Nome:</strong> {selectedDoc.nome}</p>
            <p><strong>Tipo:</strong> {selectedDoc.tipo}</p>
            <p><strong>Empresa:</strong> {selectedDoc.empresa}</p>
            <p><strong>Data:</strong> {selectedDoc.data}</p>
            {selectedDoc.erro && <p className="text-red-600"><strong>Erro:</strong> {selectedDoc.erro}</p>}
          </div>
        </Modal>
      )}
    </div>
  );
};

const Modal = ({ documento, onClose }) => {
  const [pdfUrl, setPdfUrl] = useState(null);

  useEffect(() => {
    if (documento && documento.file_path) {
      setPdfUrl(`${BACKEND_URL}/api/documentos/${documento.id}/download`);
    }
  }, [documento]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-2/3 relative">
        <button className="absolute top-2 right-2 text-gray-500" onClick={onClose}>X</button>
        <h2 className="text-xl font-bold mb-4">Detalhes do Documento</h2>
        <div className="space-y-2">
          <p><strong>Nome:</strong> {documento.nome}</p>
          <p><strong>Tipo:</strong> {documento.tipo}</p>
          <p><strong>Empresa:</strong> {documento.empresa}</p>
          <p><strong>Data:</strong> {documento.data}</p>
          {documento.erro && <p className="text-red-600"><strong>Erro:</strong> {documento.erro}</p>}
        </div>
        {pdfUrl && (
          <div className="mt-4">
            <Viewer
              fileUrl={pdfUrl}
              style={{ width: '100%', height: '500px' }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

const BACKEND_URL = "http://localhost:8000"; // Definir a URL do backend

export default Documentos;
