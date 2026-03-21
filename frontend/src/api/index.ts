// API клиент
export { apiClient, createApiClient } from './client';
export type { RequestOptions, RequestMethod, ApiClientConfig } from './client';

// Эндпоинты
export { 
  commonEndpoints, 
  bookshelfEndpoints, 
  nightstandEndpoints, 
  dresserEndpoints,
  configuratorEndpoints, 
  cartEndpoints, 
  orderEndpoints,
  queryParams,
  goodsEndpoints,
} from './endpoints';
export type { CommonEndpoints, ConfiguratorEndpoints, CartEndpoints, OrderEndpoints } from './endpoints';

// Сервисы товаров
export * from './services/bookshelf.service';
export * from './services/nightstand.service';
export * from './services/dresser.service';

// Сервисы
export * from './services/configurator.service';
export * from './services/cart.service';
export * from './services/order.service';

