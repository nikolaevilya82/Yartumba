import React, { useState } from 'react';
import { observer } from 'mobx-react-lite';
import { useNavigate, Link } from 'react-router-dom';
import { ROUTES } from '../../core/config/routes.config';
import { cartStore } from '../../stores/cart/cart.store';
import { furnitureTypeNames } from '../../core/constants/product.constants';
import './CheckoutPage.css';

const CheckoutPage = observer(() => {
  const navigate = useNavigate();
  const { items, totalItems, totalPrice, discountedPrice, isEmpty, isLoading } = cartStore;

  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    deliveryMethod: 'pickup', // 'pickup' | 'courier'
    address: '',
    comment: '',
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Сбрасываем ошибку при изменении поля
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Укажите ваше имя';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Укажите номер телефона';
    } else if (!/^[\d\s+\-()]{7,20}$/.test(formData.phone.trim())) {
      newErrors.phone = 'Введите корректный номер телефона';
    }

    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Введите корректный email';
    }

    if (formData.deliveryMethod === 'courier' && !formData.address.trim()) {
      newErrors.address = 'Укажите адрес доставки';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) return;

    setIsSubmitting(true);

    // TODO: Отправить заказ на бэкенд
    // const orderData = {
    //   customer: {
    //     name: formData.name,
    //     phone: formData.phone,
    //     email: formData.email || undefined,
    //     address: formData.deliveryMethod === 'courier' ? formData.address : undefined,
    //     comment: formData.comment || undefined,
    //   },
    //   items: items.map(item => ({ id: item.id, quantity: item.quantity })),
    //   delivery_method: formData.deliveryMethod,
    // };
    // await cartService.createOrder(orderData);

    // Имитируем отправку
    await new Promise((resolve) => setTimeout(resolve, 1200));

    setIsSubmitting(false);
    setSubmitted(true);
  };

  // Экран успеха после отправки
  if (submitted) {
    return (
      <div className="checkout-page">
        <div className="container">
          <div className="checkout-success">
            <div className="success-content">
              <span className="success-icon">✅</span>
              <h1>Заказ оформлен!</h1>
              <p className="success-subtitle">
                Спасибо, <strong>{formData.name}</strong>! Ваш заказ принят.
              </p>
              <div className="success-details">
                <p>Номер заказа: <strong>#{Math.random().toString(36).slice(2, 8).toUpperCase()}</strong></p>
                <p>Сумма: <strong>{formatPrice(discountedPrice)}</strong></p>
                <p>Способ получения: <strong>{formData.deliveryMethod === 'pickup' ? 'Самовывоз' : 'Доставка'}</strong></p>
              </div>
              <p className="success-note">
                В ближайшее время с вами свяжется наш менеджер для подтверждения заказа.
              </p>
              <div className="success-actions">
                <Link to={ROUTES.catalog.base} className="btn btn-primary btn-lg">
                  Вернуться в каталог
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Загрузка
  if (isLoading) {
    return (
      <div className="checkout-page">
        <div className="container">
          <h1 className="page-title">Оформление заказа</h1>
          <div className="checkout-loading">
            <div className="spinner"></div>
            <p>Загрузка корзины...</p>
          </div>
        </div>
      </div>
    );
  }

  // Пустая корзина
  if (isEmpty) {
    return (
      <div className="checkout-page">
        <div className="container">
          <h1 className="page-title">Оформление заказа</h1>
          <div className="checkout-empty">
            <div className="empty-content">
              <span className="empty-icon">🛒</span>
              <h2>Корзина пуста</h2>
              <p>Добавьте товары из каталога, чтобы оформить заказ</p>
              <Link to={ROUTES.catalog.base} className="btn btn-primary btn-lg">
                Перейти в каталог
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="checkout-page">
      <div className="container">
        <div className="checkout-header">
          <h1 className="page-title">Оформление заказа</h1>
          <p className="page-subtitle">Заполните данные для оформления</p>
        </div>

        <div className="checkout-layout">
          {/* Форма */}
          <form className="checkout-form" onSubmit={handleSubmit} noValidate>
            <div className="checkout-section">
              <h2 className="section-title">Контактные данные</h2>

              <div className="form-group">
                <label className="form-label" htmlFor="name">
                  ФИО <span className="required">*</span>
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  className={`form-input ${errors.name ? 'form-input--error' : ''}`}
                  placeholder="Иванов Иван Иванович"
                  value={formData.name}
                  onChange={handleChange}
                  disabled={isSubmitting}
                />
                {errors.name && <span className="form-error">{errors.name}</span>}
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="phone">
                  Телефон <span className="required">*</span>
                </label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  className={`form-input ${errors.phone ? 'form-input--error' : ''}`}
                  placeholder="+7 (999) 123-45-67"
                  value={formData.phone}
                  onChange={handleChange}
                  disabled={isSubmitting}
                />
                {errors.phone && <span className="form-error">{errors.phone}</span>}
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="email">
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  className={`form-input ${errors.email ? 'form-input--error' : ''}`}
                  placeholder="ivan@example.com"
                  value={formData.email}
                  onChange={handleChange}
                  disabled={isSubmitting}
                />
                {errors.email && <span className="form-error">{errors.email}</span>}
                <span className="form-hint">Для отправки подтверждения заказа</span>
              </div>
            </div>

            <div className="checkout-section">
              <h2 className="section-title">Способ получения</h2>

              <div className="delivery-options">
                <label className="delivery-option">
                  <input
                    type="radio"
                    name="deliveryMethod"
                    value="pickup"
                    checked={formData.deliveryMethod === 'pickup'}
                    onChange={handleChange}
                    disabled={isSubmitting}
                  />
                  <div className="delivery-option__content">
                    <span className="delivery-option__title">Самовывоз</span>
                    <span className="delivery-option__desc">г. Москва, ул. Тверская, 10, ежедневно с 10:00 до 20:00</span>
                  </div>
                </label>

                <label className="delivery-option">
                  <input
                    type="radio"
                    name="deliveryMethod"
                    value="courier"
                    checked={formData.deliveryMethod === 'courier'}
                    onChange={handleChange}
                    disabled={isSubmitting}
                  />
                  <div className="delivery-option__content">
                    <span className="delivery-option__title">Доставка курьером</span>
                    <span className="delivery-option__desc">По Москве и области, от 2 до 7 рабочих дней</span>
                  </div>
                </label>
              </div>

              {formData.deliveryMethod === 'courier' && (
                <div className="form-group">
                  <label className="form-label" htmlFor="address">
                    Адрес доставки <span className="required">*</span>
                  </label>
                  <textarea
                    id="address"
                    name="address"
                    className={`form-input form-textarea ${errors.address ? 'form-input--error' : ''}`}
                    placeholder="г. Москва, ул. Примерная, д. 1, кв. 1"
                    value={formData.address}
                    onChange={handleChange}
                    rows={3}
                    disabled={isSubmitting}
                  />
                  {errors.address && <span className="form-error">{errors.address}</span>}
                </div>
              )}
            </div>

            <div className="checkout-section">
              <h2 className="section-title">Комментарий к заказу</h2>
              <div className="form-group">
                <textarea
                  id="comment"
                  name="comment"
                  className="form-input form-textarea"
                  placeholder="Дополнительные пожелания..."
                  value={formData.comment}
                  onChange={handleChange}
                  rows={3}
                  disabled={isSubmitting}
                />
              </div>
            </div>
          </form>

          {/* Сводка заказа */}
          <div className="checkout-summary">
            <div className="summary-card">
              <h3 className="summary-title">Ваш заказ</h3>

              <div className="summary-items">
                {items.map((item) => (
                  <div key={item.id} className="summary-item">
                    <div className="summary-item__icon">{getIcon(item.furniture_type)}</div>
                    <div className="summary-item__info">
                      <span className="summary-item__name">
                        {item.configuration?.name || `${getTypeLabel(item.furniture_type)}`}
                      </span>
                      {item.configuration?.width && (
                        <span className="summary-item__dimension">
                          {item.configuration.width}×{item.configuration.height}×{item.configuration.depth} мм
                        </span>
                      )}
                    </div>
                    <div className="summary-item__quantity">×{item.quantity}</div>
                    <div className="summary-item__price">{formatPrice(item.unit_price * item.quantity)}</div>
                  </div>
                ))}
              </div>

              <div className="summary-totals">
                <div className="summary-row">
                  <span className="summary-label">Товары ({totalItems})</span>
                  <span className="summary-value">{formatPrice(totalPrice)}</span>
                </div>

                {cartStore.discountedPrice !== totalPrice && (
                  <div className="summary-row discount">
                    <span className="summary-label">Скидка</span>
                    <span className="summary-value">-{formatPrice(totalPrice - discountedPrice)}</span>
                  </div>
                )}

                {formData.deliveryMethod === 'courier' && (
                  <div className="summary-row">
                    <span className="summary-label">Доставка</span>
                    <span className="summary-value">{formatPrice(0)}</span>
                  </div>
                )}

                <div className="summary-row total">
                  <span className="summary-label">К оплате</span>
                  <span className="summary-value">{formatPrice(discountedPrice)}</span>
                </div>
              </div>

              <button
                className="btn btn-primary btn-lg btn-block"
                onClick={handleSubmit}
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Оформляем...' : 'Подтвердить заказ'}
              </button>

              <Link
                to={ROUTES.cart.base}
                className="btn btn-outline btn-block"
              >
                Вернуться в корзину
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
});

export default CheckoutPage;