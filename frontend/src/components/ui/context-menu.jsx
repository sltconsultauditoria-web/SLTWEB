import { useEffect, useState } from "react";

export default function context-menu() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/context-menu").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>context-menu</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
