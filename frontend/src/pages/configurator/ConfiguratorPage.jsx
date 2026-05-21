import React from 'react';
import './ConfiguratorPage.css';

const ConfiguratorPage = () => {
  return (
    <div className="configurator-page">
      <div className="container">
        <h1 className="page-title">Конфигуратор</h1>
        <p className="page-subtitle">Настройка параметров мебели</p>
        
        <div className="configurator-page__placeholder">
          <div className="placeholder-content">
            <span className="placeholder-icon">🔧</span>
            <h2>Конфигуратор в разработке</h2>
            <p>Скоро здесь вы сможете настроить мебель под свои нужды</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfiguratorPage;
