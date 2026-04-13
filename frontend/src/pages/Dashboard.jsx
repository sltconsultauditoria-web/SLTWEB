import { useEffect, useState } from "react";
import API from "../api.js";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/dashboard").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
