import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

interface SidebarConfig {
  isOpen: boolean;
  content?: any;
  position: 'left' | 'right';
  width?: number;
}

class SimpleSidebarStore {
  config: SidebarConfig = {
    isOpen: false,
    position: 'right',
    width: 400,
  };

  get isOpen(): boolean {
    return this.config.isOpen;
  }

  open(content: any, position: 'left' | 'right' = 'right', width = 400) {
    this.config = { isOpen: true, content, position, width };
  }

  close() {
    this.config.isOpen = false;
  }

  toggle() {
    this.config.isOpen = !this.config.isOpen;
  }
}

describe('Sidebar Store', () => {
  let sidebarStore: SimpleSidebarStore;

  beforeEach(() => {
    vi.clearAllMocks();
    sidebarStore = new SimpleSidebarStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен быть закрыт по умолчанию', () => {
      expect(sidebarStore.isOpen).toBe(false);
    });

    it('должен иметь позицию right по умолчанию', () => {
      expect(sidebarStore.config.position).toBe('right');
    });

    it('должен иметь ширину 400 по умолчанию', () => {
      expect(sidebarStore.config.width).toBe(400);
    });
  });

  describe('open', () => {
    it('должен открывать сайдбар', () => {
      sidebarStore.open('Test Content');
      
      expect(sidebarStore.isOpen).toBe(true);
    });

    it('должен передавать контент', () => {
      sidebarStore.open('Test Content');
      
      expect(sidebarStore.config.content).toBe('Test Content');
    });

    it('должен использовать позицию right по умолчанию', () => {
      sidebarStore.open('Content');
      
      expect(sidebarStore.config.position).toBe('right');
    });

    it('должен использовать позицию left при указании', () => {
      sidebarStore.open('Content', 'left');
      
      expect(sidebarStore.config.position).toBe('left');
    });

    it('должен использовать кастомную ширину', () => {
      sidebarStore.open('Content', 'right', 600);
      
      expect(sidebarStore.config.width).toBe(600);
    });
  });

  describe('close', () => {
    it('должен закрывать открытый сайдбар', () => {
      sidebarStore.open('Content');
      expect(sidebarStore.isOpen).toBe(true);
      
      sidebarStore.close();
      expect(sidebarStore.isOpen).toBe(false);
    });

    it('должен устанавливать isOpen в false', () => {
      sidebarStore.open('Content');
      sidebarStore.close();
      
      expect(sidebarStore.config.isOpen).toBe(false);
    });
  });

  describe('toggle', () => {
    it('должен открывать закрытый сайдбар', () => {
      expect(sidebarStore.isOpen).toBe(false);
      
      sidebarStore.toggle();
      expect(sidebarStore.isOpen).toBe(true);
    });

    it('должен закрывать открытый сайдбар', () => {
      sidebarStore.open('Content');
      expect(sidebarStore.isOpen).toBe(true);
      
      sidebarStore.toggle();
      expect(sidebarStore.isOpen).toBe(false);
    });

    it('должен переключать несколько раз', () => {
      sidebarStore.toggle(); // open
      expect(sidebarStore.isOpen).toBe(true);
      
      sidebarStore.toggle(); // close
      expect(sidebarStore.isOpen).toBe(false);
      
      sidebarStore.toggle(); // open
      expect(sidebarStore.isOpen).toBe(true);
    });
  });

  describe('config', () => {
    it('должен сохранять все параметры при открытии', () => {
      sidebarStore.open('Test', 'left', 500);
      
      expect(sidebarStore.config.position).toBe('left');
      expect(sidebarStore.config.width).toBe(500);
      expect(sidebarStore.config.isOpen).toBe(true);
    });
  });
});
