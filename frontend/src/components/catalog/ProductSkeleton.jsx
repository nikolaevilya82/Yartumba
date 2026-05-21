import React from 'react';
import './ProductSkeleton.css';

const ProductSkeleton = () => {
  return (
    <div className="product-skeleton">
      <div className="product-skeleton__image" />
      <div className="product-skeleton__content">
        <div className="product-skeleton__title" />
        <div className="product-skeleton__description" />
        <div className="product-skeleton__footer">
          <div className="product-skeleton__price" />
          <div className="product-skeleton__cta" />
        </div>
      </div>
    </div>
  );
};

export default ProductSkeleton;
