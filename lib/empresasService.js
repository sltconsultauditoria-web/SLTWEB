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
  const { data } = await api.put(/empresas/, payload);
  return data;
};

export const excluirEmpresa = async (id) => {
  const { data } = await api.delete(/empresas/);
  return data;
};
