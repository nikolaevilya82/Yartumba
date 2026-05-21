import { apiClient } from '../client';
import type { ApiResponse } from '../../core/types/api.types';
import type { 
  Product, 
  ProductWithDetails, 
  ProductsResponse,
  ProductsQueryParams 
} from '../../core/types/catalog.types';
import type { FurnitureType } from '../../core/constants/product.constants';

// Базовый путь для товаров
const GOODS_BASE = '/v1/goods';

/**
 * Получить список товаров
 */
export async function getProducts(
  params?: ProductsQueryParams
): Promise<ApiResponse<ProductsResponse>> {
  const queryParams = new URLSearchParams();
  
  if (params?.furniture_type) {
    queryParams.append('furniture_type', params.furniture_type);
  }
  if (params?.page) {
    queryParams.append('page', params.page.toString());
  }
  if (params?.per_page) {
    queryParams.append('per_page', params.per_page.toString());
  }
  if (params?.search) {
    queryParams.append('search', params.search);
  }
  
  const query = queryParams.toString();
  const url = query ? `${GOODS_BASE}?${query}` : GOODS_BASE;
  
  return apiClient.get<ApiResponse<ProductsResponse>>(url);
}

/**
 * Получить товары конкретного типа
 */
export async function getProductsByType(
  type: FurnitureType,
  page = 1,
  perPage = 20
): Promise<ApiResponse<ProductsResponse>> {
  return apiClient.get<ApiResponse<ProductsResponse>>(
    `${GOODS_BASE}/${type}/?page=${page}&per_page=${perPage}`
  );
}

/**
 * Получить товар по ID
 */
export async function getProductById(
  type: FurnitureType,
  id: string
): Promise<ApiResponse<ProductWithDetails>> {
  return apiClient.get<ApiResponse<ProductWithDetails>>(
    `${GOODS_BASE}/${type}/${id}/full`
  );
}
