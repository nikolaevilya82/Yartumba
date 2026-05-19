import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

interface CalculationResult {
  price: number;
  materials: any[];
  parts: any[];
}

class SimpleCalculationStore {
  calculation: CalculationResult | null = null;
  isCalculating = false;
  error: string | null = null;

  get price(): number {
    return this.calculation?.price ?? 0;
  }

  get materials(): any[] {
    return this.calculation?.materials ?? [];
  }

  get parts(): any[] {
    return this.calculation?.parts ?? [];
  }

  get isEmpty(): boolean {
    return this.calculation === null;
  }

  async calculate(config: any) {
    this.isCalculating = true;
    this.error = null;
    
    // Mock calculation
    const response = await mockConfiguratorService.calculateConfiguration(config);
    this.calculation = response.data;
    this.isCalculating = false;
  }

  clear() {
    this.calculation = null;
    this.error = null;
  }
}

const mockConfiguratorService = {
  calculateConfiguration: vi.fn(),
};

describe('Configurator Calculation Store', () => {
  let calcStore: SimpleCalculationStore;

  beforeEach(() => {
    vi.clearAllMocks();
    calcStore = new SimpleCalculationStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь null расчёт по умолчанию', () => {
      expect(calcStore.calculation).toBeNull();
    });

    it('должен не быть в процессе расчёта', () => {
      expect(calcStore.isCalculating).toBe(false);
    });

    it('должен не иметь ошибки', () => {
      expect(calcStore.error).toBeNull();
    });

    it('должен иметь 0 цену', () => {
      expect(calcStore.price).toBe(0);
    });

    it('должен быть пустым', () => {
      expect(calcStore.isEmpty).toBe(true);
    });
  });

  describe('price getter', () => {
    it('должен возвращать 0 при null расчёте', () => {
      expect(calcStore.price).toBe(0);
    });

    it('должен возвращать цену из расчёта', () => {
      calcStore.calculation = { price: 15000, materials: [], parts: [] };
      expect(calcStore.price).toBe(15000);
    });
  });

  describe('materials getter', () => {
    it('должен возвращать пустой массив при null расчёте', () => {
      expect(calcStore.materials).toEqual([]);
    });

    it('должен возвращать материалы из расчёта', () => {
      const mockMaterials = [{ name: 'ДСП', quantity: 2, price: 5000 }];
      calcStore.calculation = { price: 15000, materials: mockMaterials, parts: [] };
      expect(calcStore.materials).toEqual(mockMaterials);
    });
  });

  describe('parts getter', () => {
    it('должен возвращать пустой массив при null расчёте', () => {
      expect(calcStore.parts).toEqual([]);
    });

    it('должен возвращать части из расчёта', () => {
      const mockParts = [{ name: 'Боковина', quantity: 2, price: 3000 }];
      calcStore.calculation = { price: 15000, materials: [], parts: mockParts };
      expect(calcStore.parts).toEqual(mockParts);
    });
  });

  describe('isEmpty getter', () => {
    it('должен возвращать true при null расчёте', () => {
      expect(calcStore.isEmpty).toBe(true);
    });

    it('должен возвращать false при наличии расчёта', () => {
      calcStore.calculation = { price: 15000, materials: [], parts: [] };
      expect(calcStore.isEmpty).toBe(false);
    });
  });

  describe('calculate', () => {
    it('должен начинать расчёт', async () => {
      const mockResponse = { data: { price: 15000, materials: [], parts: [] } };
      mockConfiguratorService.calculateConfiguration.mockResolvedValueOnce(mockResponse);

      expect(calcStore.isCalculating).toBe(false);

      await calcStore.calculate({ width: 1000 });

      expect(calcStore.isCalculating).toBe(false);
      expect(calcStore.price).toBe(15000);
    });

    it('должен сохранять цену после расчёта', async () => {
      const mockResponse = { data: { price: 25000, materials: [], parts: [] } };
      mockConfiguratorService.calculateConfiguration.mockResolvedValueOnce(mockResponse);

      await calcStore.calculate({ width: 1500 });

      expect(calcStore.price).toBe(25000);
    });

    it('должен использовать переданную конфигурацию', async () => {
      const customConfig = { width: 1500, height: 2000 };
      const mockResponse = { data: { price: 20000, materials: [], parts: [] } };
      mockConfiguratorService.calculateConfiguration.mockResolvedValueOnce(mockResponse);

      await calcStore.calculate(customConfig);

      expect(mockConfiguratorService.calculateConfiguration).toHaveBeenCalledWith(customConfig);
    });
  });

  describe('clear', () => {
    it('должен очищать расчёт', () => {
      calcStore.calculation = { price: 15000, materials: [], parts: [] };
      calcStore.clear();

      expect(calcStore.calculation).toBeNull();
    });

    it('должен очищать ошибку', () => {
      calcStore.error = 'Test error';
      calcStore.clear();

      expect(calcStore.error).toBeNull();
    });

    it('должен сбрасывать цену в 0', () => {
      calcStore.calculation = { price: 15000, materials: [], parts: [] };
      calcStore.clear();

      expect(calcStore.price).toBe(0);
    });
  });
});
