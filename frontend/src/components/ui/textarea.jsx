import { useEffect, useState } from "react";
import API from "../api.js";

export default function textarea() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/textarea").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>textarea</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
