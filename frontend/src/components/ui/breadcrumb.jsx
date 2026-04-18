import { useEffect, useState } from "react";

export default function breadcrumb() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/breadcrumb").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>breadcrumb</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
