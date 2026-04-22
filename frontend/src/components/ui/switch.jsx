import { useState } from "react";

export function Switch(props) {
  const [checked, setChecked] = useState(false);
  return (
    <input
      type="checkbox"
      checked={checked}
      onChange={() => setChecked(!checked)}
      {...props}
    />
  );
}
