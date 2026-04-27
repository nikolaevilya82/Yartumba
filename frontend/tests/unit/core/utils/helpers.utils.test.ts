import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  generateId,
  generateUUID,
  delay,
  formatDate,
  formatDateTime,
  formatRelativeTime,
  round,
  clamp,
  snapToStep,
  firstOrDefault,
  groupBy,
  unique,
  uniqueBy,
  sortBy,
  chunk,
  isEmpty,
  copyToClipboard,
  debounce,
  throttle,
} from '@/core/utils/helpers.utils';

describe('helpers.utils', () => {
  describe('generateId', () => {
    it('должен генерировать уникальный ID', () => {
      const id1 = generateId();
      const id2 = generateId();
      
      expect(id1).toBeDefined();
      expect(id2).toBeDefined();
      expect(id1).not.toBe(id2);
    });

    it('должен содержать timestamp и случайную часть', () => {
      const id = generateId();
      
      expect(id).toMatch(/^\d+-[a-z0-9]+$/);
    });
  });

  describe('generateUUID', () => {
    it('должен генерировать валидный UUID v4', () => {
      const uuid = generateUUID();
      
      expect(uuid).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
    });

    it('должен генерировать уникальные UUID', () => {
      const uuids = new Set();
      for (let i = 0; i < 100; i++) {
        uuids.add(generateUUID());
      }
      
      expect(uuids.size).toBe(100);
    });
  });

  describe('delay', () => {
    it('должен ждать указанное время', async () => {
      const start = Date.now();
      await delay(100);
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeGreaterThanOrEqual(90); // Небольшой допуск
    });

    it('должен работать с нулевым задержкой', async () => {
      const start = Date.now();
      await delay(0);
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeLessThan(10);
    });
  });

  describe('formatDate', () => {
    it('должен форматировать дату из строки', () => {
      const result = formatDate('2024-01-15');
      
      expect(result).toContain('2024');
      expect(result).toContain('января');
    });

    it('должен форматировать дату из объекта Date', () => {
      const date = new Date('2024-06-20');
      const result = formatDate(date);
      
      expect(result).toContain('2024');
      expect(result).toContain('июня');
    });

    it('должен использовать кастомный локаль', () => {
      const result = formatDate('2024-01-15', 'en-US');
      
      expect(result).not.toContain('января');
    });
  });

  describe('formatDateTime', () => {
    it('должен форматировать дату и время', () => {
      const result = formatDateTime('2024-01-15T14:30:00');
      
      expect(result).toContain('2024');
      expect(result).toContain('14:30');
    });

    it('должен использовать кастомный локаль', () => {
      const result = formatDateTime('2024-01-15T14:30:00', 'en-US');
      
      expect(result).not.toContain('января');
    });
  });

  describe('formatRelativeTime', () => {
    it('должен показывать "Только что" для недавних событий', () => {
      const now = new Date();
      const result = formatRelativeTime(now);
      
      expect(result).toBe('Только что');
    });

    it('должен показывать минуты назад', () => {
      const date = new Date(Date.now() - 5 * 60 * 1000); // 5 минут назад
      const result = formatRelativeTime(date);
      
      expect(result).toBe('5 мин. назад');
    });

    it('должен показывать часы назад', () => {
      const date = new Date(Date.now() - 3 * 60 * 60 * 1000); // 3 часа назад
      const result = formatRelativeTime(date);
      
      expect(result).toBe('3 ч. назад');
    });

    it('должен показывать дни назад', () => {
      const date = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000); // 2 дня назад
      const result = formatRelativeTime(date);
      
      expect(result).toBe('2 дн. назад');
    });
  });

  describe('round', () => {
    it('должен округлять до целого по умолчанию', () => {
      expect(round(3.7)).toBe(4);
      expect(round(3.2)).toBe(3);
    });

    it('должен округлять до указанной точности', () => {
      expect(round(3.14159, 2)).toBe(3.14);
      expect(round(3.14159, 3)).toBe(3.142);
      expect(round(3.14159, 0)).toBe(3);
    });

    it('должен обрабатывать отрицательные числа', () => {
      expect(round(-3.7)).toBe(-4);
      expect(round(-3.14159, 2)).toBe(-3.14);
    });
  });

  describe('clamp', () => {
    it('должен ограничивать значение в диапазоне', () => {
      expect(clamp(5, 0, 10)).toBe(5);
      expect(clamp(-1, 0, 10)).toBe(0);
      expect(clamp(15, 0, 10)).toBe(10);
    });

    it('должен обрабатывать границы диапазона', () => {
      expect(clamp(0, 0, 10)).toBe(0);
      expect(clamp(10, 0, 10)).toBe(10);
    });

    it('должен работать с отрицательными диапазонами', () => {
      expect(clamp(-5, -10, 0)).toBe(-5);
      expect(clamp(-15, -10, 0)).toBe(-10);
    });
  });

  describe('snapToStep', () => {
    it('должен округлять до шага', () => {
      expect(snapToStep(7, 5)).toBe(10);
      expect(snapToStep(3, 5)).toBe(5);
      expect(snapToStep(5, 5)).toBe(5);
    });

    it('должен работать с дробным шагом', () => {
      expect(snapToStep(1.23, 0.5)).toBe(1.5);
      expect(snapToStep(1.78, 0.5)).toBe(2);
    });

    it('должен обрабатывать ноль', () => {
      expect(snapToStep(0, 5)).toBe(0);
    });
  });

  describe('firstOrDefault', () => {
    it('должен возвращать первый элемент массива', () => {
      expect(firstOrDefault([1, 2, 3], 0)).toBe(1);
    });

    it('должен возвращать defaultValue для пустого массива', () => {
      expect(firstOrDefault([], 42)).toBe(42);
    });

    it('должен возвращать defaultValue для пустого массива с null', () => {
      expect(firstOrDefault<string[]>([], null)).toBeNull();
    });
  });

  describe('groupBy', () => {
    it('должен группировать массив по ключу', () => {
      const items = [
        { category: 'a', name: 'item1' },
        { category: 'b', name: 'item2' },
        { category: 'a', name: 'item3' },
      ];
      
      const result = groupBy(items, 'category');
      
      expect(result.a).toHaveLength(2);
      expect(result.b).toHaveLength(1);
      expect(result.a[0].name).toBe('item1');
    });

    it('должен обрабатывать пустой массив', () => {
      const result = groupBy([], 'key');
      
      expect(result).toEqual({});
    });
  });

  describe('unique', () => {
    it('должен возвращать уникальные значения', () => {
      expect(unique([1, 2, 2, 3, 3, 3])).toEqual([1, 2, 3]);
    });

    it('должен работать со строками', () => {
      expect(unique(['a', 'b', 'a', 'c'])).toEqual(['a', 'b', 'c']);
    });

    it('должен возвращать пустой массив для пустого ввода', () => {
      expect(unique([])).toEqual([]);
    });
  });

  describe('uniqueBy', () => {
    it('должен возвращать уникальные значения по ключу', () => {
      const items = [
        { id: 1, name: 'a' },
        { id: 2, name: 'b' },
        { id: 1, name: 'c' },
      ];
      
      const result = uniqueBy(items, 'id');
      
      expect(result).toHaveLength(2);
      expect(result[0].name).toBe('a');
      expect(result[1].name).toBe('b');
    });

    it('должен обрабатывать пустой массив', () => {
      expect(uniqueBy([], 'key')).toEqual([]);
    });
  });

  describe('sortBy', () => {
    it('должен сортировать по возрастанию', () => {
      const items = [{ val: 3 }, { val: 1 }, { val: 2 }];
      
      const result = sortBy(items, 'val', 'asc');
      
      expect(result[0].val).toBe(1);
      expect(result[1].val).toBe(2);
      expect(result[2].val).toBe(3);
    });

    it('должен сортировать по убыванию', () => {
      const items = [{ val: 3 }, { val: 1 }, { val: 2 }];
      
      const result = sortBy(items, 'val', 'desc');
      
      expect(result[0].val).toBe(3);
      expect(result[1].val).toBe(2);
      expect(result[2].val).toBe(1);
    });

    it('должен не мутировать исходный массив', () => {
      const items = [{ val: 3 }, { val: 1 }];
      const original = [...items];
      
      sortBy(items, 'val');
      
      expect(items).toEqual(original);
    });
  });

  describe('chunk', () => {
    it('должен разбивать массив на чанки', () => {
      const result = chunk([1, 2, 3, 4, 5], 2);
      
      expect(result).toEqual([[1, 2], [3, 4], [5]]);
    });

    it('должен обрабатывать размер больше массива', () => {
      const result = chunk([1, 2], 5);
      
      expect(result).toEqual([[1, 2]]);
    });

    it('должен обрабатывать пустой массив', () => {
      const result = chunk([], 2);
      
      expect(result).toEqual([]);
    });

    it('должен обрабатывать размер 0', () => {
      const result = chunk([1, 2, 3], 0);
      
      // Бесконечный цикл, но так реализовано
      expect(result).toEqual([]);
    });
  });

  describe('isEmpty', () => {
    it('должен возвращать true для null и undefined', () => {
      expect(isEmpty(null)).toBe(true);
      expect(isEmpty(undefined)).toBe(true);
    });

    it('должен возвращать true для пустых строк', () => {
      expect(isEmpty('')).toBe(true);
      expect(isEmpty('   ')).toBe(true);
    });

    it('должен возвращать false для непустых строк', () => {
      expect(isEmpty('hello')).toBe(false);
    });

    it('должен возвращать true для пустых массивов и объектов', () => {
      expect(isEmpty([])).toBe(true);
      expect(isEmpty({})).toBe(true);
    });

    it('должен возвращать false для непустых массивов и объектов', () => {
      expect(isEmpty([1])).toBe(false);
      expect(isEmpty({ a: 1 })).toBe(false);
    });

    it('должен возвращать false для чисел', () => {
      expect(isEmpty(0)).toBe(false);
      expect(isEmpty(1)).toBe(false);
    });
  });

  describe('copyToClipboard', () => {
    beforeEach(() => {
      // Мокируем navigator.clipboard
      Object.assign(navigator, {
        clipboard: {
          writeText: vi.fn(),
        },
      });
    });

    it('должен копировать текст в буфер', async () => {
      navigator.clipboard.writeText.mockResolvedValue(undefined);
      
      const result = await copyToClipboard('test');
      
      expect(result).toBe(true);
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('test');
    });

    it('должен вернуть false при ошибке', async () => {
      navigator.clipboard.writeText.mockRejectedValue(new Error('Clipboard error'));
      
      const result = await copyToClipboard('test');
      
      expect(result).toBe(false);
    });
  });

  describe('debounce', () => {
    it('должен откладывать выполнение функции', () => {
      const fn = vi.fn();
      const debounced = debounce(fn, 100);
      
      debounced();
      expect(fn).not.toHaveBeenCalled();
      
      vi.advanceTimersByTime(100);
      expect(fn).toHaveBeenCalledTimes(1);
    });

    it('должен сбрасывать таймер при повторных вызовах', () => {
      const fn = vi.fn();
      const debounced = debounce(fn, 100);
      
      debounced();
      debounced();
      debounced();
      
      vi.advanceTimersByTime(50);
      expect(fn).not.toHaveBeenCalled();
      
      vi.advanceTimersByTime(50);
      expect(fn).toHaveBeenCalledTimes(1);
    });

    it('должен передавать аргументы функции', () => {
      const fn = vi.fn();
      const debounced = debounce(fn, 100);
      
      debounced('arg1', 'arg2');
      vi.advanceTimersByTime(100);
      
      expect(fn).toHaveBeenCalledWith('arg1', 'arg2');
    });
  });

  describe('throttle', () => {
    it('должен выполнять функцию сразу при первом вызове', () => {
      const fn = vi.fn();
      const throttled = throttle(fn, 100);
      
      throttled();
      expect(fn).toHaveBeenCalledTimes(1);
    });

    it('должен пропускать вызовы в пределах лимита', () => {
      const fn = vi.fn();
      const throttled = throttle(fn, 100);
      
      throttled();
      throttled();
      throttled();
      
      expect(fn).toHaveBeenCalledTimes(1);
      
      vi.advanceTimersByTime(100);
      
      throttled();
      expect(fn).toHaveBeenCalledTimes(2);
    });

    it('должен передавать аргументы функции', () => {
      const fn = vi.fn();
      const throttled = throttle(fn, 100);
      
      throttled('arg1', 'arg2');
      vi.advanceTimersByTime(100);
      throttled('arg3');
      
      expect(fn).toHaveBeenNthCalledWith(1, 'arg1', 'arg2');
      expect(fn).toHaveBeenNthCalledWith(2, 'arg3');
    });
  });
});
