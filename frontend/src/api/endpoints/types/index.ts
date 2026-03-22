// Типы для эндпоинтов товаров
export interface GoodsEndpoints {
  list: string;
  get: (id: number) => string;
  full: (id: number) => string;
  create: string;
  update: (id: number) => string;
  delete: (id: number) => string;
  parts: (id: number) => string;
  part: (id: number, partId: number) => string;
}

// Тип для всех товарных эндпоинтов
export type AllGoodsEndpoints = {
  bookshelf: GoodsEndpoints;
  nightstand: GoodsEndpoints;
  dresser: GoodsEndpoints;
};

// Тип для параметров запроса
export interface QueryParams {
  pagination: {
    page: string;
    limit: string;
    sortBy: string;
    sortOrder: string;
  };
  filters: {
    category: string;
    material: string;
    minPrice: string;
    maxPrice: string;
    active: string;
    search: string;
  };
}
