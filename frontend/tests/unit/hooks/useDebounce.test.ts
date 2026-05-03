import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from '@/hooks/useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.clearAllMocks();
  });

  it('должен возвращать начальное значение сразу', () => {
    const { result } = renderHook(() => useDebounce('initial', 300));
    
    expect(result.current).toBe('initial');
  });

  it('должен не менять значение сразу при изменении пропса', () => {
    const { result, rerender } = renderHook(({ value }) => useDebounce(value, 300), {
      initialProps: { value: 'old' }
    });
    
    rerender({ value: 'new' });
    
    expect(result.current).toBe('old');
  });

  it('должен обновить значение после задержки', () => {
    const { result, rerender } = renderHook(({ value }) => useDebounce(value, 300), {
      initialProps: { value: 'old' }
    });
    
    rerender({ value: 'new' });
    
    act(() => {
      vi.advanceTimersByTime(300);
    });
    
    expect(result.current).toBe('new');
  });

  it('должен сбрасывать таймер при изменении значения', () => {
    const { result, rerender } = renderHook(({ value }) => useDebounce(value, 300), {
      initialProps: { value: 'first' }
    });
    
    rerender({ value: 'second' });
    
    act(() => {
      vi.advanceTimersByTime(150);
    });
    
    rerender({ value: 'third' });
    
    act(() => {
      vi.advanceTimersByTime(150);
    });
    
    expect(result.current).toBe('first');
    
    act(() => {
      vi.advanceTimersByTime(300);
    });
    
    expect(result.current).toBe('third');
  });

  it('должен очищать таймер при размонтировании', () => {
    const clearTimeoutSpy = vi.spyOn(global, 'clearTimeout');
    
    const { unmount } = renderHook(() => useDebounce('test', 300));
    
    act(() => {
      vi.advanceTimersByTime(100);
    });
    
    unmount();
    
    expect(clearTimeoutSpy).toHaveBeenCalled();
  });
});
