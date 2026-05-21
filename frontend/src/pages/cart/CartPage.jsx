import React from 'react';
import './CartPage.css';

const CartPage = () => {
  return (
    <div className="cart-page">
      <div className="container">
        <h1 className="page-title">Корзина</h1>
        <p className="page-subtitle">Ваши выбранные товары</p>
        
        <div className="cart-page__placeholder">
          <div className="placeholder-content">
            <span className="placeholder-icon">🛒</span>
            <h2>Корзина пуста</h2>
            <p>Добавьте товары из каталога</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
