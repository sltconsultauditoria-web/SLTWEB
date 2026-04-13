import { useEffect, useState } from "react";
import API from "../api.js";

export default function ConfiguracaoAlertas() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/configuracaoalertas").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>ConfiguracaoAlertas</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
