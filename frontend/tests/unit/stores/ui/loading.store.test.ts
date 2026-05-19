import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

class SimpleLoadingStore {
  isPageLoading = false;
  isGlobalLoading = false;
  loadingMessage = '';

  setPageLoading(loading: boolean, message = '') {
    this.isPageLoading = loading;
    this.loadingMessage = message;
  }

  setGlobalLoading(loading: boolean, message = '') {
    this.isGlobalLoading = loading;
    this.loadingMessage = message;
  }

  show(message = 'Загрузка...') {
    this.isGlobalLoading = true;
    this.loadingMessage = message;
  }

  hide() {
    this.isGlobalLoading = false;
    this.loadingMessage = '';
  }

  showPage(message = '') {
    this.isPageLoading = true;
    this.loadingMessage = message;
  }

  hidePage() {
    this.isPageLoading = false;
    this.loadingMessage = '';
  }
}

describe('Loading Store', () => {
  let loadingStore: SimpleLoadingStore;

  beforeEach(() => {
    vi.clearAllMocks();
    loadingStore = new SimpleLoadingStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен быть не загрузочным по умолчанию', () => {
      expect(loadingStore.isPageLoading).toBe(false);
      expect(loadingStore.isGlobalLoading).toBe(false);
    });

    it('должен иметь пустое сообщение по умолчанию', () => {
      expect(loadingStore.loadingMessage).toBe('');
    });
  });

  describe('setPageLoading', () => {
    it('должен устанавливать страницу в загрузку', () => {
      loadingStore.setPageLoading(true);
      
      expect(loadingStore.isPageLoading).toBe(true);
    });

    it('должен устанавливать сообщение', () => {
      loadingStore.setPageLoading(true, 'Загрузка страницы...');
      
      expect(loadingStore.loadingMessage).toBe('Загрузка страницы...');
    });

    it('должен снимать страницу с загрузки', () => {
      loadingStore.setPageLoading(true);
      loadingStore.setPageLoading(false);
      
      expect(loadingStore.isPageLoading).toBe(false);
    });
  });

  describe('setGlobalLoading', () => {
    it('должен устанавливать глобальную загрузку', () => {
      loadingStore.setGlobalLoading(true);
      
      expect(loadingStore.isGlobalLoading).toBe(true);
    });

    it('должен устанавливать сообщение', () => {
      loadingStore.setGlobalLoading(true, 'Общая загрузка...');
      
      expect(loadingStore.loadingMessage).toBe('Общая загрузка...');
    });

    it('должен снимать глобальную загрузку', () => {
      loadingStore.setGlobalLoading(true);
      loadingStore.setGlobalLoading(false);
      
      expect(loadingStore.isGlobalLoading).toBe(false);
    });
  });

  describe('show', () => {
    it('должен показывать глобальную загрузку', () => {
      loadingStore.show();
      
      expect(loadingStore.isGlobalLoading).toBe(true);
    });

    it('должен использовать дефолтное сообщение', () => {
      loadingStore.show();
      
      expect(loadingStore.loadingMessage).toBe('Загрузка...');
    });

    it('должен использовать кастомное сообщение', () => {
      loadingStore.show('Пожалуйста, подождите');
      
      expect(loadingStore.loadingMessage).toBe('Пожалуйста, подождите');
    });
  });

  describe('hide', () => {
    it('должен скрывать глобальную загрузку', () => {
      loadingStore.show();
      expect(loadingStore.isGlobalLoading).toBe(true);
      
      loadingStore.hide();
      expect(loadingStore.isGlobalLoading).toBe(false);
    });

    it('должен очищать сообщение', () => {
      loadingStore.show('Test message');
      loadingStore.hide();
      
      expect(loadingStore.loadingMessage).toBe('');
    });
  });

  describe('showPage', () => {
    it('должен показывать загрузку страницы', () => {
      loadingStore.showPage();
      
      expect(loadingStore.isPageLoading).toBe(true);
    });

    it('должен использовать кастомное сообщение', () => {
      loadingStore.showPage('Загрузка данных...');
      
      expect(loadingStore.loadingMessage).toBe('Загрузка данных...');
    });
  });

  describe('hidePage', () => {
    it('должен скрывать загрузку страницы', () => {
      loadingStore.showPage();
      expect(loadingStore.isPageLoading).toBe(true);
      
      loadingStore.hidePage();
      expect(loadingStore.isPageLoading).toBe(false);
    });

    it('должен очищать сообщение', () => {
      loadingStore.showPage('Test');
      loadingStore.hidePage();
      
      expect(loadingStore.loadingMessage).toBe('');
    });
  });

  describe('parallel loading', () => {
    it('должен позволять несколько параллельных загрузок', () => {
      loadingStore.showPage('Page loading');
      loadingStore.show('Global loading');
      
      expect(loadingStore.isPageLoading).toBe(true);
      expect(loadingStore.isGlobalLoading).toBe(true);
    });

    it('должен сохранять независимость page и global loading', () => {
      loadingStore.show('Global');
      expect(loadingStore.isPageLoading).toBe(false);
      
      loadingStore.showPage('Page');
      expect(loadingStore.isGlobalLoading).toBe(true);
      
      loadingStore.hide();
      expect(loadingStore.isPageLoading).toBe(true);
      expect(loadingStore.isGlobalLoading).toBe(false);
    });
  });
});
