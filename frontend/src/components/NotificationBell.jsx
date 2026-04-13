import { useEffect, useState } from "react";
import API from "../api.js";

export default function NotificationBell() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/notificationbell").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>NotificationBell</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
