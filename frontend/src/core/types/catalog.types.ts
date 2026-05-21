import { FurnitureType } from '../constants/product.constants';
import { UUID } from './common.types';

/**
 * Базовый товар
 */
export interface Product {
  id: UUID;
  product_id: UUID;
  name: string;
  description?: string;
  base_price: number;
  image_url?: string;
  furniture_type: FurnitureType;
  created_at: string;
  updated_at: string;
}

/**
 * Расширенный товар с деталями
 */
export interface ProductWithDetails extends Product {
  dimensions: {
    width: number;
    height: number;
    depth: number;
  };
  parts_count: number;
  has_drawers: boolean;
  is_configurable: boolean;
}

/**
 * Фильтры для каталога
 */
export interface CatalogFilters {
  furnitureType?: FurnitureType | null;
  priceMin?: number;
  priceMax?: number;
  searchQuery?: string;
}

/**
 * Ответ API на список товаров
 */
export interface ProductsResponse {
  items: Product[];
  total: number;
  page: number;
  per_page: number;
}

/**
 * Параметры запроса товаров
 */
export interface ProductsQueryParams {
  furniture_type?: FurnitureType;
  page?: number;
  per_page?: number;
  search?: string;
}
