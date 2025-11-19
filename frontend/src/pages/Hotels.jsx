// src/pages/Hotels.jsx
import { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
import { message, Spin } from "antd";

// Резервный список отелей (работает даже без интернета!)
const FALLBACK_HOTELS = [
  { id: 1, name: "Гостиница \"Питер\"", city: "Санкт-Петербург", description: "Уютная гостиница недалеко от Эрмитажа и Невского проспекта.", rating: 4 },
  { id: 2, name: "Отель \"Зелёный двор\"", city: "Казань", description: "Современный отель в центре татарской столицы с видом на Кремль.", rating: 4 },
  { id: 3, name: "Бутик-отель \"Северное сияние\"", city: "Мурманск", description: "Идеальное место для наблюдения за полярным сиянием.", rating: 5 },
  { id: 4, name: "Пансионат \"Волна\"", city: "Сочи", description: "Прямо у моря, с собственным пляжем и спа-комплексом.", rating: 4 },
  { id: 5, name: "Гранд-отель \"Империал\"", city: "Москва", description: "Роскошь в самом сердце столицы, рядом с Красной площадью.", rating: 5 },
];

export default function Hotels() {
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://hotels-api-eiwu.onrender.com/api/hotels")
      .then(res => {
        if (!res.ok) throw new Error("API недоступен");
        return res.json();
      })
      .then(data => {
        const hotelArray = Array.isArray(data) ? data : [];
        setHotels(hotelArray.length > 0 ? hotelArray : FALLBACK_HOTELS);
      })
      .catch(() => {
        // Если API не отвечает — показываем красивые отели из резерва
        message.warning("Показываем демо-отели — сервер временно недоступен");
        setHotels(FALLBACK_HOTELS);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="pt-32 pb-24 flex justify-center items-center min-h-screen">
        <Spin size="large" tip="Загрузка эксклюзивных отелей..." />
      </div>
    );
  }

  return (
    <div className="pt-32 pb-24 px-4 md:px-8 lg:px-16">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 max-w-7xl mx-auto">

        {hotels.map((hotel) => (
          <div key={hotel.id} className="flex flex-col items-center group">
            <div className="overflow-hidden rounded-3xl shadow-2xl mb-6 w-full">
              <img
                src={`https://picsum.photos/800/900?random=${hotel.id}`}
                alt={hotel.name}
                className="w-full h-96 object-cover transition-transform duration-700 group-hover:scale-110"
              />
            </div>

            <p className="text-center text-gray-600 font-light tracking-wide text-sm md:text-base mb-6 max-w-xs px-4">
              {hotel.description}
            </p>

            <NavLink
              to="/hotel"
              state={{ hotel: { ...hotel, room_types: [
                { id: 1, name: "Стандарт", capacity: 2, price_per_night: 8000 },
                { id: 2, name: "Люкс", capacity: 2, price_per_night: 15000 },
                { id: 3, name: "Апартаменты", capacity: 4, price_per_night: 22000 },
              ]}}}
              className="bg-[#8C7034] hover:bg-[#7a5f2b] active:bg-[#6b5525]
                         text-white font-light uppercase tracking-widest
                         px-12 py-4 rounded-full text-lg
                         shadow-xl transition-all duration-300
                         hover:scale-105 active:scale-95"
            >
              {hotel.name}
            </NavLink>
          </div>
        ))}

      </div>
    </div>
  );
}