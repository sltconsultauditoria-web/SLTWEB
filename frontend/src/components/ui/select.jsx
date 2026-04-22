import { useEffect, useState } from "react";

export default function select() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/select").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>select</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
