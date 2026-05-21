import React from 'react';
import { useCatalog } from '../../stores/catalog';
import ProductCard from './ProductCard';
import ProductSkeleton from './ProductSkeleton';
import './ProductList.css';

const ProductList = () => {
  const { filteredProducts, isEmpty, isLoaded, error, loadProducts, clearFilters } = useCatalog();
  
  if (!isLoaded) {
    return (
      <div className="product-list">
        {[...Array(6)].map((_, i) => (
          <ProductSkeleton key={i} />
        ))}
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="product-list__error">
        <div className="error-message">
          <span className="error-message__icon">❌</span>
          <p>{error}</p>
          <button onClick={() => loadProducts()}>
            Попробовать снова
          </button>
        </div>
      </div>
    );
  }
  
  if (isEmpty) {
    return (
      <div className="product-list__empty">
        <div className="empty-message">
          <span className="empty-message__icon">📦</span>
          <h3>Товары не найдены</h3>
          <p>Попробуйте изменить параметры фильтра</p>
          <button onClick={() => clearFilters()}>
            Сбросить фильтры
          </button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="product-list">
      <div className="product-list__header">
        <h2>Найдено товаров: {filteredProducts.length}</h2>
      </div>
      
      <div className="product-list__grid">
        {filteredProducts.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default ProductList;
