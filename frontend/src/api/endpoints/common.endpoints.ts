// Общие эндпоинты (категории, продукты, материалы)

export const commonEndpoints = {
  // Каталог
  categories: '/v1/categories',
  products: '/v1/products',

  // Материалы
  materials: {
    all: '/v1/materials',
    sheet: '/v1/materials/sheet',
    edge: '/v1/materials/edge',
    slideGuides: '/v1/materials/slide-guides',
    hinges: '/v1/materials/hinges',
    supports: '/v1/materials/supports',
    wallMounts: '/v1/materials/wall-mounts',
  },
} as const;

export type CommonEndpoints = typeof commonEndpoints;
