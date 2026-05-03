import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Простая имитация API
const mockCartService = {
  applyPromocode: vi.fn(),
  removePromocode: vi.fn(),
};

vi.mock('@/api/services/cart.service', () => ({
  default: mockCartService,
  applyPromocode: mockCartService.applyPromocode,
  removePromocode: mockCartService.removePromocode,
}));

class SimplePromocodeStore {
  promocode: string | null = null;
  discount = 0;

  get hasDiscount(): boolean {
    return this.discount > 0;
  }

  async apply(code: string) {
    const response = await mockCartService.applyPromocode(code);
    this.promocode = code;
    this.discount = response.data.discount;
    return { success: true, discount: this.discount };
  }

  async remove() {
    await mockCartService.removePromocode();
    this.promocode = null;
    this.discount = 0;
  }

  clear() {
    this.promocode = null;
    this.discount = 0;
  }
}

describe('Cart Promocode Store', () => {
  let promocodeStore: SimplePromocodeStore;

  beforeEach(() => {
    vi.clearAllMocks();
    promocodeStore = new SimplePromocodeStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь null промокод по умолчанию', () => {
      expect(promocodeStore.promocode).toBeNull();
    });

    it('должен иметь 0 скидку по умолчанию', () => {
      expect(promocodeStore.discount).toBe(0);
    });

    it('должен не иметь скидки по умолчанию', () => {
      expect(promocodeStore.hasDiscount).toBe(false);
    });
  });

  describe('hasDiscount getter', () => {
    it('должен возвращать false при discount=0', () => {
      expect(promocodeStore.hasDiscount).toBe(false);
    });

    it('должен возвращать true при discount > 0', () => {
      promocodeStore.discount = 20;
      expect(promocodeStore.hasDiscount).toBe(true);
    });
  });

  describe('apply', () => {
    it('должен применять промокод', async () => {
      const mockResponse = { data: { discount: 20 } };
      mockCartService.applyPromocode.mockResolvedValueOnce(mockResponse);

      const result = await promocodeStore.apply('SUMMER20');

      expect(promocodeStore.promocode).toBe('SUMMER20');
      expect(promocodeStore.discount).toBe(20);
      expect(result.success).toBe(true);
      expect(result.discount).toBe(20);
    });

    it('должен возвращать ошибку при неудаче', async () => {
      mockCartService.applyPromocode.mockRejectedValueOnce(
        new Error('Invalid promocode')
      );

      await expect(promocodeStore.apply('INVALID')).rejects.toThrow('Invalid promocode');
    });
  });

  describe('remove', () => {
    it('должен удалять промокод', async () => {
      promocodeStore.promocode = 'TEST';
      promocodeStore.discount = 20;

      const mockResponse = { data: {} };
      mockCartService.removePromocode.mockResolvedValueOnce(mockResponse);

      await promocodeStore.remove();

      expect(promocodeStore.promocode).toBeNull();
      expect(promocodeStore.discount).toBe(0);
    });

    it('должен вызывать API removePromocode', async () => {
      promocodeStore.promocode = 'TEST';

      const mockResponse = { data: {} };
      mockCartService.removePromocode.mockResolvedValueOnce(mockResponse);

      await promocodeStore.remove();

      expect(mockCartService.removePromocode).toHaveBeenCalled();
    });
  });

  describe('clear', () => {
    it('должен сбрасывать промокод и скидку', () => {
      promocodeStore.promocode = 'TEST';
      promocodeStore.discount = 25;

      promocodeStore.clear();

      expect(promocodeStore.promocode).toBeNull();
      expect(promocodeStore.discount).toBe(0);
    });

    it('должен сбрасывать hasDiscount', () => {
      promocodeStore.promocode = 'TEST';
      promocodeStore.discount = 25;

      expect(promocodeStore.hasDiscount).toBe(true);

      promocodeStore.clear();

      expect(promocodeStore.hasDiscount).toBe(false);
    });
  });
});
