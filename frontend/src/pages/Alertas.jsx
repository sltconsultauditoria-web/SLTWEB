import { useEffect, useState } from "react";
import API from "@/api";

export default function Alertas() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/alertas").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Alertas</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
