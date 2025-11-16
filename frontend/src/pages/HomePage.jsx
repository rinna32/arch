import React from 'react'

export default function HomePage() {

    const [hotels, setHotels] = useState([]);

    useEffect(() => {
        API.get('/hotels/')
        .then(res => setHotels(res.data))
        .catch(err => console.log(err));
    }, []);
    return (
        <div className="container py-5">
      <h1 className="mb-4">Каталог отелей</h1>
      <div className="row">
        {hotels.map(hotel => (
          <div key={hotel.id} className="col-md-4 mb-4">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">{hotel.name}</h5>
                <p>
                  <strong>Город:</strong> {hotel.city}<br/>
                  <strong>Рейтинг:</strong> {'★'.repeat(hotel.rating)}
                </p>
                <Link to={`/book/${hotel.id}`} className="btn btn-primary">
                  Забронировать
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
       
    )
}
