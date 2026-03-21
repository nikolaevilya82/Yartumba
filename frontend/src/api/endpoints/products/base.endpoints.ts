// Базовые эндпоинты для товаров (фабрика)
// Используется как основа для конкретных типов товаров

export const goodsBase = {
  list: '',
  get: (id: number) => `/${id}`,
  full: (id: number) => `/${id}/full`,
  create: '',
  update: (id: number) => `/${id}`,
  delete: (id: number) => `/${id}`,
  parts: (id: number) => `/${id}/parts`,
  part: (id: number, partId: number) => `/${id}/parts/${partId}`,
} as const;

// Тип для создания эндпоинтов с базовым путём
export function createGoodsEndpoints(basePath: string) {
  return {
    list: basePath,
    get: (id: number) => `${basePath}/${id}`,
    full: (id: number) => `${basePath}/${id}/full`,
    create: basePath,
    update: (id: number) => `${basePath}/${id}`,
    delete: (id: number) => `${basePath}/${id}`,
    parts: (id: number) => `${basePath}/${id}/parts`,
    part: (id: number, partId: number) => `${basePath}/${id}/parts/${partId}`,
  } as const;
}
