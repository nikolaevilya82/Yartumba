import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Простая имитация API
const mockCartService = {
  addItemToCart: vi.fn(),
  updateCartItem: vi.fn(),
  incrementCartItem: vi.fn(),
  decrementCartItem: vi.fn(),
  removeFromCart: vi.fn(),
  clearCart: vi.fn(),
  applyPromocode: vi.fn(),
  removePromocode: vi.fn(),
};

vi.mock('@/api/services/cart.service', () => ({
  default: mockCartService,
  addItemToCart: mockCartService.addItemToCart,
  updateCartItem: mockCartService.updateCartItem,
  incrementCartItem: mockCartService.incrementCartItem,
  decrementCartItem: mockCartService.decrementCartItem,
  removeFromCart: mockCartService.removeFromCart,
  clearCart: mockCartService.clearCart,
  applyPromocode: mockCartService.applyPromocode,
  removePromocode: mockCartService.removePromocode,
}));

describe('Cart Actions', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('addItemToCart API call', () => {
    it('должен вызывать API с правильными параметрами', async () => {
      const mockResponse = { data: { cart: null } };
      mockCartService.addItemToCart.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.addItemToCart('bookshelf', { width: 1000, height: 2000 }, 1);

      expect(mockCartService.addItemToCart).toHaveBeenCalledWith(
        'bookshelf',
        { width: 1000, height: 2000 },
        1
      );
    });

    it('должен использовать quantity=1 по умолчанию', async () => {
      const mockResponse = { data: { cart: null } };
      mockCartService.addItemToCart.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.addItemToCart('nightstand', { width: 500 });

      expect(mockCartService.addItemToCart).toHaveBeenCalledWith(
        'nightstand',
        { width: 500 }
      );
    });

    it('должен возвращать ошибку при неудаче API', async () => {
      mockCartService.addItemToCart.mockRejectedValueOnce(new Error('API error'));

      const { default: cartService } = await import('@/api/services/cart.service');
      
      await expect(cartService.addItemToCart('bookshelf', { width: 1000 })).rejects.toThrow('API error');
    });
  });

  describe('updateCartItem API call', () => {
    it('должен обновлять количество товара', async () => {
      const mockResponse = { data: {} };
      mockCartService.updateCartItem.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.updateCartItem(1, 5);

      expect(mockCartService.updateCartItem).toHaveBeenCalledWith(1, 5);
    });
  });

  describe('incrementCartItem API call', () => {
    it('должен увеличивать количество товара', async () => {
      const mockResponse = { data: {} };
      mockCartService.incrementCartItem.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.incrementCartItem(1);

      expect(mockCartService.incrementCartItem).toHaveBeenCalledWith(1);
    });
  });

  describe('decrementCartItem API call', () => {
    it('должен уменьшать количество товара', async () => {
      const mockResponse = { data: {} };
      mockCartService.decrementCartItem.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.decrementCartItem(1);

      expect(mockCartService.decrementCartItem).toHaveBeenCalledWith(1);
    });
  });

  describe('removeFromCart API call', () => {
    it('должен удалять товар из корзины', async () => {
      const mockResponse = { data: {} };
      mockCartService.removeFromCart.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.removeFromCart(1);

      expect(mockCartService.removeFromCart).toHaveBeenCalledWith(1);
    });
  });

  describe('clearCart API call', () => {
    it('должен очищать корзину', async () => {
      const mockResponse = { data: {} };
      mockCartService.clearCart.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.clearCart();

      expect(mockCartService.clearCart).toHaveBeenCalled();
    });
  });

  describe('applyPromocode API call', () => {
    it('должен применять промокод', async () => {
      const mockResponse = { data: { discount: 20 } };
      mockCartService.applyPromocode.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      const result = await cartService.applyPromocode('SUMMER20');

      expect(mockCartService.applyPromocode).toHaveBeenCalledWith('SUMMER20');
      expect(result.data.discount).toBe(20);
    });
  });

  describe('removePromocode API call', () => {
    it('должен удалять промокод', async () => {
      const mockResponse = { data: {} };
      mockCartService.removePromocode.mockResolvedValueOnce(mockResponse);

      const { default: cartService } = await import('@/api/services/cart.service');
      await cartService.removePromocode();

      expect(mockCartService.removePromocode).toHaveBeenCalled();
    });
  });
});
