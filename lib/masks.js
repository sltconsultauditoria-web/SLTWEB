export const maskCNPJ = (value) => {
  if (!value) return "";
  value = value.replace(/\D/g, "");
  value = value.replace(/^(\d{2})(\d)/, "\.\");
  value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "\.\.\");
  value = value.replace(/\.(\d{3})(\d)/, ".\/\");
  value = value.replace(/(\d{4})(\d)/, "\-\");
  return value.slice(0, 18);
};

export const maskIE = (value) => {
  if (!value) return "";
  value = value.replace(/\D/g, "");
  return value.slice(0, 14);
};
