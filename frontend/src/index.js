import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App";

// Ponto de montagem: div id="root" no index.html
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <BrowserRouter basename="/consultSLTweb">
      <Routes>
        {/* Rota principal da aplicação */}
        <Route path="/" element={<App />} />
        {/* Se quiser acessar diretamente /consultSLTweb */}
        <Route path="/consultSLTweb" element={<App />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
