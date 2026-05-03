
import React from "react";

export default function Dashboard() {
  const cards = [
    { title: "Empresas", value: "128" },
    { title: "Guias Pendentes", value: "19" },
    { title: "Alertas", value: "7" },
    { title: "OCR Hoje", value: "32" },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard Executivo</h1>

      <div className="grid md:grid-cols-4 gap-6">
        {cards.map((c, i) => (
          <div key={i} className="bg-white rounded-2xl shadow p-6">
            <p className="text-gray-500">{c.title}</p>
            <h2 className="text-3xl font-bold mt-2">{c.value}</h2>
          </div>
        ))}
      </div>
    </div>
  );
}
