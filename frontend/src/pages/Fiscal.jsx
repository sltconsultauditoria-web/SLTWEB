import { useEffect, useState } from "react";
import API from "@/api";

export default function Fiscal() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/fiscal").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Fiscal</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
