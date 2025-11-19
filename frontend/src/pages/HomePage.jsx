// src/pages/HomePage.jsx
import { NavLink } from "react-router-dom";

export default function HomePage() {
  const token = localStorage.getItem("token");

  return (
    <div className="relative h-screen w-full overflow-hidden">
      
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage:
            "url('https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?q=80&w=2070&auto=format&fit=crop')",
        }}
      >
        <div className="absolute inset-0 bg-black/30" />
      </div>

     
      <div className="relative h-full flex flex-col justify-between text-white">
        
        <div className="flex justify-between items-center px-10 pt-8">
          <h1 className="text-6xl font-thin tracking-widest text-amber-100">
            LUXURY RETREATS
          </h1>

          <div className="flex items-center gap-8 text-lg">
            <NavLink
              to="/hotels"
              className="hover:text-amber-200 transition duration-300"
            >
              HOTELS
            </NavLink>

            <NavLink
              to={token ? "/profile" : "/login"}   
              className="hover:text-amber-200 transition duration-300"
            >
              {token ? "My Bookings" : "Login"}
            </NavLink>
          </div>
        </div>

        {/* Центральная кнопка */}
        <div className="flex justify-center pb-32">
          <NavLink to="/hotels">
            <button className="bg-amber-600 hover:bg-amber-700 text-white font-medium text-xl tracking-widest px-16 py-6 rounded-full shadow-2xl transform hover:scale-105 transition duration-500">
              HOTELS
            </button>
          </NavLink>
        </div>
      </div>
    </div>
  );
}