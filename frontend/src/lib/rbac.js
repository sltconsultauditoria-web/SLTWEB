export const normalizeRole = (value) => {
  const role = String(value || "").trim().toLowerCase();
  if (role === "administrator" || role === "superadmin") return "admin";
  if (role === "visualizacao" || role === "visualização") return "viewer";
  return role;
};

export const userRole = (user) => normalizeRole(user?.role || user?.perfil);

export const isAdminUser = (user) => ["admin", "super_admin"].includes(userRole(user));
