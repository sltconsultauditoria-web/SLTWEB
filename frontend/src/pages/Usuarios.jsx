import { useEffect, useState } from "react";
import API from "../api.js";

export default function Usuarios() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/usuarios").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Usuarios</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
