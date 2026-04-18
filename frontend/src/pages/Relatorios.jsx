import { useEffect, useState } from "react";
import API from "@/api";

export default function Relatorios() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/relatorios").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Relatorios</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
