import { useEffect, useState } from "react";
import API from "@/api";

export default function Auditoria() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/auditoria").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Auditoria</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
