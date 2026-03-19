import React, { useEffect, useState } from "react";

function NotificationBell({ userId }) {
  const [count, setCount] = useState(0);

  const backendUrl =
    process.env.REACT_APP_BACKEND_URL.replace("http", "ws");

  useEffect(() => {
    if (!userId) return;

      `${backendUrl}/ws/notifications/${userId}`
    );

    ws.onopen = () => {
      console.log("WS conectado");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "new_notification") {
        setCount((prev) => prev + 1);
      }
    };

    ws.onerror = (error) => {
      console.error("Erro WS:", error);
    };

    return () => ws.close();
  }, [userId]);

  return (
    <div style={{ position: "relative", fontSize: "22px" }}>
      🔔
      {count > 0 && (
        <span
          style={{
            position: "absolute",
            top: "-5px",
            right: "-10px",
            background: "red",
            color: "white",
            borderRadius: "50%",
            padding: "3px 7px",
            fontSize: "12px"
          }}
        >
          {count}
        </span>
      )}
    </div>
  );
}

export default NotificationBell;
