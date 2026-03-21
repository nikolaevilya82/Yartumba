import { apiClient } from '../client';
import { dresserEndpoints } from '../endpoints/products';
import type { ApiResponse, PaginatedResponse } from '../../core/types/api.types';
import type { Dresser, FurniturePart, FurnitureWithProduct } from '../../core/types/product.types';

// Данные для создания комода
export interface CreateDresserData {
  width: number;
  height: number;
  depth: number;
  drawer_count: number;
  row_count: number;
  has_mirror: boolean;
  material_id?: number;
}

// Данные для обновления комода
export interface UpdateDresserData extends Partial<CreateDresserData> {}

// Параметры запроса
export interface DresserParams {
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

// Получить список комодов
export async function getDressers(
  params?: DresserParams
): Promise<PaginatedResponse<Dresser>> {
  return apiClient.get<PaginatedResponse<Dresser>>(
    dresserEndpoints.list,
    params
  );
}

// Получить комод по ID
export async function getDresserById(id: number): Promise<ApiResponse<Dresser>> {
  return apiClient.get<ApiResponse<Dresser>>(dresserEndpoints.get(id));
}

// Получить комод с деталями
export async function getDresserFull(id: number): Promise<ApiResponse<FurnitureWithProduct>> {
  return apiClient.get<ApiResponse<FurnitureWithProduct>>(dresserEndpoints.full(id));
}

// Создать комод
export async function createDresser(
  data: CreateDresserData
): Promise<ApiResponse<Dresser>> {
  return apiClient.post<ApiResponse<Dresser>>(
    dresserEndpoints.create,
    data
  );
}

// Обновить комод
export async function updateDresser(
  id: number,
  data: UpdateDresserData
): Promise<ApiResponse<Dresser>> {
  return apiClient.patch<ApiResponse<Dresser>>(
    dresserEndpoints.update(id),
    data
  );
}

// Удалить комод
export async function deleteDresser(id: number): Promise<ApiResponse<{ success: boolean }>> {
  return apiClient.delete<ApiResponse<{ success: boolean }>>(
    dresserEndpoints.delete(id)
  );
}

// === Детали комода ===

// Получить все детали комода
export async function getDresserParts(
  dresserId: number
): Promise<ApiResponse<FurniturePart[]>> {
  return apiClient.get<ApiResponse<FurniturePart[]>>(
    dresserEndpoints.parts(dresserId)
  );
}

// Получить деталь комода по ID
export async function getDresserPartById(
  dresserId: number,
  partId: number
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.get<ApiResponse<FurniturePart>>(
    dresserEndpoints.part(dresserId, partId)
  );
}

// Создать деталь комода
export async function createDresserPart(
  dresserId: number,
  data: Partial<FurniturePart>
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.post<ApiResponse<FurniturePart>>(
    dresserEndpoints.parts(dresserId),
    data
  );
}

// Обновить деталь комода
export async function updateDresserPart(
  dresserId: number,
  partId: number,
  data: Partial<FurniturePart>
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.patch<ApiResponse<FurniturePart>>(
    dresserEndpoints.part(dresserId, partId),
    data
  );
}

// Удалить деталь комода
export async function deleteDresserPart(
  dresserId: number,
  partId: number
): Promise<ApiResponse<{ success: boolean }>> {
  return apiClient.delete<ApiResponse<{ success: boolean }>>(
    dresserEndpoints.part(dresserId, partId)
  );
}

// Экспорт сервиса
export const dresserService = {
  getList: getDressers,
  getById: getDresserById,
  getFull: getDresserFull,
  create: createDresser,
  update: updateDresser,
  delete: deleteDresser,
  getParts: getDresserParts,
  getPartById: getDresserPartById,
  createPart: createDresserPart,
  updatePart: updateDresserPart,
  deletePart: deleteDresserPart,
};

export default dresserService;
