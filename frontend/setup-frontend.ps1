# ===============================
# CRIAR ESTRUTURA LIB
# ===============================

New-Item -ItemType Directory -Force -Path ".\src\lib" | Out-Null

# ===============================
# API BASE
# ===============================

@"
import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
"@ | Set-Content ".\src\lib\api.js"

# ===============================
# EMPRESAS SERVICE
# ===============================

@"
import api from "./api";

export const listarEmpresas = async () => {
  const { data } = await api.get("/empresas");
  return data;
};

export const criarEmpresa = async (payload) => {
  const { data } = await api.post("/empresas", payload);
  return data;
};

export const atualizarEmpresa = async (id, payload) => {
  const { data } = await api.put(`/empresas/${id}`, payload);
  return data;
};

export const excluirEmpresa = async (id) => {
  const { data } = await api.delete(`/empresas/${id}`);
  return data;
};
"@ | Set-Content ".\src\lib\empresasService.js"

# ===============================
# ALERTAS SERVICE
# ===============================

@"
import api from "./api";

export const listarAlertas = async () => {
  const { data } = await api.get("/alertas");
  return data;
};

export const marcarComoLido = async (id) => {
  const { data } = await api.put(`/alertas/${id}/lido`);
  return data;
};
"@ | Set-Content ".\src\lib\alertasService.js"

# ===============================
# FISCAL SERVICE
# ===============================

@"
import api from "./api";

export const listarObrigações = async () => {
  const { data } = await api.get("/fiscal/obrigacoes");
  return data;
};

export const gerarGuia = async (payload) => {
  const { data } = await api.post("/fiscal/guia", payload);
  return data;
};
"@ | Set-Content ".\src\lib\fiscalService.js"

# ===============================
# MASCARAS
# ===============================

@"
export const maskCNPJ = (value) => {
  if (!value) return "";
  value = value.replace(/\D/g, "");
  value = value.replace(/^(\d{2})(\d)/, "\$1.\$2");
  value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "\$1.\$2.\$3");
  value = value.replace(/\.(\d{3})(\d)/, ".\$1/\$2");
  value = value.replace(/(\d{4})(\d)/, "\$1-\$2");
  return value.slice(0, 18);
};

export const maskIE = (value) => {
  if (!value) return "";
  value = value.replace(/\D/g, "");
  return value.slice(0, 14);
};
"@ | Set-Content ".\src\lib\masks.js"

Write-Host ""
Write-Host "======================================="
Write-Host " INTEGRAÇÃO CONCLUÍDA COM SUCESSO"
Write-Host "======================================="
Write-Host ""
