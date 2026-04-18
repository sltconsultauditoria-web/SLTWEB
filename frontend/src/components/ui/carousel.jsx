import { useEffect, useState } from "react";

export default function carousel() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/carousel").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>carousel</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
