import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

function ProductsPage() {
    const [products, setProducts] = useState(window.__INITIAL_PROPS__.products || []);
    const location = useLocation();

    // Если переход по react-router — подгружаем данные
    useEffect(() => {
        if (!window.__INITIAL_PROPS__.products) {
            fetch('/api/products/' + location.search)
                .then(r => r.json())
                .then(setProducts);
        }
    }, [location]);

    return (
        <div className="container">
            <h1>Товары</h1>
            <div className="row">
                {products.map(p => (
                    <div className="col-md-4" key={p.id}>
                        <div className="card">
                            <img src={p.image} className="card-img-top" />
                            <div className="card-body">
                                <h5>{p.name}</h5>
                                <p>{p.price} ₽</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ProductsPage;