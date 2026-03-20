export const apiConfig = {
  baseUrl: 'http://localhost:8000',
  timeout: 30000,
  retryAttempts: 3,
  retryDelay: 1000,
} as const;

export const endpoints = {
  // Каталог
  categories: '/v1/categories',
  products: '/v1/products',

  // Товары
  bookshelf: '/v1/goods/bookshelf',
  nightstand: '/v1/goods/nightstand',
  dresser: '/v1/goods/dresser',

  // Материалы
  sheetMaterials: '/v1/materials/sheet',
  edgeMaterials: '/v1/materials/edge',
  slideGuides: '/v1/materials/slide-guides',
  hinges: '/v1/materials/hinges',
  supports: '/v1/materials/supports',
  wallMounts: '/v1/materials/wall-mounts',

  // Корзина
  cart: '/v1/cart',
} as const;

export const apiEndpoints = {
  bookshelf: {
    list: endpoints.bookshelf,
    get: (id: number) => `${endpoints.bookshelf}/${id}`,
    getFull: (id: number) => `${endpoints.bookshelf}/${id}/full`,
    create: endpoints.bookshelf,
    update: (id: number) => `${endpoints.bookshelf}/${id}`,
    delete: (id: number) => `${endpoints.bookshelf}/${id}`,
    parts: (id: number) => `${endpoints.bookshelf}/${id}/parts`,
    part: (id: number, partId: number) => `${endpoints.bookshelf}/${id}/parts/${partId}`,
  },
  nightstand: {
    list: endpoints.nightstand,
    get: (id: number) => `${endpoints.nightstand}/${id}`,
    getFull: (id: number) => `${endpoints.nightstand}/${id}/full`,
    create: endpoints.nightstand,
    update: (id: number) => `${endpoints.nightstand}/${id}`,
    delete: (id: number) => `${endpoints.nightstand}/${id}`,
    parts: (id: number) => `${endpoints.nightstand}/${id}/parts`,
    part: (id: number, partId: number) => `${endpoints.nightstand}/${id}/parts/${partId}`,
  },
  dresser: {
    list: endpoints.dresser,
    get: (id: number) => `${endpoints.dresser}/${id}`,
    getFull: (id: number) => `${endpoints.dresser}/${id}/full`,
    create: endpoints.dresser,
    update: (id: number) => `${endpoints.dresser}/${id}`,
    delete: (id: number) => `${endpoints.dresser}/${id}`,
    parts: (id: number) => `${endpoints.dresser}/${id}/parts`,
    part: (id: number, partId: number) => `${endpoints.dresser}/${id}/parts/${partId}`,
  },
} as const;

export type ApiConfig = typeof apiConfig;
export type Endpoints = typeof endpoints;
