import api from "./api";

export const listarObrigações = async () => {
  const { data } = await api.get("/fiscal/obrigacoes");
  return data;
};

export const gerarGuia = async (payload) => {
  const { data } = await api.post("/fiscal/guia", payload);
  return data;
};
