import { useEffect, useState } from "react";
import API from "@/api";

export default function Documentos() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/documentos").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Documentos</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
