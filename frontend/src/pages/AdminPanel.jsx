import { useState, useEffect } from 'react';
import API from '../services/api';

export default function AdminPanel() {
  const [hotels, setHotels] = useState([]);
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    API.get('/hotels/').then(res => setHotels(res.data));
    API.get('/bookings/').then(res => setBookings(res.data));
  }, []);

  const confirmBooking = async (id) => {
    await API.patch(`/bookings/${id}/`, { status: 'confirmed' });
    setBookings(bookings.map(b => b.id === id ? { ...b, status: 'confirmed' } : b));
  };

  return (
    <div className="container py-5">
      <h1>Админ-панель</h1>

      <h3>Брони</h3>
      <div className="row">
        {bookings.map(b => (
          <div key={b.id} className="col-md-4 mb-3">
            <div className="card">
              <div className="card-body">
                <p><strong>{b.user}</strong> → {b.hotel_name}</p>
                <p>{b.check_in} → {b.check_out}</p>
                <p>Статус: <span className="badge bg-warning">{b.status}</span></p>
                {b.status === 'pending' && (
                  <button className="btn btn-success btn-sm" onClick={() => confirmBooking(b.id)}>
                    Подтвердить
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}