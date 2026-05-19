import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useLocalStorage } from '@/hooks/useLocalStorage';

describe('useLocalStorage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    localStorage.clear();
  });

  describe('initialState', () => {
    it('должен использовать initialValue если localStorage пуст', () => {
      const { result } = renderHook(() => useLocalStorage('test', 'default'));
      
      expect(result.current[0]).toBe('default');
    });

    it('должен читать значение из localStorage', () => {
      localStorage.setItem('test', JSON.stringify('saved'));
      
      const { result } = renderHook(() => useLocalStorage('test', 'default'));
      
      expect(result.current[0]).toBe('saved');
    });

    it('должен обрабатывать ошибку парсинга JSON', () => {
      localStorage.setItem('invalid', 'not json');
      
      const { result } = renderHook(() => useLocalStorage('invalid', 'fallback'));
      
      expect(result.current[0]).toBe('fallback');
    });
  });

  describe('setValue', () => {
    it('должен обновлять локальное состояние', () => {
      const { result } = renderHook(() => useLocalStorage('test', 'initial'));
      
      act(() => {
        result.current[1]('new value');
      });
      
      expect(result.current[0]).toBe('new value');
    });

    it('должен записывать значение в localStorage', () => {
      const { result } = renderHook(() => useLocalStorage('test', ''));
      
      act(() => {
        result.current[1]('updated');
      });
      
      expect(localStorage.getItem('test')).toBe('"updated"');
    });

    it('должен сериализовать объекты в JSON', () => {
      const config = { theme: 'dark', lang: 'ru' };
      
      const { result } = renderHook(() => useLocalStorage('config', {} as any));
      
      act(() => {
        result.current[1](config);
      });
      
      expect(localStorage.getItem('config')).toBe(JSON.stringify(config));
    });
  });

  describe('type handling', () => {
    it('должен работать с числами', () => {
      const { result } = renderHook(() => useLocalStorage('number', 0));
      
      act(() => {
        result.current[1](42);
      });
      
      expect(result.current[0]).toBe(42);
    });

    it('должен работать с boolean', () => {
      const { result } = renderHook(() => useLocalStorage('bool', false));
      
      act(() => {
        result.current[1](true);
      });
      
      expect(result.current[0]).toBe(true);
    });
  });
});
