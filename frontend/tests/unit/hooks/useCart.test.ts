import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useCart } from '@/hooks/useCart';

describe('useCart', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('должен возвращать пустую корзину по умолчанию', () => {
    const result = useCart();
    
    expect(result.items).toEqual([]);
    expect(result.totalItems).toBe(0);
    expect(result.totalPrice).toBe(0);
    expect(result.isEmpty).toBe(true);
  });

  it('должен иметь функции для работы с корзиной', () => {
    const result = useCart();
    
    expect(typeof result.addToCart).toBe('function');
    expect(typeof result.removeFromCart).toBe('function');
    expect(typeof result.updateItemQuantity).toBe('function');
    expect(typeof result.incrementItem).toBe('function');
    expect(typeof result.decrementItem).toBe('function');
    expect(typeof result.clearCart).toBe('function');
  });

  it('должен вызывать addToCart без ошибок', async () => {
    const result = useCart();
    
    await expect(result.addToCart('bookshelf', { width: 1000 }, 1)).resolves.not.toThrow();
  });

  it('должен вызывать removeFromCart без ошибок', () => {
    const result = useCart();
    
    expect(() => result.removeFromCart(123)).not.toThrow();
  });

  it('должен вызывать updateItemQuantity без ошибок', () => {
    const result = useCart();
    
    expect(() => result.updateItemQuantity(123, 5)).not.toThrow();
  });
});

