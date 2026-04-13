import { useEffect, useState } from "react";
import API from "../api.js";

export default function Sidebar() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/sidebar").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Sidebar</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
