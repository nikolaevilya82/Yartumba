import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

interface CartItem {
  id: number;
  furniture_type: string;
  furniture_id: number;
  quantity: number;
  price: number;
}

interface Cart {
  items: CartItem[];
  total_items: number;
  total_price: number;
}

class SimpleCartStore {
  cart: Cart | null = null;

  get items(): CartItem[] {
    return this.cart?.items ?? [];
  }

  get totalItems(): number {
    return this.cart?.total_items ?? 0;
  }

  get totalPrice(): number {
    return this.cart?.total_price ?? 0;
  }

  get isEmpty(): boolean {
    return this.items.length === 0;
  }

  updateFromResponse(cart: Cart | null) {
    this.cart = cart;
  }

  clear() {
    this.cart = null;
  }
}

describe('Cart Store', () => {
  let cartStore: SimpleCartStore;

  beforeEach(() => {
    vi.clearAllMocks();
    cartStore = new SimpleCartStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь пустую корзину по умолчанию', () => {
      expect(cartStore.cart).toBeNull();
    });

    it('должен иметь пустой список товаров', () => {
      expect(cartStore.items).toEqual([]);
    });

    it('должен иметь 0 товаров', () => {
      expect(cartStore.totalItems).toBe(0);
    });

    it('должен иметь 0 общую цену', () => {
      expect(cartStore.totalPrice).toBe(0);
    });

    it('должен быть пустым', () => {
      expect(cartStore.isEmpty).toBe(true);
    });
  });

  describe('items getter', () => {
    it('должен возвращать пустой массив при null корзине', () => {
      expect(cartStore.items).toEqual([]);
    });

    it('должен возвращать товары из корзины', () => {
      const mockCart: Cart = {
        items: [
          { id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 2, price: 5000 },
          { id: 2, furniture_type: 'nightstand', furniture_id: 2, quantity: 1, price: 3000 },
        ],
        total_items: 3,
        total_price: 13000,
      };
      cartStore.updateFromResponse(mockCart);
      
      expect(cartStore.items).toHaveLength(2);
      expect(cartStore.items[0].id).toBe(1);
    });
  });

  describe('totalItems getter', () => {
    it('должен возвращать 0 при null корзине', () => {
      expect(cartStore.totalItems).toBe(0);
    });

    it('должен возвращать общее количество товаров', () => {
      const mockCart: Cart = {
        items: [
          { id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 2, price: 5000 },
          { id: 2, furniture_type: 'nightstand', furniture_id: 2, quantity: 3, price: 3000 },
        ],
        total_items: 5,
        total_price: 19000,
      };
      cartStore.updateFromResponse(mockCart);
      
      expect(cartStore.totalItems).toBe(5);
    });
  });

  describe('totalPrice getter', () => {
    it('должен возвращать 0 при null корзине', () => {
      expect(cartStore.totalPrice).toBe(0);
    });

    it('должен возвращать общую цену', () => {
      const mockCart: Cart = {
        items: [
          { id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 2, price: 5000 },
        ],
        total_items: 2,
        total_price: 10000,
      };
      cartStore.updateFromResponse(mockCart);
      
      expect(cartStore.totalPrice).toBe(10000);
    });
  });

  describe('isEmpty getter', () => {
    it('должен возвращать true при пустой корзине', () => {
      expect(cartStore.isEmpty).toBe(true);
    });

    it('должен возвращать false при товарах в корзине', () => {
      const mockCart: Cart = {
        items: [{ id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 1, price: 5000 }],
        total_items: 1,
        total_price: 5000,
      };
      cartStore.updateFromResponse(mockCart);
      
      expect(cartStore.isEmpty).toBe(false);
    });
  });

  describe('updateFromResponse', () => {
    it('должен обновлять корзину из ответа', () => {
      const mockCart: Cart = {
        items: [{ id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 1, price: 5000 }],
        total_items: 1,
        total_price: 5000,
      };
      
      cartStore.updateFromResponse(mockCart);
      
      expect(cartStore.cart).toEqual(mockCart);
      expect(cartStore.items).toHaveLength(1);
    });

    it('должен очищать корзину при null', () => {
      const mockCart: Cart = {
        items: [{ id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 1, price: 5000 }],
        total_items: 1,
        total_price: 5000,
      };
      cartStore.updateFromResponse(mockCart);
      
      cartStore.updateFromResponse(null);
      
      expect(cartStore.cart).toBeNull();
      expect(cartStore.items).toEqual([]);
    });
  });

  describe('clear', () => {
    it('должен очищать корзину', () => {
      const mockCart: Cart = {
        items: [{ id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 1, price: 5000 }],
        total_items: 1,
        total_price: 5000,
      };
      cartStore.updateFromResponse(mockCart);
      
      cartStore.clear();
      
      expect(cartStore.cart).toBeNull();
      expect(cartStore.items).toEqual([]);
      expect(cartStore.totalItems).toBe(0);
      expect(cartStore.totalPrice).toBe(0);
    });
  });

  describe('reactivity', () => {
    it('должен обновлять геттеры при изменении корзины', () => {
      const mockCart1: Cart = {
        items: [{ id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 1, price: 5000 }],
        total_items: 1,
        total_price: 5000,
      };
      cartStore.updateFromResponse(mockCart1);
      
      expect(cartStore.totalItems).toBe(1);
      
      const mockCart2: Cart = {
        items: [
          { id: 1, furniture_type: 'bookshelf', furniture_id: 1, quantity: 2, price: 5000 },
          { id: 2, furniture_type: 'nightstand', furniture_id: 2, quantity: 1, price: 3000 },
        ],
        total_items: 3,
        total_price: 13000,
      };
      cartStore.updateFromResponse(mockCart2);
      
      expect(cartStore.totalItems).toBe(3);
      expect(cartStore.totalPrice).toBe(13000);
    });
  });
});
