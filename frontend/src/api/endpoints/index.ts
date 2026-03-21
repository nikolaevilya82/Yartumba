// Главный файл экспорта эндпоинтов
// Отвечает только за ре-экспорт, не за логику

// Общие эндпоинты
export { commonEndpoints } from './common.endpoints';
export type { CommonEndpoints } from './common.endpoints';

// Продукты (товары)
export { 
  goodsEndpoints, 
  bookshelfEndpoints,
  nightstandEndpoints,
  dresserEndpoints,
} from './products';

// Конфигуратор
export { configuratorEndpoints } from './configurator.endpoints';
export type { ConfiguratorEndpoints } from './configurator.endpoints';

// Корзина
export { cartEndpoints } from './cart.endpoints';
export type { CartEndpoints } from './cart.endpoints';

// Заказы
export { orderEndpoints } from './orders.endpoints';
export type { OrderEndpoints } from './orders.endpoints';

// Хелперы
export { getEndpointsByType, buildUrl, createBaseEndpoints } from './helpers';
export type { GoodsEndpoints, AllGoodsEndpoints, QueryParams } from './types';

// Параметры запросов
export const queryParams = {
  pagination: {
    page: 'page',
    limit: 'limit',
    sortBy: 'sort_by',
    sortOrder: 'sort_order',
  },
  filters: {
    category: 'category_id',
    material: 'material_type',
    minPrice: 'min_price',
    maxPrice: 'max_price',
    active: 'is_active',
    search: 'search',
  },
} as const;

