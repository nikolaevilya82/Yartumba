export const routes = {
  home: '/',
  catalog: '/catalog',

  // Товары
  bookshelf: '/bookshelf',
  bookshelfDetail: (id: number) => `/bookshelf/${id}`,
  bookshelfConfigurator: (id: number) => `/bookshelf/${id}/configurator`,

  nightstand: '/nightstand',
  nightstandDetail: (id: number) => `/nightstand/${id}`,
  nightstandConfigurator: (id: number) => `/nightstand/${id}/configurator`,

  dresser: '/dresser',
  dresserDetail: (id: number) => `/dresser/${id}`,
  dresserConfigurator: (id: number) => `/dresser/${id}/configurator`,

  // Корзина
  cart: '/cart',
  checkout: '/checkout',

  // Страницы
  about: '/about',
  contacts: '/contacts',
  notFound: '*',
} as const;

export const routeNames = {
  home: 'Главная',
  catalog: 'Каталог',
  bookshelf: 'Книжные полки',
  nightstand: 'Прикроватные тумбы',
  dresser: 'Комоды',
  cart: 'Корзина',
  checkout: 'Оформление заказа',
  about: 'О нас',
  contacts: 'Контакты',
} as const;

export type RouteParams = {
  bookshelfDetail: number;
  bookshelfConfigurator: number;
  nightstandDetail: number;
  nightstandConfigurator: number;
  dresserDetail: number;
  dresserConfigurator: number;
};

export type Routes = typeof routes;
