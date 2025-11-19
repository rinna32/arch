// src/routes.jsx (или routes.tsx)

import { createBrowserRouter } from "react-router-dom";

// Layout
import MainLayout from "./pages/MainLayout";        // ← Правильный путь! У тебя MainLayout в папке layout, а не pages

// Страницы
import HomePage from "./pages/HomePage";
import Hotels from "./pages/Hotels";              // ← Список всех отелей (галерея)
import HotelsPage from "./pages/HotelsPage";      // ← Детальная страница одного отеля
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AdminPanel from "./pages/AdminPanel";
import ProfilePage from "./pages/ProfilePage";    // ← если будет потом

export const router = createBrowserRouter([
  {
    Component: MainLayout,
    children: [
      {
        index: true,           // → /
        Component: HomePage,
      },
      {
        path: "hotels",         // → /hotels
        Component: Hotels,      // ← Галерея всех 20 отелей
      },
      {
        path: "hotel",          // → /hotel  (или можно "hotelspage" — как хочешь)
        Component: HotelsPage,  // ← Детальная страница выбранного отеля + бронирование
      },
      {
        path: "login",
        Component: LoginPage,
      },
      {
        path: "register",
        Component: RegisterPage,
      },
      {
        path: "profile",
        Component: ProfilePage,
      },
      {
        path: "admin",
        Component: AdminPanel,
      },
    ],
  },
]);