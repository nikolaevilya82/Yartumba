import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ROUTES } from '../core/config/routes.config';
import CatalogPage from '../pages/catalog/CatalogPage';
import ConfiguratorPage from '../pages/configurator/ConfiguratorPage';
import CartPage from '../pages/cart/CartPage';
import LoginPage from '../pages/auth/LoginPage';
import RegisterPage from '../pages/auth/RegisterPage';

const AppRoutes = () => {
  return (
    <Routes>
        {/* Главная - каталог */}
        <Route path={ROUTES.home} element={<CatalogPage />} />
        
        {/* Каталог */}
        <Route path={ROUTES.catalog.base} element={<CatalogPage />} />
        <Route path={ROUTES.catalog.type(':type')} element={<CatalogPage />} />
        
        {/* Конфигуратор */}
        <Route path={ROUTES.configurator.base} element={<ConfiguratorPage />} />
        <Route path={ROUTES.configurator.type(':type')} element={<ConfiguratorPage />} />
        <Route path={ROUTES.configurator.product(':id')} element={<ConfiguratorPage />} />
        <Route path={ROUTES.configurator.materials(':id')} element={<ConfiguratorPage />} />
        <Route path={ROUTES.configurator.summary(':id')} element={<ConfiguratorPage />} />
        
        {/* Корзина */}
        <Route path={ROUTES.cart.base} element={<CartPage />} />
        <Route path={ROUTES.cart.checkout} element={<CartPage />} />
        
        {/* Авторизация */}
        <Route path={ROUTES.auth.login} element={<LoginPage />} />
        <Route path={ROUTES.auth.register} element={<RegisterPage />} />
        
        {/* 404 */}
        <Route path="*" element={
          <div style={{ padding: '48px', textAlign: 'center' }}>
            <h1>404</h1>
            <p>Страница не найдена</p>
          </div>
        } />
      </Routes>
  );
};

export default AppRoutes;
