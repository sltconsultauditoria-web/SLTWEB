import {
  LayoutDashboard,
  Building2,
  FileText,
  Calendar,
  Bell,
  Settings,
  Receipt,
  FileBarChart,
  Bot,
  Calculator,
  Shield,
  ScanLine,
  UserCog,
  LibraryBig,
} from "lucide-react";

export const navigationGroups = [
  {
    title: "Operação",
    items: [
      { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard" },
      { icon: Building2, label: "Empresas", path: "/empresas" },
      { icon: FileText, label: "Documentos", path: "/documentos" },
      { icon: Calendar, label: "Obrigações", path: "/obrigacoes" },
      { icon: LibraryBig, label: "Catálogo Fiscal", path: "/catalogo-obrigacoes" },
      { icon: Receipt, label: "DAS/Guias", path: "/guias" },
      { icon: Calculator, label: "Fiscal (IRIS)", path: "/fiscal" },
      { icon: Shield, label: "Auditoria", path: "/auditoria" },
      { icon: ScanLine, label: "OCR", path: "/ocr" },
      { icon: Bot, label: "Robôs", path: "/robos" },
      { icon: Bell, label: "Alertas", path: "/alertas" },
      { icon: FileBarChart, label: "Relatórios", path: "/relatorios" },
    ],
  },
  {
    title: "Administrativo",
    items: [
      { icon: UserCog, label: "Usuários", path: "/usuarios", adminOnly: true },
      { icon: Settings, label: "Configurações", path: "/configuracoes" },
    ],
  },
];

export const routeTitles = [
  { path: "/dashboard", title: "Dashboard", description: "Painel executivo do ambiente" },
  { path: "/empresas", title: "Empresas", description: "Cadastro e visão fiscal por empresa" },
  { path: "/documentos", title: "Documentos", description: "Arquivos, status e processamento" },
  { path: "/obrigacoes", title: "Obrigações", description: "Calendário e acompanhamento fiscal" },
  { path: "/catalogo-obrigacoes", title: "Catálogo Fiscal", description: "Base regulatória e regras" },
  { path: "/guias", title: "Guias", description: "DAS, DARFs e recolhimentos" },
  { path: "/alertas", title: "Alertas", description: "Ocorrências e vencimentos" },
  { path: "/relatorios", title: "Relatórios", description: "Exportação e análise operacional" },
  { path: "/configuracoes", title: "Configurações", description: "Parâmetros do sistema" },
  { path: "/config-alertas", title: "Alertas", description: "Regras e notificações" },
  { path: "/robos", title: "Robôs", description: "Automação e integrações" },
  { path: "/fiscal", title: "Fiscal", description: "Painel tributário consolidado" },
  { path: "/auditoria", title: "Auditoria", description: "Trilha e conformidade" },
  { path: "/ocr", title: "OCR", description: "Leitura e extração documental" },
  { path: "/usuarios", title: "Usuários", description: "Gestão administrativa de contas" },
];

export const resolveRouteTitle = (pathname = "") => {
  const sortedRoutes = [...routeTitles].sort((a, b) => b.path.length - a.path.length);
  return (
    sortedRoutes.find(
      (route) => pathname === route.path || pathname.startsWith(`${route.path}/`)
    ) || {
      title: "SLTWEB",
      description: "Sistema de gestão fiscal integrada",
    }
  );
};

export const isMenuItemActive = (pathname, path) => {
  if (path === "/dashboard") {
    return pathname === path;
  }

  return pathname === path || pathname.startsWith(`${path}/`);
};
