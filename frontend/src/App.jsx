import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { CatalogProvider } from './stores/catalog';
import { cartStore } from './stores/cart/cart.store';
import AppRoutes from './routes/AppRoutes';
import { ROUTES } from './core/config/routes.config';
import './core/styles/global.css';

const Header = observer(() => {
  useEffect(() => {
    cartStore.fetch();
  }, []);

  const cartCount = cartStore.totalItems;

  return (
    <header className="header">
      <div className="container">
        <Link to={ROUTES.home} className="logo">
          <span className="logo__text">Yartumba</span>
        </Link>
        <nav className="nav">
          <Link to={ROUTES.catalog.base} className="nav-link active">
            <span className="nav-link__icon">🪑</span>
            Каталог
          </Link>
          <Link to={ROUTES.configurator.base} className="nav-link">
            <span className="nav-link__icon">🔧</span>
            Конфигуратор
          </Link>
          <Link to={ROUTES.cart.base} className="nav-link cart-badge">
            <span className="nav-link__icon">🛒</span>
            Корзина
            {cartCount > 0 && (
              <span className="cart-badge__count">{cartCount}</span>
            )}
          </Link>
        </nav>
      </div>
    </header>
  );
});

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer__links">
          <a href="#" className="footer__link">О нас</a>
          <a href="#" className="footer__link">Контакты</a>
          <a href="#" className="footer__link">Доставка</a>
        </div>
        <p>© 2025 Yartumba — Мебель на заказ</p>
      </div>
    </footer>
  );
};

const App = () => {
  return (
    <CatalogProvider>
      <div className="app">
        <Header />
        <main className="main">
          <AppRoutes />
        </main>
        <Footer />
      </div>
    </CatalogProvider>
  );
};

export default App;
