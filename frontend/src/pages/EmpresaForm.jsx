import { useEffect, useState } from "react";
import API from "../api.js";

export default function EmpresaForm() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/empresaform").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>EmpresaForm</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
