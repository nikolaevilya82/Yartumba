import React, { useEffect, useState } from 'react';
import { observer } from 'mobx-react-lite';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../core/config/routes.config';
import { cartStore } from '../../stores/cart/cart.store';
import { cartActions } from '../../stores/cart/cart.actions';
import { cartPromocodeStore } from '../../stores/cart/cart.promocode';
import { furnitureTypeNames } from '../../core/constants/product.constants';
import './CartPage.css';

const CartPage = observer(() => {
  const [promocodeInput, setPromocodeInput] = useState('');
  const [isApplyingPromo, setIsApplyingPromo] = useState(false);

  useEffect(() => {
    cartStore.fetch();
  }, []);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      maximumFractionDigits: 0,
    }).format(price);
  };

  const getTypeLabel = (type) => {
    return furnitureTypeNames[type] || type;
  };

  const getIcon = (type) => {
    const icons = {
      bookshelf: '📚',
      nightstand: '🛏️',
      dresser: '🗄️',
    };
    return icons[type] || '🪑';
  };

  const handleIncrement = async (itemId) => {
    await cartActions.increment(itemId);
  };

  const handleDecrement = async (itemId) => {
    await cartActions.decrement(itemId);
  };

  const handleRemove = async (itemId) => {
    await cartActions.removeItem(itemId);
  };

  const handleApplyPromocode = async () => {
    if (!promocodeInput.trim()) return;
    
    setIsApplyingPromo(true);
    const result = await cartActions.applyPromocode(promocodeInput.trim());
    if (result.success) {
      setPromocodeInput('');
    }
    setIsApplyingPromo(false);
  };

  const handleRemovePromocode = async () => {
    await cartActions.removePromocode();
  };

  const handleClearCart = async () => {
    if (window.confirm('Очистить корзину?')) {
      await cartActions.clear();
    }
  };

  const handleCheckout = () => {
    // TODO: Переход к оформлению заказа
    alert('Функция оформления заказа в разработке');
  };

  const { items, totalItems, totalPrice, discountedPrice, isEmpty, isLoading } = cartStore;
  const { hasDiscount, discount } = cartPromocodeStore;

  // Состояние загрузки
  if (isLoading) {
    return (
      <div className="cart-page">
        <div className="container">
          <h1 className="page-title">Корзина</h1>
          <p className="page-subtitle">Загрузка...</p>
          <div className="cart-loading">
            <div className="spinner"></div>
          </div>
        </div>
      </div>
    );
  }

  // Пустая корзина
  if (isEmpty) {
    return (
      <div className="cart-page">
        <div className="container">
          <h1 className="page-title">Корзина</h1>
          <p className="page-subtitle">Ваши выбранные товары</p>
          
          <div className="cart-page__empty">
            <div className="empty-content">
              <span className="empty-icon">🛒</span>
              <h2>Корзина пуста</h2>
              <p>Добавьте товары из каталога</p>
              <Link to={ROUTES.catalog.base} className="btn btn-primary btn-lg">
                Перейти в каталог
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Товары в корзине
  return (
    <div className="cart-page">
      <div className="container">
        <h1 className="page-title">Корзина</h1>
        <p className="page-subtitle">{totalItems} {totalItems === 1 ? 'товар' : totalItems < 5 ? 'товара' : 'товаров'}</p>
        
        <div className="cart-content">
          <div className="cart-items">
            {items.map((item) => (
              <div key={item.id} className="cart-item">
                <div className="cart-item__type-icon">
                  {getIcon(item.furniture_type)}
                </div>
                
                <div className="cart-item__info">
                  <h3 className="cart-item__name">
                    {item.configuration?.name || `${getTypeLabel(item.furniture_type)} #${item.furniture_id.slice(0, 8)}`}
                  </h3>
                  
                  {item.configuration && (
                    <div className="cart-item__details">
                      {item.configuration.width && item.configuration.height && item.configuration.depth && (
                        <span className="cart-item__dimension">
                          {item.configuration.width}×{item.configuration.height}×{item.configuration.depth} мм
                        </span>
                      )}
                      {item.configuration.material_name && (
                        <span className="cart-item__material">{item.configuration.material_name}</span>
                      )}
                      {item.configuration.shelf_count && (
                        <span className="cart-item__feature">{item.configuration.shelf_count} полок</span>
                      )}
                      {item.configuration.drawer_count && (
                        <span className="cart-item__feature">{item.configuration.drawer_count} ящиков</span>
                      )}
                    </div>
                  )}
                </div>
                
                <div className="cart-item__price">
                  {formatPrice(item.unit_price)}
                </div>
                
                <div className="cart-item__quantity">
                  <button
                    className="quantity-btn"
                    onClick={() => handleDecrement(item.id)}
                    disabled={item.quantity <= 1}
                  >
                    −
                  </button>
                  <span className="quantity-value">{item.quantity}</span>
                  <button
                    className="quantity-btn"
                    onClick={() => handleIncrement(item.id)}
                  >
                    +
                  </button>
                </div>
                
                <div className="cart-item__total">
                  {formatPrice(item.unit_price * item.quantity)}
                </div>
                
                <button
                  className="cart-item__remove"
                  onClick={() => handleRemove(item.id)}
                  title="Удалить"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
          
          <div className="cart-summary">
            <div className="summary-card">
              <h3 className="summary-title">Итого</h3>
              
              <div className="summary-row">
                <span className="summary-label">Товары ({totalItems})</span>
                <span className="summary-value">{formatPrice(totalPrice)}</span>
              </div>
              
              {hasDiscount && (
                <div className="summary-row discount">
                  <span className="summary-label">Скидка ({discount}%)</span>
                  <span className="summary-value">-{formatPrice(totalPrice - discountedPrice)}</span>
                </div>
              )}
              
              <div className="summary-row total">
                <span className="summary-label">К оплате</span>
                <span className="summary-value">{formatPrice(discountedPrice)}</span>
              </div>
              
              {hasDiscount && (
                <div className="promocode-applied">
                  <span>🎉 Промокод <strong>{cartPromocodeStore.promocode}</strong> активирован</span>
                  <button
                    className="promocode-remove"
                    onClick={handleRemovePromocode}
                  >
                    Отменить
                  </button>
                </div>
              )}
              
              <div className="promocode-input">
                <input
                  type="text"
                  placeholder="Введите промокод"
                  value={promocodeInput}
                  onChange={(e) => setPromocodeInput(e.target.value)}
                  disabled={hasDiscount}
                />
                <button
                  className="btn btn-secondary"
                  onClick={handleApplyPromocode}
                  disabled={!promocodeInput.trim() || hasDiscount || isApplyingPromo}
                >
                  {isApplyingPromo ? 'Проверка...' : 'Применить'}
                </button>
              </div>
              
              <button
                className="btn btn-primary btn-lg btn-block"
                onClick={handleCheckout}
              >
                Оформить заказ
              </button>
              
              <button
                className="btn btn-outline btn-block"
                onClick={handleClearCart}
              >
                Очистить корзину
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
});

export default CartPage;
