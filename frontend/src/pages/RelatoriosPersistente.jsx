import { useEffect, useState } from "react";
import API from "@/api";

export default function RelatoriosPersistente() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/relatoriospersistente").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>RelatoriosPersistente</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
