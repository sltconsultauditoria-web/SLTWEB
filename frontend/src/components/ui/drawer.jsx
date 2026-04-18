import { useEffect, useState } from "react";

export default function drawer() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/drawer").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>drawer</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
