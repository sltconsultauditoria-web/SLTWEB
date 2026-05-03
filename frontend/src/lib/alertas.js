const normalizeText = (value, fallback = "") => {
  if (typeof value !== "string") return fallback;
  const trimmed = value.trim();
  return trimmed || fallback;
};

const normalizePriority = (value) => {
  const raw = normalizeText(value).toLowerCase();
  const mapping = {
    crítico: "critica",
    critico: "critica",
    critical: "critica",
    alta: "alta",
    high: "alta",
    media: "media",
    média: "media",
    medium: "media",
    baixa: "baixa",
    low: "baixa",
  };

  return mapping[raw] || raw || "media";
};

const normalizeStatus = (value) => {
  const raw = normalizeText(value).toLowerCase();
  const mapping = {
    lido: "lido",
    read: "lido",
    resolvido: "resolvido",
    resolved: "resolvido",
    arquivado: "arquivado",
    archived: "arquivado",
    pendente: "pendente",
    pending: "pendente",
  };

  return mapping[raw] || raw || "pendente";
};

const isResolvedAlert = (alerta) => {
  const status = normalizeStatus(alerta?.status || alerta?.data?.status);
  return Boolean(alerta?.resolvido || alerta?.data?.resolvido || status === "resolvido" || status === "arquivado");
};

const isReadAlert = (alerta) => {
  const status = normalizeStatus(alerta?.status || alerta?.data?.status);
  return Boolean(alerta?.lido || alerta?.data?.lido || status === "lido");
};

const isUnreadAlert = (alerta) => !isReadAlert(alerta) && !isResolvedAlert(alerta);

const isCriticalAlert = (alerta) => {
  const prioridade = normalizePriority(alerta?.prioridade || alerta?.data?.prioridade || alerta?.nivel || alerta?.data?.nivel);
  return ["critica", "alta"].includes(prioridade) && !isResolvedAlert(alerta);
};

const normalizeAlerta = (item = {}) => {
  const nested = typeof item?.data === "object" && item.data ? item.data : {};
  const prioridade = normalizePriority(item.prioridade || nested.prioridade || item.nivel || nested.nivel);
  const status = normalizeStatus(item.status || nested.status || (item.resolvido || nested.resolvido ? "resolvido" : item.lido || nested.lido ? "lido" : "pendente"));
  const resolved = isResolvedAlert({ ...item, prioridade, status });
  const read = isReadAlert({ ...item, prioridade, status });

  return {
    ...item,
    id: item.id || item._id || nested.id || "",
    tipo: normalizeText(item.tipo || nested.tipo, "sistema"),
    prioridade,
    titulo: normalizeText(item.titulo || nested.titulo || item.mensagem || nested.mensagem, "Alerta"),
    descricao: normalizeText(item.descricao || nested.descricao || item.mensagem || nested.mensagem, ""),
    empresa: item.empresa || nested.empresa || null,
    tempo: normalizeText(item.tempo || nested.tempo, ""),
    status,
    lido: read,
    resolvido: resolved,
    data: item.data || item.created_at || item.createdAt || item.timestamp || nested.data || nested.created_at || nested.createdAt || null,
  };
};

const normalizeAlertas = (items) => {
  if (!Array.isArray(items)) return [];
  return items.map(normalizeAlerta);
};

const countBadgeAlertas = (items) => normalizeAlertas(items).filter(isUnreadAlert).length;

const countCriticalAlertas = (items) => normalizeAlertas(items).filter(isCriticalAlert).length;

const formatBadgeCount = (count) => {
  const total = Number(count);
  if (!Number.isFinite(total) || total <= 0) return 0;
  return total > 99 ? "99+" : total;
};

export {
  countBadgeAlertas,
  countCriticalAlertas,
  formatBadgeCount,
  isCriticalAlert,
  isReadAlert,
  isResolvedAlert,
  isUnreadAlert,
  normalizeAlerta,
  normalizeAlertas,
  normalizePriority,
  normalizeStatus,
};
