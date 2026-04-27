import { describe, it, expect } from 'vitest';
import {
  formatPrice,
  formatPriceOnly,
  formatPriceWithSymbol,
  calculateDiscount,
  calculateSalePrice,
  formatPriceRange,
  formatLargePrice,
  roundPrice,
  isSalePrice,
} from '@/core/utils/price.utils';

describe('price.utils', () => {
  describe('formatPrice', () => {
    it('должен форматировать положительную цену', () => {
      const result = formatPrice(1000);
      expect(result.replace(/\s/g, ' ')).toBe('1 000 ₽');
    });

    it('должен форматировать ноль', () => {
      const result = formatPrice(0);
      expect(result.replace(/\s/g, ' ')).toBe('0 ₽');
    });

    it('должен обрабатывать отрицательные числа', () => {
      const result = formatPrice(-1000);
      expect(result.replace(/\s/g, ' ')).toBe('-1 000 ₽');
    });

    it('должен округлять до 2 знаков', () => {
      const result = formatPrice(1000.123);
      expect(result.replace(/\s/g, ' ')).toBe('1 000,12 ₽');
    });

    it('должен форматировать большие числа', () => {
      const result = formatPrice(1000000);
      expect(result.replace(/\s/g, ' ')).toBe('1 000 000 ₽');
    });

    it('должен обрабатывать дробные цены', () => {
      const result = formatPrice(99.99);
      expect(result.replace(/\s/g, ' ')).toBe('99,99 ₽');
    });
  });

  describe('formatPriceOnly', () => {
    it('должен форматировать цену без валюты', () => {
      expect(formatPriceOnly(1000).replace(/\s/g, ' ')).toBe('1 000');
    });

    it('должен обрабатывать ноль', () => {
      expect(formatPriceOnly(0).replace(/\s/g, ' ')).toBe('0');
    });

    it('должен обрабатывать отрицательные числа', () => {
      expect(formatPriceOnly(-500).replace(/\s/g, ' ')).toBe('-500');
    });
  });

  describe('formatPriceWithSymbol', () => {
    it('должен форматировать с символом по умолчанию', () => {
      expect(formatPriceWithSymbol(1000).replace(/\s/g, ' ')).toBe('1 000 ₽');
    });

    it('должен форматировать с кастомным символом', () => {
      expect(formatPriceWithSymbol(1000, '$').replace(/\s/g, ' ')).toBe('1 000 $');
      expect(formatPriceWithSymbol(1000, '€').replace(/\s/g, ' ')).toBe('1 000 €');
    });

    it('должен обрабатывать дробные цены', () => {
      expect(formatPriceWithSymbol(1234.56, '₽').replace(/\s/g, ' ')).toBe('1 234,56 ₽');
    });
  });

  describe('calculateDiscount', () => {
    it('должен рассчитывать скидку корректно', () => {
      expect(calculateDiscount(1000, 800)).toBe(20);
      expect(calculateDiscount(1000, 500)).toBe(50);
      expect(calculateDiscount(1000, 0)).toBe(100);
    });

    it('должен возвращать 0 при нулевой или отрицательной исходной цене', () => {
      expect(calculateDiscount(0, 500)).toBe(0);
      expect(calculateDiscount(-100, 500)).toBe(0);
    });

    it('должен возвращать 0 при цене продажи больше или равной исходной', () => {
      expect(calculateDiscount(1000, 1000)).toBe(0);
      expect(calculateDiscount(1000, 1500)).toBe(0);
    });

    it('должен возвращать 0 при отрицательной цене продажи', () => {
      expect(calculateDiscount(1000, -100)).toBe(0);
    });

    it('должен округлять до целого числа', () => {
      expect(calculateDiscount(333, 111)).toBe(67);
    });
  });

  describe('calculateSalePrice', () => {
    it('должен рассчитывать цену со скидкой корректно', () => {
      expect(calculateSalePrice(1000, 20)).toBe(800);
      expect(calculateSalePrice(1000, 50)).toBe(500);
      expect(calculateSalePrice(1000, 0)).toBe(1000);
    });

    it('должен возвращать исходную цену при недопустимом проценте скидки', () => {
      expect(calculateSalePrice(1000, -10)).toBe(1000);
      expect(calculateSalePrice(1000, 101)).toBe(1000);
    });

    it('должен обрабатывать 100% скидку', () => {
      expect(calculateSalePrice(1000, 100)).toBe(0);
    });

    it('должен округлять до 2 знаков', () => {
      expect(calculateSalePrice(1000, 33.33)).toBe(666.7);
    });
  });

  describe('formatPriceRange', () => {
    it('должен форматировать диапазон цен', () => {
      expect(formatPriceRange(1000, 2000).replace(/\s/g, ' ')).toBe('1 000 ₽ – 2 000 ₽');
    });

    it('должен обрабатывать одинаковые цены', () => {
      expect(formatPriceRange(1000, 1000).replace(/\s/g, ' ')).toBe('1 000 ₽ – 1 000 ₽');
    });

    it('должен обрабатывать нули', () => {
      expect(formatPriceRange(0, 1000).replace(/\s/g, ' ')).toBe('0 ₽ – 1 000 ₽');
    });
  });

  describe('formatLargePrice', () => {
    it('должен форматировать большие цены (без символа валюты)', () => {
      expect(formatLargePrice(1000000)).toBe('1 000 000');
    });

    it('должен работать с обычными ценами (без символа валюты)', () => {
      expect(formatLargePrice(1000)).toBe('1 000');
    });
  });

  describe('roundPrice', () => {
    it('должен округлять до целого по умолчанию', () => {
      expect(roundPrice(1234.567)).toBe(1235);
    });

    it('должен округлять до указанной точности', () => {
      expect(roundPrice(1234.567, 1)).toBe(1234.6);
      expect(roundPrice(1234.567, 2)).toBe(1234.57);
      expect(roundPrice(1234.567, 3)).toBe(1234.567);
    });

    it('должен обрабатывать отрицательные числа', () => {
      expect(roundPrice(-1234.567, 2)).toBe(-1234.57);
    });

    it('должен обрабатывать ноль', () => {
      expect(roundPrice(0)).toBe(0);
    });
  });

  describe('isSalePrice', () => {
    it('должен возвращать true для акционной цены', () => {
      expect(isSalePrice(1000, 800)).toBe(true);
      expect(isSalePrice(1000, 1)).toBe(true);
    });

    it('должен возвращать false при равных ценах', () => {
      expect(isSalePrice(1000, 1000)).toBe(false);
    });

    it('должен возвращать false при цене продажи больше', () => {
      expect(isSalePrice(1000, 1500)).toBe(false);
    });

    it('должен возвращать false при нулевой цене продажи', () => {
      expect(isSalePrice(1000, 0)).toBe(false);
    });

    it('должен возвращать false при отрицательной цене', () => {
      expect(isSalePrice(1000, -100)).toBe(false);
    });
  });
});
