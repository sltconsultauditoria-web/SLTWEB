import { useEffect, useState } from "react";

export default function hover-card() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/hover-card").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>hover-card</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
