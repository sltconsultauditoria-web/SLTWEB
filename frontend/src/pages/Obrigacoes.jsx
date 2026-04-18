import { useEffect, useState } from "react";
import API from "@/api";

export default function Obrigacoes() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/obrigacoes").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Obrigacoes</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
