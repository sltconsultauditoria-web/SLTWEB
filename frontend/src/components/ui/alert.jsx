import { useEffect, useState } from "react";
import API from "../api.js";

export default function alert() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/alert").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>alert</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
