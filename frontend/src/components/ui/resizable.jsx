import { useEffect, useState } from "react";

export default function resizable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/resizable").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>resizable</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
