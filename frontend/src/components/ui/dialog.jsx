import { useEffect, useState } from "react";
import API from "../api.js";

export default function dialog() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/dialog").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>dialog</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
