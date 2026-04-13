import { useEffect, useState } from "react";
import API from "../api.js";

export default function navigation-menu() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/navigation-menu").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>navigation-menu</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
