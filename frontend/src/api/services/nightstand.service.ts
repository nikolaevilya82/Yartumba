import { apiClient } from '../client';
import { nightstandEndpoints } from '../endpoints/products';
import type { ApiResponse, PaginatedResponse } from '../../core/types/api.types';
import type { Nightstand, FurniturePart, FurnitureWithProduct } from '../../core/types/product.types';

// Данные для создания тумбы
export interface CreateNightstandData {
  width: number;
  height: number;
  depth: number;
  drawer_count: number;
  has_door: boolean;
  leg_height?: number;
  material_id?: number;
}

// Данные для обновления тумбы
export interface UpdateNightstandData extends Partial<CreateNightstandData> {}

// Параметры запроса
export interface NightstandParams {
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  category_id?: number;
  material_type?: string;
  min_price?: number;
  max_price?: number;
  is_active?: boolean;
  search?: string;
}

// Получить список тумб
export async function getNightstands(
  params?: NightstandParams
): Promise<PaginatedResponse<Nightstand>> {
  return apiClient.get<PaginatedResponse<Nightstand>>(
    nightstandEndpoints.list,
    params
  );
}

// Получить тумбу по ID
export async function getNightstandById(id: number): Promise<ApiResponse<Nightstand>> {
  return apiClient.get<ApiResponse<Nightstand>>(nightstandEndpoints.get(id));
}

// Получить тумбу с деталями
export async function getNightstandFull(id: number): Promise<ApiResponse<FurnitureWithProduct>> {
  return apiClient.get<ApiResponse<FurnitureWithProduct>>(nightstandEndpoints.full(id));
}

// Создать тумбу
export async function createNightstand(
  data: CreateNightstandData
): Promise<ApiResponse<Nightstand>> {
  return apiClient.post<ApiResponse<Nightstand>>(
    nightstandEndpoints.create,
    data
  );
}

// Обновить тумбу
export async function updateNightstand(
  id: number,
  data: UpdateNightstandData
): Promise<ApiResponse<Nightstand>> {
  return apiClient.patch<ApiResponse<Nightstand>>(
    nightstandEndpoints.update(id),
    data
  );
}

// Удалить тумбу
export async function deleteNightstand(id: number): Promise<ApiResponse<{ success: boolean }>> {
  return apiClient.delete<ApiResponse<{ success: boolean }>>(
    nightstandEndpoints.delete(id)
  );
}

// === Детали тумбы ===

// Получить все детали тумбы
export async function getNightstandParts(
  nightstandId: number
): Promise<ApiResponse<FurniturePart[]>> {
  return apiClient.get<ApiResponse<FurniturePart[]>>(
    nightstandEndpoints.parts(nightstandId)
  );
}

// Получить деталь тумбы по ID
export async function getNightstandPartById(
  nightstandId: number,
  partId: number
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.get<ApiResponse<FurniturePart>>(
    nightstandEndpoints.part(nightstandId, partId)
  );
}

// Создать деталь тумбы
export async function createNightstandPart(
  nightstandId: number,
  data: Partial<FurniturePart>
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.post<ApiResponse<FurniturePart>>(
    nightstandEndpoints.parts(nightstandId),
    data
  );
}

// Обновить деталь тумбы
export async function updateNightstandPart(
  nightstandId: number,
  partId: number,
  data: Partial<FurniturePart>
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.patch<ApiResponse<FurniturePart>>(
    nightstandEndpoints.part(nightstandId, partId),
    data
  );
}

// Удалить деталь тумбы
export async function deleteNightstandPart(
  nightstandId: number,
  partId: number
): Promise<ApiResponse<{ success: boolean }>> {
  return apiClient.delete<ApiResponse<{ success: boolean }>>(
    nightstandEndpoints.part(nightstandId, partId)
  );
}

// Экспорт сервиса
export const nightstandService = {
  getList: getNightstands,
  getById: getNightstandById,
  getFull: getNightstandFull,
  create: createNightstand,
  update: updateNightstand,
  delete: deleteNightstand,
  getParts: getNightstandParts,
  getPartById: getNightstandPartById,
  createPart: createNightstandPart,
  updatePart: updateNightstandPart,
  deletePart: deleteNightstandPart,
};

export default nightstandService;
