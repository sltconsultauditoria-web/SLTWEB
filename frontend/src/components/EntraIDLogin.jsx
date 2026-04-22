import { useEffect, useState } from "react";
import API from "@/api";

export default function EntraIDLogin() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/entraidlogin").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>EntraIDLogin</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
