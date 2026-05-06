export const masks = {
  cnpj: "99.999.999/9999-99",
  cpf: "999.999.999-99",
  cep: "99999-999",
  telefone: "(99) 99999-9999",
};

const onlyDigits = (value) => String(value || "").replace(/\D/g, "");

export const normalizeEmail = (value) => String(value || "").trim().toLowerCase().replace(/\s+/g, "");

export const formatCompetencia = (value) => {
  const digits = onlyDigits(value).slice(0, 6);
  if (digits.length <= 2) return digits;
  return `${digits.slice(0, 2)}/${digits.slice(2)}`;
};

export const formatProtocol = (value) => String(value || "").trim().toUpperCase().replace(/\s+/g, "");

export const formatPercent = (value) => {
  const digits = String(value || "").replace(/[^\d,.-]/g, "");
  return digits.replace(".", ",");
};

export const formatCurrencyInput = (value) => {
  const digits = onlyDigits(value);
  if (!digits) return "";
  const number = Number(digits) / 100;
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number.isFinite(number) ? number : 0);
};

export const formatCNPJ = (value) => {
  const digits = onlyDigits(value).slice(0, 14);
  return digits
    .replace(/^(\d{2})(\d)/, "$1.$2")
    .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
    .replace(/\.(\d{3})(\d)/, ".$1/$2")
    .replace(/(\d{4})(\d)/, "$1-$2");
};

export const formatCPF = (value) => {
  const digits = onlyDigits(value).slice(0, 11);
  return digits
    .replace(/^(\d{3})(\d)/, "$1.$2")
    .replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3")
    .replace(/\.(\d{3})(\d)/, ".$1-$2");
};

export const formatTelefone = (value) => {
  const digits = onlyDigits(value).slice(0, 11);
  return digits
    .replace(/^(\d{2})(\d)/, "($1) $2")
    .replace(/(\d{5})(\d)/, "$1-$2");
};

export const formatCEP = (value) => {
  const digits = onlyDigits(value).slice(0, 8);
  return digits.replace(/^(\d{5})(\d)/, "$1-$2");
};

export function formatMoney(value) {
  const number = Number(value || 0);
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number.isFinite(number) ? number : 0);
}

export function formatDate(value) {
  if (!value) return "-";
  const date = value instanceof Date ? value : new Date(value);
  return Number.isNaN(date.getTime()) ? "-" : date.toLocaleDateString("pt-BR");
}
