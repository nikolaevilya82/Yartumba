import React, { useEffect } from 'react';
import { useCatalog } from '../../stores/catalog';
import ProductFilters from '../../components/catalog/ProductFilters';
import ProductList from '../../components/catalog/ProductList';
import './CatalogPage.css';

const CatalogPage = () => {
  const { loadProducts } = useCatalog();
  
  useEffect(() => {
    loadProducts();
  }, [loadProducts]);
  
  return (
    <div className="catalog-page">
      <div className="catalog-page__header">
        <h1 className="page-title">Каталог мебели</h1>
        <p className="page-subtitle">Создайте мебель своей мечты с помощью нашего конфигуратора</p>
      </div>
      
      <ProductFilters />
      <ProductList />
    </div>
  );
};

export default CatalogPage;
