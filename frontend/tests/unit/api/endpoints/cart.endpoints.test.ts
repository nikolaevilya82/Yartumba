import { describe, it, expect } from 'vitest';
import { cartEndpoints } from '@/api/endpoints';

describe('api/endpoints/cart', () => {
  describe('cart', () => {
    it('должен возвращать правильный URL для корзины', () => {
      expect(cartEndpoints.cart).toBe('/v1/cart');
    });
  });

  describe('cartItem(id)', () => {
    it('должен возвращать правильный URL для товара в корзине по ID', () => {
      expect(cartEndpoints.cartItem(1)).toBe('/v1/cart/items/1');
      expect(cartEndpoints.cartItem(123)).toBe('/v1/cart/items/123');
      expect(cartEndpoints.cartItem(9999)).toBe('/v1/cart/items/9999');
    });

    it('должен работать с ID 0', () => {
      expect(cartEndpoints.cartItem(0)).toBe('/v1/cart/items/0');
    });
  });

  describe('applyPromocode', () => {
    it('должен возвращать правильный URL для применения промокода', () => {
      expect(cartEndpoints.applyPromocode).toBe('/v1/cart/promocode');
    });
  });

  describe('removePromocode', () => {
    it('должен возвращать правильный URL для удаления промокода', () => {
      expect(cartEndpoints.removePromocode).toBe('/v1/cart/promocode');
    });
  });

  describe('все эндпоинты должны быть строками или функциями', () => {
    it('cart должен быть строкой', () => {
      expect(typeof cartEndpoints.cart).toBe('string');
    });

    it('cartItem должен быть функцией', () => {
      expect(typeof cartEndpoints.cartItem).toBe('function');
    });

    it('applyPromocode должен быть строкой', () => {
      expect(typeof cartEndpoints.applyPromocode).toBe('string');
    });

    it('removePromocode должен быть строкой', () => {
      expect(typeof cartEndpoints.removePromocode).toBe('string');
    });
  });
});
