import { useEffect, useState } from "react";
import API from "../api.js";

export default function checkbox() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/checkbox").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>checkbox</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
