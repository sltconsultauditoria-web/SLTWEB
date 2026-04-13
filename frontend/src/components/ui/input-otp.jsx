import { useEffect, useState } from "react";
import API from "../api.js";

export default function input-otp() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/input-otp").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>input-otp</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
