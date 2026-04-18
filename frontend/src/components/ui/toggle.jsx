import { useEffect, useState } from "react";

export default function toggle() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/toggle").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>toggle</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
