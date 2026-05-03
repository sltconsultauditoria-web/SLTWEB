export {
  formatCEP,
  formatCNPJ,
  formatCPF,
  formatDate,
  formatMoney,
  formatTelefone,
  masks,
} from "../utils/masks";

export const maskCNPJ = formatCNPJ;

export const maskIE = (value) => {
  if (!value) return "";
  return String(value).replace(/\D/g, "").slice(0, 14);
};
