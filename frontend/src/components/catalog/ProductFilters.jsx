import React from 'react';
import { useCatalog } from '../../stores/catalog';
import { FURNITURE_TYPES } from '../../core/constants/product.constants';
import './ProductFilters.css';

const ProductFilters = () => {
  const { selectedType, setSearchQuery, clearFilters, currentFilters, setSelectedType } = useCatalog();
  
  const handleTypeChange = (type) => {
    setSelectedType(type === 'all' ? null : type);
  };
  
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };
  
  return (
    <div className="product-filters">
      <div className="product-filters__search">
        <input
          type="text"
          placeholder="Поиск товаров..."
          value={currentFilters.searchQuery || ''}
          onChange={handleSearchChange}
          className="product-filters__search-input"
        />
      </div>
      
      <div className="product-filters__types">
        <button
          className={`product-filters__type-btn ${selectedType === null ? 'active' : ''}`}
          onClick={() => handleTypeChange('all')}
        >
          Все
        </button>
        
        {FURNITURE_TYPES.map(type => (
          <button
            key={type}
            className={`product-filters__type-btn ${selectedType === type ? 'active' : ''}`}
            onClick={() => handleTypeChange(type)}
          >
            {type === 'bookshelf' && 'Полки'}
            {type === 'nightstand' && 'Тумбы'}
            {type === 'dresser' && 'Комоды'}
          </button>
        ))}
      </div>
      
      {selectedType && (
        <button 
          className="product-filters__clear"
          onClick={clearFilters}
        >
          Сбросить фильтры
        </button>
      )}
    </div>
  );
};

export default ProductFilters;
