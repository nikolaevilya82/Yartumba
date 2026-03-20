const STORAGE_PREFIX = 'yartumba_';

/**
 * Получение ключа с префиксом
 */
function getKey(key: string): string {
  return `${STORAGE_PREFIX}${key}`;
}

/**
 * Сохранение данных в localStorage
 */
export function setItem<T>(key: string, value: T): boolean {
  try {
    const serialized = JSON.stringify(value);
    localStorage.setItem(getKey(key), serialized);
    return true;
  } catch (error) {
    console.error(`Error saving to localStorage: ${key}`, error);
    return false;
  }
}

/**
 * Получение данных из localStorage
 */
export function getItem<T>(key: string, defaultValue: T | null = null): T | null {
  try {
    const item = localStorage.getItem(getKey(key));
    if (item === null) return defaultValue;
    return JSON.parse(item) as T;
  } catch (error) {
    console.error(`Error reading from localStorage: ${key}`, error);
    return defaultValue;
  }
}

/**
 * Удаление данных из localStorage
 */
export function removeItem(key: string): boolean {
  try {
    localStorage.removeItem(getKey(key));
    return true;
  } catch (error) {
    console.error(`Error removing from localStorage: ${key}`, error);
    return false;
  }
}

/**
 * Очистка всех данных приложения в localStorage
 */
export function clearAll(): boolean {
  try {
    const keysToRemove: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith(STORAGE_PREFIX)) {
        keysToRemove.push(key);
      }
    }
    keysToRemove.forEach((key) => localStorage.removeItem(key));
    return true;
  } catch (error) {
    console.error('Error clearing localStorage', error);
    return false;
  }
}

/**
 * Проверка существования ключа
 */
export function hasItem(key: string): boolean {
  return localStorage.getItem(getKey(key)) !== null;
}

/**
 * Сохранение с временем жизни (TTL в миллисекундах)
 */
export function setItemWithTTL<T>(key: string, value: T, ttl: number): boolean {
  try {
    const data = {
      value,
      expires: Date.now() + ttl,
    };
    return setItem(key, data);
  } catch {
    return false;
  }
}

/**
 * Получение данных с проверкой TTL
 */
export function getItemWithTTL<T>(key: string, defaultValue: T | null = null): T | null {
  const data = getItem<{ value: T; expires: number }>(key);
  if (!data) return defaultValue;
  if (Date.now() > data.expires) {
    removeItem(key);
    return defaultValue;
  }
  return data.value;
}

/**
 * Сохранение простого значения (строка/число)
 */
export function setPrimitive(key: string, value: string | number): boolean {
  try {
    localStorage.setItem(getKey(key), String(value));
    return true;
  } catch {
    return false;
  }
}

/**
 * Получение простого значения
 */
export function getPrimitive(key: string, defaultValue: string = ''): string {
  return localStorage.getItem(getKey(key)) ?? defaultValue;
}

// Ключи для часто используемых данных
export const storageKeys = {
  cart: 'cart',
  favorites: 'favorites',
  user: 'user',
  settings: 'settings',
  lastViewed: 'last_viewed',
  configurator: 'configurator',
} as const;
