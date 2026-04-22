import { useEffect, useState } from "react";

export default function calendar() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/calendar").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>calendar</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
