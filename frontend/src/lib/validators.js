import { useEffect, useState } from "react";
import API from "@/api";

export default function validators() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/validators").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>validators</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
