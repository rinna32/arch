// src/layouts/MainLayout.jsx
import { NavLink, Outlet } from "react-router-dom";

export default function MainLayout() {
  const token = localStorage.getItem("token");

  return (
    <div className="relative min-h-screen">
      <header className="absolute inset-x-0 top-0 z-50 flex items-center justify-between px-4 py-8 md:px-6 lg:px-10 xl:px-16">

        <NavLink
          to="/"
          className="text-5xl md:text-6xl lg:text-7xl font-light tracking-widest"
          style={{
            fontFamily: '"Playfair Display", serif',
            color: "#8C7034"
          }}
        >
          LUXURY RETREATS
        </NavLink>

        <nav className="flex items-center gap-6 md:gap-10 text-xl lg:text-2xl font-light tracking-widest">
          {token ? (
            <>=
              <NavLink to="/profile" className="hover:opacity-80 transition">
                <img
                  src="/human.png"
                  alt="Profile"
                  className="w-10 h-10 md:w-12 md:h-12 rounded-full object-cover border-2"
                  style={{ borderColor: "#8C7034" }}
                />
              </NavLink>

              <button
                onClick={() => {
                  localStorage.removeItem("token");
                  window.location.href = "/";
                }}
                className="text-black hover:text-red-600 transition font-light"
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <NavLink
                to="/login"
                className="text-black hover:text-[#8C7034] transition font-light"
              >
                Войти
              </NavLink>

              <NavLink
                to="/register"
                className="bg-[#8C7034] hover:bg-[#7a5f2b] text-white px-6 py-3 rounded-full font-light transition shadow-lg"
              >
                Регистрация
              </NavLink>
            </>
          )}
        </nav>
      </header>




      <main>
        <Outlet />
      </main>
    </div>
  );
}