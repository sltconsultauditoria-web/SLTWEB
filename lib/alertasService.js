import api from "./api";

export const listarAlertas = async () => {
  const { data } = await api.get("/alertas");
  return data;
};

export const marcarComoLido = async (id) => {
  const { data } = await api.put(/alertas//lido);
  return data;
};
