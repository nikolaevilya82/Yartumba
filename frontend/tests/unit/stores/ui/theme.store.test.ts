import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Моки localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value;
    }),
    clear: vi.fn(() => {
      store = {};
    }),
    removeItem: vi.fn((key: string) => {
      delete store[key];
    }),
  };
})();

// Моки document
const documentMock = {
  documentElement: {
    classList: {
      toggle: vi.fn(),
    },
  },
};

// Создаём простой store для тестирования
class SimpleThemeStore {
  theme: 'light' | 'dark' | 'system' = 'system';

  setTheme(theme: 'light' | 'dark' | 'system') {
    this.theme = theme;
    localStorageMock.setItem('theme', theme);
  }

  toggle() {
    const themes: ('light' | 'dark' | 'system')[] = ['light', 'dark', 'system'];
    const currentIndex = themes.indexOf(this.theme);
    const nextIndex = (currentIndex + 1) % themes.length;
    this.setTheme(themes[nextIndex]);
  }

  get currentTheme(): string {
    if (this.theme === 'system') {
      return (window as any).matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return this.theme;
  }
}

describe('Theme Store', () => {
  let themeStore: SimpleThemeStore;

  beforeEach(() => {
    vi.clearAllMocks();
    localStorageMock.clear();
    (global.localStorage as unknown) = localStorageMock;
    (global.document as unknown) = documentMock;
    
    themeStore = new SimpleThemeStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь дефолтную тему system', () => {
      expect(themeStore.theme).toBe('system');
    });
  });

  describe('setTheme', () => {
    it('должен устанавливать light тему', () => {
      themeStore.setTheme('light');
      
      expect(themeStore.theme).toBe('light');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'light');
    });

    it('должен устанавливать dark тему', () => {
      themeStore.setTheme('dark');
      
      expect(themeStore.theme).toBe('dark');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'dark');
    });

    it('должен устанавливать system тему', () => {
      themeStore.setTheme('system');
      
      expect(themeStore.theme).toBe('system');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'system');
    });
  });

  describe('currentTheme', () => {
    it('должен возвращать light при system и светлой системе', () => {
      Object.defineProperty(window, 'matchMedia', {
        writable: true,
        value: vi.fn().mockImplementation(() => ({
          matches: false,
        })),
      });
      
      themeStore.setTheme('system');
      expect(themeStore.currentTheme).toBe('light');
    });

    it('должен возвращать dark при system и тёмной системе', () => {
      Object.defineProperty(window, 'matchMedia', {
        writable: true,
        value: vi.fn().mockImplementation(() => ({
          matches: true,
        })),
      });
      
      themeStore.setTheme('system');
      expect(themeStore.currentTheme).toBe('dark');
    });

    it('должен возвращать установленную тему при light', () => {
      themeStore.setTheme('light');
      expect(themeStore.currentTheme).toBe('light');
    });

    it('должен возвращать установленную тему при dark', () => {
      themeStore.setTheme('dark');
      expect(themeStore.currentTheme).toBe('dark');
    });
  });

  describe('toggle', () => {
    it('должен переключать system → light → dark → system', () => {
      themeStore.setTheme('system');
      themeStore.toggle();
      expect(themeStore.theme).toBe('light');
      
      themeStore.toggle();
      expect(themeStore.theme).toBe('dark');
      
      themeStore.toggle();
      expect(themeStore.theme).toBe('system');
    });

    it('должен переключать light → dark → system → light', () => {
      themeStore.setTheme('light');
      themeStore.toggle();
      expect(themeStore.theme).toBe('dark');
      
      themeStore.toggle();
      expect(themeStore.theme).toBe('system');
      
      themeStore.toggle();
      expect(themeStore.theme).toBe('light');
    });
  });
});

