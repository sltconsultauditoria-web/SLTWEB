import { useEffect, useState } from "react";
import API from "../api.js";

export default function toast() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/toast").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>toast</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
