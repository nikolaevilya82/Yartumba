import { useState, useEffect } from 'react';

/**
 * Хук для debounce значений
 * @param value - Значение для debounce
 * @param delay - Задержка в миллисекундах (по умолчанию 300)
 * @returns Debounced значение
 */
export function useDebounce<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}
