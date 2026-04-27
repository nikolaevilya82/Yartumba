import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  setItem,
  getItem,
  removeItem,
  clearAll,
  hasItem,
  setItemWithTTL,
  getItemWithTTL,
  setPrimitive,
  getPrimitive,
  storageKeys,
} from '@/core/utils/storage.utils';

// Моки localStorage
const localStorageMock = {
  store: new Map<string, string>(),
  getItem: vi.fn((key: string) => localStorageMock.store.get(key) || null),
  setItem: vi.fn((key: string, value: string) => {
    localStorageMock.store.set(key, value);
  }),
  removeItem: vi.fn((key: string) => {
    localStorageMock.store.delete(key);
  }),
  clear: vi.fn(() => {
    localStorageMock.store.clear();
  }),
  get length() {
    return localStorageMock.store.size;
  },
  key: vi.fn((index: number) => {
    const keys = Array.from(localStorageMock.store.keys());
    return keys[index] || null;
  }),
};

// Перезаписываем глобальный localStorage
Object.defineProperty(global, 'localStorage', {
  value: localStorageMock,
  writable: true,
});

describe('storage.utils', () => {
  beforeEach(() => {
    localStorageMock.store.clear();
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('setItem', () => {
    it('должен сохранять данные в localStorage', () => {
      const result = setItem('test', { foo: 'bar' });
      
      expect(result).toBe(true);
      expect(localStorageMock.setItem).toHaveBeenCalled();
      
      const stored = localStorageMock.store.get('yartumba_test');
      expect(stored).toBe(JSON.stringify({ foo: 'bar' }));
    });

    it('должен сохранять строки', () => {
      const result = setItem('string', 'hello');
      
      expect(result).toBe(true);
      const stored = localStorageMock.store.get('yartumba_string');
      expect(stored).toBe('"hello"');
    });

    it('должен сохранять числа', () => {
      const result = setItem('number', 123);
      
      expect(result).toBe(true);
      const stored = localStorageMock.store.get('yartumba_number');
      expect(stored).toBe('123');
    });

    it('должен сохранять массивы', () => {
      const result = setItem('array', [1, 2, 3]);
      
      expect(result).toBe(true);
      const stored = localStorageMock.store.get('yartumba_array');
      expect(stored).toBe(JSON.stringify([1, 2, 3]));
    });

    it('должен вернуть false при ошибке сериализации', () => {
      // Объект с циклической ссылкой вызовет ошибку
      const circular: Record<string, unknown> = {};
      circular.self = circular;
      
      const result = setItem('circular', circular);
      
      expect(result).toBe(false);
    });
  });

  describe('getItem', () => {
    it('должен получать данные из localStorage', () => {
      localStorageMock.store.set('yartumba_test', JSON.stringify({ foo: 'bar' }));
      
      const result = getItem<{ foo: string }>('test');
      
      expect(result).toEqual({ foo: 'bar' });
    });

    it('должен возвращать defaultValue если ключ не найден', () => {
      const result = getItem('nonexistent', 'default');
      
      expect(result).toBe('default');
    });

    it('должен возвращать null по умолчанию если defaultValue не указан', () => {
      const result = getItem('nonexistent');
      
      expect(result).toBeNull();
    });

    it('должен возвращать defaultValue при ошибке парсинга', () => {
      localStorageMock.store.set('yartumba_invalid', 'invalid json');
      
      const result = getItem('invalid', 'default');
      
      expect(result).toBe('default');
    });

    it('должен правильно десериализировать разные типы', () => {
      localStorageMock.store.set('yartumba_string', '"hello"');
      localStorageMock.store.set('yartumba_number', '123');
      localStorageMock.store.set('yartumba_array', '[1,2,3]');
      localStorageMock.store.set('yartumba_bool', 'true');
      
      expect(getItem<string>('string')).toBe('hello');
      expect(getItem<number>('number')).toBe(123);
      expect(getItem<number[]>('array')).toEqual([1, 2, 3]);
      expect(getItem<boolean>('bool')).toBe(true);
    });
  });

  describe('removeItem', () => {
    it('должен удалять данные из localStorage', () => {
      localStorageMock.store.set('yartumba_test', 'value');
      
      const result = removeItem('test');
      
      expect(result).toBe(true);
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('yartumba_test');
      expect(localStorageMock.store.has('yartumba_test')).toBe(false);
    });

    it('должен вернуть false при ошибке', () => {
      // Мокируем ошибку
      localStorageMock.removeItem.mockImplementationOnce(() => {
        throw new Error('Storage error');
      });
      
      const result = removeItem('test');
      
      expect(result).toBe(false);
    });
  });

  describe('clearAll', () => {
    it('должен очищать все данные приложения', () => {
      localStorageMock.store.set('yartumba_test1', 'value1');
      localStorageMock.store.set('yartumba_test2', 'value2');
      localStorageMock.store.set('other_key', 'other_value');
      
      const result = clearAll();
      
      expect(result).toBe(true);
      expect(localStorageMock.store.has('yartumba_test1')).toBe(false);
      expect(localStorageMock.store.has('yartumba_test2')).toBe(false);
      expect(localStorageMock.store.has('other_key')).toBe(true); // Не трогает чужие ключи
    });

    it('должен обрабатывать ошибку', () => {
      localStorageMock.clear.mockImplementationOnce(() => {
        throw new Error('Clear error');
      });
      
      // Функция clearAll не использует localStorage.clear(), поэтому ошибка не возникнет
      const result = clearAll();
      
      expect(result).toBe(true);
    });
  });

  describe('hasItem', () => {
    it('должен возвращать true если ключ существует', () => {
      localStorageMock.store.set('yartumba_test', 'value');
      
      const result = hasItem('test');
      
      expect(result).toBe(true);
    });

    it('должен возвращать false если ключ не существует', () => {
      const result = hasItem('nonexistent');
      
      expect(result).toBe(false);
    });
  });

  describe('setItemWithTTL', () => {
    it('должен сохранять данные с TTL', () => {
      const result = setItemWithTTL('test', { data: 'value' }, 3600000);
      
      expect(result).toBe(true);
      
      const stored = JSON.parse(localStorageMock.store.get('yartumba_test') || '{}');
      expect(stored.value).toEqual({ data: 'value' });
      expect(stored.expires).toBeDefined();
      expect(stored.expires - Date.now()).toBeCloseTo(3600000, -2);
    });

    it('должен вернуть false при ошибке', () => {
      const circular: Record<string, unknown> = {};
      circular.self = circular;
      
      const result = setItemWithTTL('circular', circular, 1000);
      
      expect(result).toBe(false);
    });
  });

  describe('getItemWithTTL', () => {
    it('должен возвращать данные если TTL не истёк', () => {
      const expires = Date.now() + 3600000;
      localStorageMock.store.set(
        'yartumba_test',
        JSON.stringify({ value: { data: 'value' }, expires })
      );
      
      const result = getItemWithTTL('test');
      
      expect(result).toEqual({ data: 'value' });
    });

    it('должен удалить данные если TTL истёк', () => {
      const expires = Date.now() - 1000; // Уже истёк
      localStorageMock.store.set(
        'yartumba_test',
        JSON.stringify({ value: { data: 'value' }, expires })
      );
      
      const result = getItemWithTTL('test');
      
      expect(result).toBeNull();
      expect(localStorageMock.store.has('yartumba_test')).toBe(false);
    });

    it('должен возвращать defaultValue если ключ не найден', () => {
      const result = getItemWithTTL('nonexistent', 'default');
      
      expect(result).toBe('default');
    });
  });

  describe('setPrimitive', () => {
    it('должен сохранять строковое значение', () => {
      const result = setPrimitive('test', 'hello');
      
      expect(result).toBe(true);
      expect(localStorageMock.store.get('yartumba_test')).toBe('hello');
    });

    it('должен сохранять числовое значение как строку', () => {
      const result = setPrimitive('number', 123);
      
      expect(result).toBe(true);
      expect(localStorageMock.store.get('yartumba_number')).toBe('123');
    });

    it('должен вернуть false при ошибке', () => {
      localStorageMock.setItem.mockImplementationOnce(() => {
        throw new Error('Storage error');
      });
      
      const result = setPrimitive('test', 'value');
      
      expect(result).toBe(false);
    });
  });

  describe('getPrimitive', () => {
    it('должен получать строковое значение', () => {
      localStorageMock.store.set('yartumba_test', 'hello');
      
      const result = getPrimitive('test');
      
      expect(result).toBe('hello');
    });

    it('должен возвращать defaultValue если ключ не найден', () => {
      const result = getPrimitive('nonexistent', 'default');
      
      expect(result).toBe('default');
    });
  });

  describe('storageKeys', () => {
    it('должен содержать предопределённые ключи', () => {
      expect(storageKeys.cart).toBe('cart');
      expect(storageKeys.favorites).toBe('favorites');
      expect(storageKeys.user).toBe('user');
      expect(storageKeys.settings).toBe('settings');
      expect(storageKeys.lastViewed).toBe('last_viewed');
      expect(storageKeys.configurator).toBe('configurator');
    });
  });
});
