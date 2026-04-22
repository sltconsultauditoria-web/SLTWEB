import { useEffect, useState } from "react";

export default function form() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/form").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>form</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
