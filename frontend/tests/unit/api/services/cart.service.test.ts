import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  getCart,
  addItemToCart,
  updateCartItem,
  incrementCartItem,
  decrementCartItem,
  removeFromCart,
  clearCart,
  applyPromocode,
  removePromocode,
  getCartItemsCount,
  getCartTotal,
  isItemInCart,
} from '@/api/services/cart.service';
import * as apiClient from '@/api/client';
import * as cartEndpoints from '@/api/endpoints/cart.endpoints';

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

describe('api/services/cart', () => {
  const mockApiClient = apiClient.apiClient as {
    get: ReturnType<typeof vi.fn>;
    post: ReturnType<typeof vi.fn>;
    patch: ReturnType<typeof vi.fn>;
    delete: ReturnType<typeof vi.fn>;
  };

  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getCart', () => {
    it('должен вызывать правильный эндпоинт для получения корзины', async () => {
      const mockResponse = {
        data: { items: [], total_items: 0, total_price: 0 },
      };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await getCart();

      expect(mockApiClient.get).toHaveBeenCalledWith(cartEndpoints.cartEndpoints.cart);
    });

    it('должен возвращать данные корзины', async () => {
      const mockCart = {
        items: [{ id: 1, quantity: 2, price: 1000 }],
        total_items: 1,
        total_price: 2000,
      };
      const mockResponse = { data: mockCart };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      const result = await getCart();

      expect(result.data).toEqual(mockCart);
    });
  });

  describe('addItem', () => {
    it('должен вызывать POST запрос для добавления товара', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      const payload = {
        furniture_type: 'bookshelf',
        configuration: { width: 1000, height: 2000 },
        quantity: 1,
      };

      await addItemToCart('bookshelf', { width: 1000, height: 2000 }, 1);

      expect(mockApiClient.post).toHaveBeenCalledWith(
        cartEndpoints.cartEndpoints.cart,
        payload
      );
    });

    it('должен использовать quantity=1 по умолчанию', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      await addItemToCart('nightstand', { width: 500 });

      expect(mockApiClient.post).toHaveBeenCalledWith(
        cartEndpoints.cartEndpoints.cart,
        expect.objectContaining({ quantity: 1 })
      );
    });
  });

  describe('updateQuantity', () => {
    it('должен вызывать PATCH запрос для обновления количества', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.patch.mockResolvedValueOnce(mockResponse);

      await updateCartItem(123, { quantity: 5 });

      expect(mockApiClient.patch).toHaveBeenCalledWith(
        cartEndpoints.cartEndpoints.cartItem(123),
        { quantity: 5 }
      );
    });
  });

  describe('increment', () => {
    it('должен увеличивать количество товара на 1', async () => {
      const mockCart = {
        data: {
          items: [{ id: 1, quantity: 2 }],
          total_items: 1,
          total_price: 0,
        },
      };
      mockApiClient.get.mockResolvedValueOnce(mockCart);
      mockApiClient.patch.mockResolvedValueOnce({ data: { success: true } });

      await incrementCartItem(1);

      expect(mockApiClient.patch).toHaveBeenCalledWith(
        cartEndpoints.cartEndpoints.cartItem(1),
        { quantity: 3 }
      );
    });

    it('должен выбрасывать ошибку если товар не найден', async () => {
      const mockCart = {
        data: {
          items: [],
          total_items: 0,
          total_price: 0,
        },
      };
      mockApiClient.get.mockResolvedValueOnce(mockCart);

      await expect(incrementCartItem(999)).rejects.toThrow('Item not found');
    });
  });

  describe('decrement', () => {
    it('должен выбрасывать ошибку если товар не найден', async () => {
      const mockCart = {
        data: {
          items: [],
          total_items: 0,
          total_price: 0,
        },
      };
      mockApiClient.get.mockResolvedValueOnce(mockCart);

      await expect(decrementCartItem(999)).rejects.toThrow('Item not found');
    });
  });

  describe('removePromocode', () => {
    it('должен вызывать DELETE запрос для удаления промокода', async () => {
      const mockResponse = { data: { items: [] } };
      mockApiClient.delete.mockResolvedValueOnce(mockResponse);

      await removePromocode();

      expect(mockApiClient.delete).toHaveBeenCalledWith(
        `${cartEndpoints.cartEndpoints.cart}/promocode`
      );
    });
  });

  describe('isItemInCart', () => {
    it('должен возвращать false если товара нет в корзине', async () => {
      const mockCart = {
        data: {
          items: [{ furniture_type: 'bookshelf', furniture_id: 1 }],
          total_items: 1,
          total_price: 0,
        },
      };
      mockApiClient.get.mockResolvedValueOnce(mockCart);

      const result = await isItemInCart('dresser', 999);

      expect(result).toBe(false);
    });

    it('должен возвращать false при ошибке', async () => {
      mockApiClient.get.mockRejectedValueOnce(new Error('API error'));

      const result = await isItemInCart('bookshelf', 1);

      expect(result).toBe(false);
    });
  });

  describe('обработка ошибок', () => {
    it('должен пробрасывать ошибки от apiClient', async () => {
      const apiError = {
        code: 'CART_ERROR',
        message: 'Cart operation failed',
        status_code: 400,
      };
      mockApiClient.get.mockRejectedValueOnce(apiError);

      await expect(getCart()).rejects.toEqual(apiError);
    });
  });
});
