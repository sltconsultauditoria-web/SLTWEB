import { useEffect, useState } from "react";
import API from "../api.js";

export default function menubar() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/menubar").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>menubar</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
