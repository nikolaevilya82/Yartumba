import { apiClient } from '../client';
import { bookshelfEndpoints } from '../endpoints/products';
import type { ApiResponse, PaginatedResponse } from '../../core/types/api.types';
import type { Bookshelf, FurniturePart, FurnitureWithProduct } from '../../core/types/product.types';

// Данные для создания полки
export interface CreateBookshelfData {
  width: number;
  height: number;
  depth: number;
  shelf_count: number;
  has_back_panel: boolean;
  max_weight_per_shelf: number;
  material_id?: number;
}

// Данные для обновления полки
export interface UpdateBookshelfData extends Partial<CreateBookshelfData> {}

// Параметры запроса
export interface BookshelfParams {
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

// Получить список полок
export async function getBookshelves(
  params?: BookshelfParams
): Promise<PaginatedResponse<Bookshelf>> {
  return apiClient.get<PaginatedResponse<Bookshelf>>(
    bookshelfEndpoints.list,
    params
  );
}

// Получить полку по ID
export async function getBookshelfById(id: number): Promise<ApiResponse<Bookshelf>> {
  return apiClient.get<ApiResponse<Bookshelf>>(bookshelfEndpoints.get(id));
}

// Получить полку с деталями
export async function getBookshelfFull(id: number): Promise<ApiResponse<FurnitureWithProduct>> {
  return apiClient.get<ApiResponse<FurnitureWithProduct>>(bookshelfEndpoints.full(id));
}

// Создать полку
export async function createBookshelf(
  data: CreateBookshelfData
): Promise<ApiResponse<Bookshelf>> {
  return apiClient.post<ApiResponse<Bookshelf>>(
    bookshelfEndpoints.create,
    data
  );
}

// Обновить полку
export async function updateBookshelf(
  id: number,
  data: UpdateBookshelfData
): Promise<ApiResponse<Bookshelf>> {
  return apiClient.patch<ApiResponse<Bookshelf>>(
    bookshelfEndpoints.update(id),
    data
  );
}

// Удалить полку
export async function deleteBookshelf(id: number): Promise<ApiResponse<{ success: boolean }>> {
  return apiClient.delete<ApiResponse<{ success: boolean }>>(
    bookshelfEndpoints.delete(id)
  );
}

// === Детали полки ===

// Получить все детали полки
export async function getBookshelfParts(
  bookshelfId: number
): Promise<ApiResponse<FurniturePart[]>> {
  return apiClient.get<ApiResponse<FurniturePart[]>>(
    bookshelfEndpoints.parts(bookshelfId)
  );
}

// Получить деталь полки по ID
export async function getBookshelfPartById(
  bookshelfId: number,
  partId: number
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.get<ApiResponse<FurniturePart>>(
    bookshelfEndpoints.part(bookshelfId, partId)
  );
}

// Создать деталь полки
export async function createBookshelfPart(
  bookshelfId: number,
  data: Partial<FurniturePart>
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.post<ApiResponse<FurniturePart>>(
    bookshelfEndpoints.parts(bookshelfId),
    data
  );
}

// Обновить деталь полки
export async function updateBookshelfPart(
  bookshelfId: number,
  partId: number,
  data: Partial<FurniturePart>
): Promise<ApiResponse<FurniturePart>> {
  return apiClient.patch<ApiResponse<FurniturePart>>(
    bookshelfEndpoints.part(bookshelfId, partId),
    data
  );
}

// Удалить деталь полки
export async function deleteBookshelfPart(
  bookshelfId: number,
  partId: number
): Promise<ApiResponse<{ success: boolean }>> {
  return apiClient.delete<ApiResponse<{ success: boolean }>>(
    bookshelfEndpoints.part(bookshelfId, partId)
  );
}

// Экспорт сервиса
export const bookshelfService = {
  getList: getBookshelves,
  getById: getBookshelfById,
  getFull: getBookshelfFull,
  create: createBookshelf,
  update: updateBookshelf,
  delete: deleteBookshelf,
  getParts: getBookshelfParts,
  getPartById: getBookshelfPartById,
  createPart: createBookshelfPart,
  updatePart: updateBookshelfPart,
  deletePart: deleteBookshelfPart,
};

export default bookshelfService;
