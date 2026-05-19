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

class SimpleLanguageStore {
  language: 'ru' | 'en' = 'ru';

  setLanguage(lang: 'ru' | 'en') {
    this.language = lang;
    localStorageMock.setItem('language', lang);
  }

  toggle() {
    this.language = this.language === 'ru' ? 'en' : 'ru';
    localStorageMock.setItem('language', this.language);
  }
}

describe('Language Store', () => {
  let languageStore: SimpleLanguageStore;

  beforeEach(() => {
    vi.clearAllMocks();
    localStorageMock.clear();
    (global.localStorage as unknown) = localStorageMock;
    
    languageStore = new SimpleLanguageStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь дефолтный язык ru', () => {
      expect(languageStore.language).toBe('ru');
    });
  });

  describe('setLanguage', () => {
    it('должен устанавливать русский язык', () => {
      languageStore.setLanguage('ru');
      
      expect(languageStore.language).toBe('ru');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('language', 'ru');
    });

    it('должен устанавливать английский язык', () => {
      languageStore.setLanguage('en');
      
      expect(languageStore.language).toBe('en');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('language', 'en');
    });
  });

  describe('toggle', () => {
    it('должен переключать ru → en', () => {
      languageStore.setLanguage('ru');
      languageStore.toggle();
      
      expect(languageStore.language).toBe('en');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('language', 'en');
    });

    it('должен переключать en → ru', () => {
      languageStore.setLanguage('en');
      languageStore.toggle();
      
      expect(languageStore.language).toBe('ru');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('language', 'ru');
    });
  });
});
