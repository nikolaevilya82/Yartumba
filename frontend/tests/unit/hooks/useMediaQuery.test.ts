import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useMediaQuery } from '@/hooks/useMediaQuery';

describe('useMediaQuery', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('должен возвращать false по умолчанию', () => {
    const { result } = renderHook(() => useMediaQuery('(max-width: 768px)'));
    
    expect(result.current).toBe(false);
  });

  it('должен возвращать matches из window.matchMedia', () => {
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(() => ({
        matches: true,
        media: '(max-width: 768px)',
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      })),
    });
    
    const { result } = renderHook(() => useMediaQuery('(max-width: 768px)'));
    
    expect(result.current).toBe(true);
  });

  it('должен вызывать matchMedia с правильным запросом', () => {
    const matchMediaSpy = vi.fn().mockImplementation(() => ({
      matches: false,
      media: '(min-width: 1024px)',
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }));
    
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: matchMediaSpy,
    });
    
    renderHook(() => useMediaQuery('(min-width: 1024px)'));
    
    expect(matchMediaSpy).toHaveBeenCalledWith('(min-width: 1024px)');
  });

  it('должен подписываться на изменения', () => {
    const addListener = vi.fn();
    
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(() => ({
        matches: false,
        media: '(max-width: 768px)',
        addEventListener: addListener,
        removeEventListener: vi.fn(),
      })),
    });
    
    renderHook(() => useMediaQuery('(max-width: 768px)'));
    
    expect(addListener).toHaveBeenCalledWith('change', expect.any(Function));
  });

  it('должен отписываться при размонтировании', () => {
    const removeListener = vi.fn();
    
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(() => ({
        matches: false,
        media: '(max-width: 768px)',
        addEventListener: vi.fn(),
        removeEventListener: removeListener,
      })),
    });
    
    const { unmount } = renderHook(() => useMediaQuery('(max-width: 768px)'));
    
    unmount();
    
    expect(removeListener).toHaveBeenCalledWith('change', expect.any(Function));
  });
});
