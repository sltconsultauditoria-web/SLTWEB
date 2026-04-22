import { useEffect, useState } from "react";

export default function accordion() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/accordion").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>accordion</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
