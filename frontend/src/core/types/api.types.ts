// Базовый API ответ
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

// Ответ с пагинацией
export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationInfo;
}

// Информация о пагинации
export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

// Параметры запроса с пагинацией
export interface PaginationParams {
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

// Параметры фильтрации
export interface FilterParams {
  category_id?: number;
  material_type?: string;
  min_price?: number;
  max_price?: number;
  is_active?: boolean;
  search?: string;
}

// Параметры запроса
export interface RequestParams extends PaginationParams, FilterParams {}

// Ошибка API
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
  status_code: number;
}

// Ответ при ошибке
export interface ApiErrorResponse {
  error: ApiError;
}

// Успешный ответ без данных
export interface ApiSuccessResponse {
  message: string;
  success: boolean;
}

// Ответ при создании/обновлении с ID
export interface IdResponse {
  id: number;
  message?: string;
}

// Тип для загрузки
export interface LoadingState {
  isLoading: boolean;
  error: ApiError | null;
}

// Generic тип для async операций
export type AsyncData<T> = {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
};

// Методы HTTP
export type HttpMethod = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';

// Конфиг для запроса
export interface RequestConfig {
  method: HttpMethod;
  url: string;
  data?: unknown;
  params?: Record<string, string | number | boolean | undefined>;
  headers?: Record<string, string>;
  timeout?: number;
}
