import { useEffect, useState } from "react";

export default function popover() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/popover").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>popover</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
