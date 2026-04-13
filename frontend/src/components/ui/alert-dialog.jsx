import { useEffect, useState } from "react";
import API from "../api.js";

export default function alert-dialog() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/alert-dialog").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>alert-dialog</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
