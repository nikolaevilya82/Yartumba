import { apiConfig } from '../core/config/api.config';
import type { ApiError } from '../core/types/api.types';

export type RequestMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface RequestOptions {
  method?: RequestMethod;
  body?: unknown;
  headers?: Record<string, string>;
  params?: Record<string, string | number | boolean | undefined>;
}

export interface ApiClientConfig {
  baseUrl: string;
  timeout: number;
  getAuthToken?: () => string | null;
}

class ApiClient {
  private baseUrl: string;
  private timeout: number;
  private getAuthToken?: () => string | null;

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl;
    this.timeout = config.timeout;
    this.getAuthToken = config.getAuthToken;
  }

  private async request<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const { method = 'GET', body, headers = {}, params } = options;

    let url = `${this.baseUrl}${endpoint}`;

    // Добавляем query params
    if (params) {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, String(value));
        }
      });
      const queryString = searchParams.toString();
      if (queryString) {
        url += `?${queryString}`;
      }
    }

    // Подготовка заголовков
    const requestHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...headers,
    };

    // Добавляем токен авторизации
    if (this.getAuthToken) {
      const token = this.getAuthToken();
      if (token) {
        requestHeaders['Authorization'] = `Bearer ${token}`;
      }
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        method,
        headers: requestHeaders,
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error: ApiError = {
          code: errorData.code || 'UNKNOWN_ERROR',
          message: errorData.message || response.statusText,
          details: errorData.details,
          status_code: response.status,
        };
        throw error;
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      
      if ((error as Error).name === 'AbortError') {
        const timeoutError: ApiError = {
          code: 'TIMEOUT',
          message: 'Превышен таймаут запроса',
          status_code: 408,
        };
        throw timeoutError;
      }
      
      throw error;
    }
  }

  async get<T>(endpoint: string, params?: Record<string, string | number | boolean | undefined>): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET', params });
  }

  async post<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, { method: 'POST', body });
  }

  async put<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, { method: 'PUT', body });
  }

  async patch<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, { method: 'PATCH', body });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// Экземпляр API клиента
export const apiClient = new ApiClient({
  baseUrl: apiConfig.baseUrl,
  timeout: apiConfig.timeout,
  getAuthToken: () => localStorage.getItem('auth_token'),
});

// Хелпер для создания кастомного клиента (например, для авторизованных запросов)
export function createApiClient(config: Partial<ApiClientConfig> = {}): ApiClient {
  return new ApiClient({
    baseUrl: config.baseUrl ?? apiConfig.baseUrl,
    timeout: config.timeout ?? apiConfig.timeout,
    getAuthToken: config.getAuthToken,
  });
}
