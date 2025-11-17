// frontend/src/App.jsx
import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [hotels, setHotels] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    if (token) {
      loadHotels();
    }
  }, [token]);

  const loadHotels = async () => {
    try {
      const res = await axios.get(`${API_URL}/hotels/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHotels(res.data);
    } catch (err) {
      console.log("Ошибка загрузки:", err.response?.data);
    }
  };

  const login = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_URL}/login/`, { username, password });
      const newToken = res.data.access;
      localStorage.setItem("token", newToken);
      setToken(newToken);
    } catch (err) {
      alert("Ошибка входа: " + (err.response?.data?.detail || "Неверные данные"));
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken("");
    setHotels([]);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Бронирование отелей</h1>

      {!token ? (
        <form onSubmit={login}>
          <input
            placeholder="Логин"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ margin: "5px", padding: "8px" }}
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ margin: "5px", padding: "8px" }}
          />
          <button type="submit" style={{ padding: "8px 16px" }}>
            Войти
          </button>
        </form>
      ) : (
        <div>
          <button onClick={logout} style={{ marginBottom: "20px" }}>
            Выйти
          </button>
          <h2>Отели</h2>
          {hotels.length === 0 ? (
            <p>Загрузка отелей...</p>
          ) : (
            hotels.map((h) => (
              <div
                key={h.id}
                style={{
                  border: "1px solid #ccc",
                  margin: "10px",
                  padding: "10px",
                  borderRadius: "8px",
                }}
              >
                <h3>{h.name}</h3>
                <p>
                  {h.city} ★ {h.rating}
                </p>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default App;