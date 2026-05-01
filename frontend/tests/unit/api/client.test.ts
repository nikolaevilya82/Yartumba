import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { apiClient, createApiClient } from '@/api/client';
import type { ApiError } from '@/core/types/api.types';

// Мокируем global.fetch
global.fetch = vi.fn();

describe('api/client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('GET запрос', () => {
    it('должен выполнять GET запрос к правильному URL', async () => {
      const mockResponse = { data: 'test' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.get<{ data: string }>('/test-endpoint');

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/test-endpoint',
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('должен добавлять query параметры', async () => {
      const mockResponse = { items: [] };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      await apiClient.get('/test-endpoint', { page: 1, limit: 10, active: true });

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('page=1'),
        expect.any(Object)
      );
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('limit=10'),
        expect.any(Object)
      );
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('active=true'),
        expect.any(Object)
      );
    });

    it('должен игнорировать undefined параметры', async () => {
      const mockResponse = { items: [] };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      await apiClient.get('/test-endpoint', { page: 1, filter: undefined });

      expect(global.fetch).toHaveBeenCalledWith(
        expect.not.stringContaining('filter='),
        expect.any(Object)
      );
    });
  });

  describe('POST запрос с телом', () => {
    it('должен выполнять POST запрос с телом', async () => {
      const mockResponse = { id: 1, name: 'Created' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const payload = { name: 'Test', value: 123 };
      const result = await apiClient.post('/test-endpoint', payload);

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/test-endpoint',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(payload),
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('должен выполнять POST запрос без тела', async () => {
      const mockResponse = { success: true };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.post('/test-endpoint');

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/test-endpoint',
        expect.objectContaining({
          method: 'POST',
          body: undefined,
        })
      );
      expect(result).toEqual(mockResponse);
    });
  });

  describe('PUT запрос', () => {
    it('должен выполнять PUT запрос с телом', async () => {
      const mockResponse = { id: 1, updated: true };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const payload = { name: 'Updated' };
      const result = await apiClient.put('/test-endpoint/1', payload);

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/test-endpoint/1',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify(payload),
        })
      );
      expect(result).toEqual(mockResponse);
    });
  });

  describe('DELETE запрос', () => {
    it('должен выполнять DELETE запрос', async () => {
      const mockResponse = { success: true };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.delete('/test-endpoint/1');

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/test-endpoint/1',
        expect.objectContaining({
          method: 'DELETE',
        })
      );
      expect(result).toEqual(mockResponse);
    });
  });

  describe('Обработка ошибок', () => {
    it('должен обрабатывать 404 ошибку', async () => {
      const mockError: ApiError = {
        code: 'NOT_FOUND',
        message: 'Resource not found',
        status_code: 404,
      };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => mockError,
      });

      await expect(apiClient.get('/nonexistent')).rejects.toEqual(mockError);
    });

    it('должен обрабатывать 500 ошибку', async () => {
      const mockError: ApiError = {
        code: 'INTERNAL_ERROR',
        message: 'Internal server error',
        status_code: 500,
      };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => mockError,
      });

      await expect(apiClient.get('/error')).rejects.toEqual(mockError);
    });

    it('должен обрабатывать ошибку с невалидным JSON', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => {
          throw new Error('Invalid JSON');
        },
      });

      await expect(apiClient.get('/error')).rejects.toEqual(
        expect.objectContaining({
          status_code: 500,
          message: 'Internal Server Error',
        })
      );
    });

    it('должен обрабатывать таймаут запроса', async () => {
      // Мокируем abort
      const abortControllerAbort = vi.fn();
      vi.spyOn(global, 'AbortController').mockImplementation(() => ({
        signal: {},
        abort: abortControllerAbort,
      } as unknown as AbortController));

      // Создаём ошибку AbortError
      const abortError = new Error('The operation was aborted');
      abortError.name = 'AbortError';
      
      (global.fetch as jest.Mock).mockRejectedValueOnce(abortError);

      // Создаём клиента с коротким таймаутом
      const client = createApiClient({ timeout: 1 });
      
      await expect(client.get('/slow-endpoint')).rejects.toEqual(
        expect.objectContaining({
          code: 'TIMEOUT',
          message: 'Превышен таймаут запроса',
          status_code: 408,
        })
      );
    });
  });

  describe('Авторизация', () => {
    it('должен добавлять токен авторизации если он есть', async () => {
      const mockResponse = { data: 'protected' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const client = createApiClient({
        getAuthToken: () => 'test-token-123',
      });

      await client.get('/protected-endpoint');

      const callArgs = (global.fetch as jest.Mock).mock.calls[0];
      const headers = callArgs[1].headers;
      
      expect(headers['Authorization']).toBe('Bearer test-token-123');
    });

    it('должен не добавлять токен если его нет', async () => {
      const mockResponse = { data: 'public' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const client = createApiClient({
        getAuthToken: () => null,
      });

      await client.get('/public-endpoint');

      const callArgs = (global.fetch as jest.Mock).mock.calls[0];
      const headers = callArgs[1].headers;
      
      expect(headers['Authorization']).toBeUndefined();
    });

    it('должен обновлять токен при каждом запросе', async () => {
      const mockResponse = { data: 'protected' };
      (global.fetch as jest.Mock)
        .mockResolvedValueOnce({ ok: true, json: async () => mockResponse })
        .mockResolvedValueOnce({ ok: true, json: async () => mockResponse });

      let currentToken = 'token-1';
      const client = createApiClient({
        getAuthToken: () => currentToken,
      });

      await client.get('/endpoint-1');
      const headers1 = (global.fetch as jest.Mock).mock.calls[0][1].headers;
      expect(headers1['Authorization']).toBe('Bearer token-1');

      // Меняем токен
      currentToken = 'token-2';
      
      await client.get('/endpoint-2');
      const headers2 = (global.fetch as jest.Mock).mock.calls[1][1].headers;
      expect(headers2['Authorization']).toBe('Bearer token-2');
    });
  });

  describe('createApiClient', () => {
    it('должен создавать клиента с кастомной базовой URL', async () => {
      const mockResponse = { data: 'test' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const client = createApiClient({ baseUrl: 'https://api.example.com' });
      await client.get('/endpoint');

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.example.com/endpoint',
        expect.any(Object)
      );
    });

    it('должен создавать клиента с кастомным таймаутом', async () => {
      const mockResponse = { data: 'test' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const client = createApiClient({ timeout: 5000 });
      await client.get('/endpoint');

      // Проверяем что запрос выполнился
      expect(global.fetch).toHaveBeenCalled();
    });
  });
});
