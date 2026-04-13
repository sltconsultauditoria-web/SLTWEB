import { useEffect, useState } from "react";
import API from "../api.js";

export default function LoginPage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/loginpage").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>LoginPage</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
