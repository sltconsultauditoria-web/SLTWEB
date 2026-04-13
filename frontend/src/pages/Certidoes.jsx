import { useEffect, useState } from "react";
import API from "../api.js";

export default function Certidoes() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/certidoes").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>Certidoes</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
