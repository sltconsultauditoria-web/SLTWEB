
import React from "react";
import { Link, Outlet } from "react-router-dom";

export default function EnterpriseLayout() {
  return (
    <div className="min-h-screen bg-slate-100 flex">
      
      {/* Sidebar */}
      <aside className="w-72 bg-slate-900 text-white p-6 hidden md:block">
        <h1 className="text-2xl font-bold mb-8">CONSULTSLT</h1>

        <nav className="space-y-3 text-sm">
          <Link to="/dashboard" className="block hover:text-cyan-400">Dashboard</Link>
          <Link to="/empresas" className="block hover:text-cyan-400">Empresas</Link>
          <Link to="/guias" className="block hover:text-cyan-400">Guias</Link>
          <Link to="/documentos" className="block hover:text-cyan-400">Documentos</Link>
          <Link to="/alertas" className="block hover:text-cyan-400">Alertas</Link>
          <Link to="/relatorios" className="block hover:text-cyan-400">Relatórios</Link>
          <Link to="/ocr" className="block hover:text-cyan-400">OCR</Link>
        </nav>
      </aside>

      {/* Content */}
      <main className="flex-1">

        <header className="bg-white shadow px-8 py-4 flex justify-between">
          <h2 className="font-semibold text-lg">Painel Corporativo</h2>
          <span className="text-sm text-gray-500">consultSLTweb</span>
        </header>

        <section className="p-8">
          <Outlet />
        </section>

      </main>
    </div>
  );
}
