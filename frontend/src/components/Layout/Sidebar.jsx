import { useEffect, useState } from "react";
import API from "@/api"; // ✅ caminho corrigido

export default function Sidebar() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/sidebar")
      .then((res) => setData(res.data))
      .catch((err) => console.error("Erro ao carregar sidebar:", err));
  }, []);

  return (
    <aside style={{ padding: "1rem", backgroundColor: "#f9f9f9" }}>
      <h2>Sidebar</h2>
      {data.length > 0 ? (
        <ul>
          {data.map((item, index) => (
            <li key={index}>{item.name || JSON.stringify(item)}</li>
          ))}
        </ul>
      ) : (
        <p>Nenhum dado encontrado.</p>
      )}
    </aside>
  );
}
