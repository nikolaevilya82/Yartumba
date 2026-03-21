// Хелперы для работы с эндпоинтами
import type { GoodsEndpoints } from '../types';

// Получить эндпоинты товара по типу
export function getEndpointsByType(
  type: 'bookshelf' | 'nightstand' | 'dresser',
  endpointsMap: Record<string, GoodsEndpoints>
): GoodsEndpoints {
  const endpoints = endpointsMap[type];
  if (!endpoints) {
    throw new Error(`Unknown goods type: ${type}`);
  }
  return endpoints;
}

// Построить URL с параметрами
export function buildUrl(baseUrl: string, params?: Record<string, string | number | boolean | undefined>): string {
  if (!params) return baseUrl;

  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, String(value));
    }
  });

  const queryString = searchParams.toString();
  return queryString ? `${baseUrl}?${queryString}` : baseUrl;
}

// Создать базовые эндпоинты для товара
export function createBaseEndpoints(basePath: string) {
  return {
    list: basePath,
    get: (id: number) => `${basePath}/${id}`,
    full: (id: number) => `${basePath}/${id}/full`,
    create: basePath,
    update: (id: number) => `${basePath}/${id}`,
    delete: (id: number) => `${basePath}/${id}`,
    parts: (id: number) => `${basePath}/${id}/parts`,
    part: (id: number, partId: number) => `${basePath}/${id}/parts/${partId}`,
  };
}
