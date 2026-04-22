import { useEffect, useState } from "react";
import API from "@/api";

export default function RecibosSharePoint() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/recibossharepoint").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>RecibosSharePoint</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
