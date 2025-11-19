// src/pages/HomePage.jsx
import { Link } from "react-router-dom";

export default function HomePage() {
  const token = localStorage.getItem("token");

  return (
    <div className="relative h-screen w-full overflow-hidden">
      <div className="absolute inset-0 bg-black/40" />

      <img
        src="/luxury-retreats.png"
        alt="Luxury Retreats"
        className="absolute inset-0 h-full w-full object-cover"
      />

      <Link
        to="/hotels"
        className="absolute bottom-20 left-1/2 -translate-x-1/2 
                   bg-[#8C7034] hover:bg-[#7a5f2b] active:bg-[#6b5525]
                   text-white font-light uppercase tracking-widest
                   px-24 py-6 rounded-full
                   text-2xl shadow-2xl transition-all duration-300
                   hover:scale-105 active:scale-95 z-10
                   border-2 border-amber-200/30"
      >
        Hotels
      </Link>

    </div>
  );
}