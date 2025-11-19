// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { router } from "./routes";
import { RouterProvider } from "react-router-dom";

// Это ОБЯЗАТЕЛЬНО для createBrowserRouter + Vite
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);