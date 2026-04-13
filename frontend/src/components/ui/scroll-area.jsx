import { useEffect, useState } from "react";
import API from "../api.js";

export default function scroll-area() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/scroll-area").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>scroll-area</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
