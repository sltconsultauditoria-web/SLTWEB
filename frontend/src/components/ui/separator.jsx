import { useEffect, useState } from "react";

export default function separator() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/separator").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>separator</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
