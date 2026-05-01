import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  getBookshelves,
  getBookshelfById,
  getBookshelfFull,
  createBookshelf,
  updateBookshelf,
  deleteBookshelf,
  getBookshelfParts,
  getBookshelfPartById,
  createBookshelfPart,
  updateBookshelfPart,
  deleteBookshelfPart,
} from '@/api/services/bookshelf.service';
import * as apiClient from '@/api/client';
import * as endpoints from '@/api/endpoints/products';

vi.mock('@/api/client', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/api/client')>();
  return {
    ...actual,
    apiClient: {
      get: vi.fn(),
      post: vi.fn(),
      patch: vi.fn(),
      delete: vi.fn(),
    },
  };
});

describe('api/services/bookshelf', () => {
  const mockApiClient = apiClient.apiClient as {
    get: ReturnType<typeof vi.fn>;
    post: ReturnType<typeof vi.fn>;
    patch: ReturnType<typeof vi.fn>;
    delete: ReturnType<typeof vi.fn>;
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getList', () => {
    it('должен вызывать правильный эндпоинт для получения списка', async () => {
      const mockResponse = {
        data: { items: [], total: 0 },
      };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await getBookshelves({ page: 1, limit: 10 });

      expect(mockApiClient.get).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.list,
        { page: 1, limit: 10 }
      );
    });

    it('должен возвращать данные из ответа', async () => {
      const mockResponse = {
        data: { items: [{ id: 1 }], total: 1 },
      };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      const result = await getBookshelves();

      expect(result).toEqual(mockResponse);
    });

    it('должен работать без параметров', async () => {
      const mockResponse = { data: { items: [] } };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await getBookshelves();

      expect(mockApiClient.get).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.list,
        undefined
      );
    });
  });

  describe('getById', () => {
    it('должен вызывать правильный эндпоинт для получения полки по ID', async () => {
      const mockResponse = { data: { id: 1, name: 'Test' } };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await getBookshelfById(123);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.get(123)
      );
    });

    it('должен возвращать данные полки', async () => {
      const mockBookshelf = { id: 1, width: 1000, height: 2000 };
      const mockResponse = { data: mockBookshelf };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      const result = await getBookshelfById(1);

      expect(result.data).toEqual(mockBookshelf);
    });
  });

  describe('getFull', () => {
    it('должен вызывать правильный эндпоинт для получения полки с деталями', async () => {
      const mockResponse = { data: { id: 1, parts: [] } };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await getBookshelfFull(456);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.full(456)
      );
    });
  });

  describe('create', () => {
    it('должен вызывать POST запрос с правильными данными', async () => {
      const mockResponse = { data: { id: 1 } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      const payload = {
        width: 1200,
        height: 2000,
        depth: 400,
        shelf_count: 5,
        has_back_panel: true,
        max_weight_per_shelf: 50,
      };

      await createBookshelf(payload);

      expect(mockApiClient.post).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.create,
        payload
      );
    });
  });

  describe('update', () => {
    it('должен вызывать PATCH запрос с правильными данными', async () => {
      const mockResponse = { data: { id: 1 } };
      mockApiClient.patch.mockResolvedValueOnce(mockResponse);

      const payload = { width: 1500 };

      await updateBookshelf(123, payload);

      expect(mockApiClient.patch).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.update(123),
        payload
      );
    });
  });

  describe('delete', () => {
    it('должен вызывать DELETE запрос', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.delete.mockResolvedValueOnce(mockResponse);

      await deleteBookshelf(789);

      expect(mockApiClient.delete).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.delete(789)
      );
    });

    it('должен возвращать результат удаления', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.delete.mockResolvedValueOnce(mockResponse);

      const result = await deleteBookshelf(1);

      expect(result.data.success).toBe(true);
    });
  });

  describe('getParts', () => {
    it('должен вызывать правильный эндпоинт для получения деталей', async () => {
      const mockResponse = { data: { items: [] } };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await getBookshelfParts(123);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.parts(123)
      );
    });
  });

  describe('getPartById', () => {
    it('должен вызывать правильный эндпоинт для получения детали', async () => {
      const mockResponse = { data: { id: 1, type: 'shelf' } };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await getBookshelfPartById(123, 456);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.part(123, 456)
      );
    });
  });

  describe('createPart', () => {
    it('должен вызывать POST запрос для создания детали', async () => {
      const mockResponse = { data: { id: 1 } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      const payload = { type: 'shelf', width: 1000 };

      await createBookshelfPart(123, payload);

      expect(mockApiClient.post).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.parts(123),
        payload
      );
    });
  });

  describe('updatePart', () => {
    it('должен вызывать PATCH запрос для обновления детали', async () => {
      const mockResponse = { data: { id: 1 } };
      mockApiClient.patch.mockResolvedValueOnce(mockResponse);

      const payload = { width: 1200 };

      await updateBookshelfPart(123, 456, payload);

      expect(mockApiClient.patch).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.part(123, 456),
        payload
      );
    });
  });

  describe('deletePart', () => {
    it('должен вызывать DELETE запрос для удаления детали', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.delete.mockResolvedValueOnce(mockResponse);

      await deleteBookshelfPart(123, 456);

      expect(mockApiClient.delete).toHaveBeenCalledWith(
        endpoints.bookshelfEndpoints.part(123, 456)
      );
    });
  });

  describe('обработка ошибок', () => {
    it('должен пробрасывать ошибки от apiClient', async () => {
      const apiError = {
        code: 'NOT_FOUND',
        message: 'Not found',
        status_code: 404,
      };
      mockApiClient.get.mockRejectedValueOnce(apiError);

      await expect(getBookshelfById(999)).rejects.toEqual(apiError);
    });

    it('должен обрабатывать сетевые ошибки', async () => {
      const networkError = new Error('Network error');
      mockApiClient.get.mockRejectedValueOnce(networkError);

      await expect(getBookshelves()).rejects.toEqual(networkError);
    });
  });
});
