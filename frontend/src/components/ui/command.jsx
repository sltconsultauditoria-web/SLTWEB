import { useEffect, useState } from "react";
import API from "../api.js";

export default function command() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/command").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>command</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
