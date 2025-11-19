// src/layout/MainLayout.jsx
import { NavLink, Outlet } from "react-router-dom";

export default function MainLayout() {
  const token = localStorage.getItem("token");

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
     
      <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-xl">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <NavLink to="/" className="text-3xl font-bold tracking-tight">
            Booking
          </NavLink>

          <nav className="flex items-center gap-8 text-lg">
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive ? "underline underline-offset-4 font-semibold" : "hover:underline"
              }
            >
              Главная
            </NavLink>
            <NavLink
              to="/hotels"
              className={({ isActive }) =>
                isActive ? "underline underline-offset-4 font-semibold" : "hover:underline"
              }
            >
              Отели
            </NavLink>

            {token ? (
              <>
                <NavLink
                  to="/profile"
                  className={({ isActive }) =>
                    isActive ? "underline underline-offset-4 font-semibold" : "hover:underline"
                  }
                >
                  Мои брони
                </NavLink>
                <button
                  onClick={() => {
                    localStorage.removeItem("token");
                    window.location.href = "/login";
                  }}
                  className="bg-red-500 hover:bg-red-600 px-5 py-2 rounded-lg font-medium transition"
                >
                  Выйти
                </button>
              </>
            ) : (
              <>
                <NavLink
                  to="/login"
                  className="hover:underline"
                >
                  Войти
                </NavLink>
                <NavLink
                  to="/register"
                  className="bg-white text-indigo-600 hover:bg-gray-100 px-5 py-2 rounded-lg font-medium transition"
                >
                  Регистрация
                </NavLink>
              </>
            )}
          </nav>
        </div>
      </header>

      
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-10">
        <Outlet />
      </main>

      <footer className="bg-gray-900 text-gray-400 py-8 text-center">
        © 2025 Система бронирования отелей
      </footer>
    </div>
  );
}