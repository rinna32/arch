import { Link } from 'react-router-dom';

function Navbar() {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <Link className="navbar-brand" to="/">Магазин</Link>
            <div className="navbar-nav">
                <Link className="nav-link" to="/products">Товары</Link>
                <Link className="nav-link" to="/cart">Корзина</Link>
                <Link className="nav-link" to="/profile">Профиль</Link>
            </div>
        </nav>
    );
}