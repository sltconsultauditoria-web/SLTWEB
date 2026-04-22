import { useEffect, useState } from "react";

export default function dropdown-menu() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/dropdown-menu").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>dropdown-menu</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
