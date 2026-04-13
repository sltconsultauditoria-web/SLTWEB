import { useEffect, useState } from "react";
import API from "../api.js";

export default function ForgotPasswordPage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/forgotpasswordpage").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>ForgotPasswordPage</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
