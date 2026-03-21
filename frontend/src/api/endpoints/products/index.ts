import { bookshelfEndpoints } from './bookshelf.endpoints';
import { nightstandEndpoints } from './nightstand.endpoints';
import { dresserEndpoints } from './dresser.endpoints';

// Объединённые эндпоинты товаров
export const goodsEndpoints = {
  bookshelf: bookshelfEndpoints,
  nightstand: nightstandEndpoints,
  dresser: dresserEndpoints,
} as const;

// Прямые экспорты
export { bookshelfEndpoints, nightstandEndpoints, dresserEndpoints };
