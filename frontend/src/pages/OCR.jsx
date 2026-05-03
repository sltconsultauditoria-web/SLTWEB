import React, { useEffect, useMemo, useState } from "react";
import { AlertTriangle, CheckCircle, Clock, FileText, ScanLine, Upload } from "lucide-react";
import api from "../services/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const toArray = (value) => {
  if (Array.isArray(value)) return value;
  if (Array.isArray(value?.data)) return value.data;
  if (Array.isArray(value?.documentos)) return value.documentos;
  if (Array.isArray(value?.tipos)) return value.tipos;
  return [];
};

const formatarData = (value) => {
  if (!value) return "-";
  const data = new Date(value);
  return Number.isNaN(data.getTime()) ? "-" : data.toLocaleDateString("pt-BR");
};

const formatarTamanho = (bytes) => {
  const value = Number(bytes || 0);
  if (!value) return "-";
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
  return `${(value / (1024 * 1024)).toFixed(1)} MB`;
};

export default function OCR() {
  const [file, setFile] = useState(null);
  const [documentos, setDocumentos] = useState([]);
  const [estatisticas, setEstatisticas] = useState({});
  const [tipos, setTipos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState("");

  const carregarDados = async () => {
    setLoading(true);
    setErro("");

    try {
      const [documentosRes, estatisticasRes, tiposRes] = await Promise.all([
        api.get("/ocr/documentos"),
        api.get("/ocr/estatisticas"),
        api.get("/ocr/tipos-suportados"),
      ]);

      setDocumentos(toArray(documentosRes.data));
      setEstatisticas(estatisticasRes.data || {});
      setTipos(toArray(tiposRes.data));
    } catch (error) {
      console.error("Erro ao carregar OCR:", error);
      setErro("Nao foi possivel carregar os dados de OCR.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  const enviar = async () => {
    if (!file) {
      setErro("Selecione um arquivo PDF, PNG ou JPG.");
      return;
    }

    setEnviando(true);
    setErro("");

    try {
      const form = new FormData();
      form.append("file", file);
      await api.post("/ocr/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFile(null);
      await carregarDados();
    } catch (error) {
      console.error("Erro ao enviar OCR:", error);
      setErro(error?.response?.data?.detail || "Erro ao processar arquivo OCR.");
    } finally {
      setEnviando(false);
    }
  };

  const resumo = useMemo(() => ({
    total: Number(estatisticas.total || documentos.length || 0),
    processados: Number(estatisticas.processados || documentos.filter((doc) => doc.status === "processado").length || 0),
    pendentes: Number(estatisticas.pendentes || estatisticas.revisao_necessaria || 0),
    erros: Number(estatisticas.erros || 0),
  }), [documentos, estatisticas]);

  const statusBadge = (status) => {
    const value = String(status || "recebido").toLowerCase();
    if (["erro", "falha", "failed"].includes(value)) return <Badge className="bg-red-500">Erro</Badge>;
    if (["recebido", "pendente", "processando"].includes(value)) return <Badge className="bg-yellow-500">Pendente</Badge>;
    return <Badge className="bg-green-500">Processado</Badge>;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-900"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="ocr-page">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <ScanLine className="h-7 w-7 text-indigo-600" />
          OCR Documentos
        </h1>
        <p className="text-gray-500">Processamento de documentos fiscais com persistencia no MongoDB</p>
      </div>

      {erro && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-4 flex items-center gap-3 text-red-700">
            <AlertTriangle className="h-5 w-5" />
            <span className="text-sm font-medium">{erro}</span>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card><CardContent className="p-4 flex items-center justify-between"><div><p className="text-sm text-gray-500">Documentos OCR</p><p className="text-2xl font-bold text-blue-600">{resumo.total}</p></div><FileText className="h-8 w-8 text-blue-500" /></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center justify-between"><div><p className="text-sm text-gray-500">Processados</p><p className="text-2xl font-bold text-green-600">{resumo.processados}</p></div><CheckCircle className="h-8 w-8 text-green-500" /></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center justify-between"><div><p className="text-sm text-gray-500">Pendentes</p><p className="text-2xl font-bold text-yellow-600">{resumo.pendentes}</p></div><Clock className="h-8 w-8 text-yellow-500" /></CardContent></Card>
        <Card><CardContent className="p-4 flex items-center justify-between"><div><p className="text-sm text-gray-500">Com Erro</p><p className="text-2xl font-bold text-red-600">{resumo.erros}</p></div><AlertTriangle className="h-8 w-8 text-red-500" /></CardContent></Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Enviar Documento
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col md:flex-row gap-3 md:items-center">
            <input
              type="file"
              accept=".pdf,.png,.jpg,.jpeg,application/pdf,image/png,image/jpeg"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-700 file:mr-4 file:rounded-md file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-medium file:text-blue-700 hover:file:bg-blue-100"
            />
            <Button onClick={enviar} disabled={enviando} className="bg-blue-900 hover:bg-blue-800">
              {enviando ? "Processando..." : "Processar"}
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {tipos.map((tipo) => (
              <Badge key={tipo.codigo || tipo.descricao} variant="outline">
                {tipo.descricao}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Documentos Processados</CardTitle>
        </CardHeader>
        <CardContent>
          {documentos.length === 0 ? (
            <div className="text-center py-10 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-3 text-gray-300" />
              <p>Nenhum documento OCR encontrado.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Arquivo</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Tipo</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Tamanho</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Data</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {documentos.map((doc, index) => (
                    <tr key={doc.id || index} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium text-gray-900">{doc.nome_arquivo || doc.nome || "Documento"}</td>
                      <td className="px-4 py-3 text-gray-600">{doc.content_type || doc.tipo || "-"}</td>
                      <td className="px-4 py-3 text-gray-600">{formatarTamanho(doc.tamanho_bytes)}</td>
                      <td className="px-4 py-3 text-gray-600">{formatarData(doc.created_at)}</td>
                      <td className="px-4 py-3">{statusBadge(doc.status)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
