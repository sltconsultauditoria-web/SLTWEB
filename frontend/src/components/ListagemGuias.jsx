import { useEffect, useState } from "react";
import API from "@/api";

export default function ListagemGuias() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/listagemguias").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>ListagemGuias</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
