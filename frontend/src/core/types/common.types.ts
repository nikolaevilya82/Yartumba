/**
 * UUID тип
 */
export type UUID = string;

/**
 * Статусы загрузки
 */
export type LoadingStatus = 'idle' | 'loading' | 'success' | 'error';

/**
 * Пагинация
 */
export interface Pagination {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}
