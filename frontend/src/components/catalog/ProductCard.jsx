import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../core/config/routes.config';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const { id, name, furniture_type, base_price, image_url, description } = product;
  
  const getTypeLabel = (type) => {
    const labels = {
      bookshelf: 'Книжная полка',
      nightstand: 'Прикроватная тумба',
      dresser: 'Комод',
    };
    return labels[type] || type;
  };
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      maximumFractionDigits: 0,
    }).format(price);
  };
  
  return (
    <div className="product-card">
      <Link to={ROUTES.configurator.product(id)} className="product-card__link">
        <div className="product-card__image-wrapper">
          {image_url ? (
            <img 
              src={image_url} 
              alt={name}
              className="product-card__image"
            />
          ) : (
            <div className="product-card__placeholder">
              <span className="product-card__placeholder-icon">🪑</span>
            </div>
          )}
          <span className="product-card__type">{getTypeLabel(furniture_type)}</span>
        </div>
        
        <div className="product-card__content">
          <h3 className="product-card__title">{name}</h3>
          {description && (
            <p className="product-card__description">{description}</p>
          )}
          <div className="product-card__footer">
            <span className="product-card__price">{formatPrice(base_price)}</span>
            <span className="product-card__cta">Настроить →</span>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default ProductCard;
