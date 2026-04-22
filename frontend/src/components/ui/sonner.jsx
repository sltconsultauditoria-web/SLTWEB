import { useEffect, useState } from "react";

export default function sonner() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/sonner").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>sonner</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
