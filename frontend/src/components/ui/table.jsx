import { useEffect, useState } from "react";

export default function table() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/table").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>table</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
