import { useEffect, useState } from "react";
import API from "@/api";

export default function FiscalList() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/fiscallist").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>FiscalList</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
