export const ROUTES = {
  // Главная
  home: '/',
  
  // Каталог
  catalog: {
    base: '/catalog',
    type: (type: string) => `/catalog/${type}`,
    product: (id: string) => `/catalog/product/${id}`,
  },
  
  // Конфигуратор
  configurator: {
    base: '/configurator',
    type: (type: string) => `/configurator/${type}`,
    product: (id: string) => `/configurator/product/${id}`,
    materials: (id: string) => `/configurator/product/${id}/materials`,
    summary: (id: string) => `/configurator/product/${id}/summary`,
  },
  
  // Корзина
  cart: {
    base: '/cart',
    checkout: '/cart/checkout',
  },
  
  // Авторизация
  auth: {
    login: '/login',
    register: '/register',
  },
} as const;

