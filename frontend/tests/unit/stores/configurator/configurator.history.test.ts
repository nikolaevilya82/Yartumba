import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

interface FurnitureConfiguration {
  width: number;
  height: number;
  depth: number;
  shelves?: number;
}

interface SavedConfiguration {
  id: number;
  name: string;
}

class SimpleDataStore {
  configuration: FurnitureConfiguration = { width: 800, height: 2000, depth: 350, shelves: 5 };
  
  updateConfiguration(partial: Partial<FurnitureConfiguration>) {
    this.configuration = { ...this.configuration, ...partial };
  }

  loadConfiguration(config: FurnitureConfiguration, type: string) {
    this.configuration = { ...config };
  }
}

class SimpleHistoryStore {
  history: FurnitureConfiguration[] = [];
  historyIndex = -1;
  savedConfigurations: SavedConfiguration[] = [];
  isSaving = false;
  isLoading = false;

  private dataStore = new SimpleDataStore();

  get canUndo(): boolean {
    return this.historyIndex > 0;
  }

  get canRedo(): boolean {
    return this.historyIndex < this.history.length - 1;
  }

  get isEmpty(): boolean {
    return this.history.length === 0;
  }

  pushToHistory(config: FurnitureConfiguration) {
    if (this.historyIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.historyIndex + 1);
    }
    this.history.push({ ...config });
    this.historyIndex = this.history.length - 1;
  }

  undo() {
    if (this.canUndo) {
      this.historyIndex--;
      this.dataStore.updateConfiguration(this.history[this.historyIndex]);
    }
  }

  redo() {
    if (this.canRedo) {
      this.historyIndex++;
      this.dataStore.updateConfiguration(this.history[this.historyIndex]);
    }
  }

  clearHistory() {
    this.history = [];
    this.historyIndex = -1;
  }

  async save(name: string) {
    this.isSaving = true;
    const mockResponse = { data: { id: 1, name } };
    this.savedConfigurations.push(mockResponse.data);
    this.isSaving = false;
    return mockResponse.data;
  }

  async loadSaved() {
    this.isLoading = true;
    const mockConfigurations: SavedConfiguration[] = [{ id: 1, name: 'Test' }];
    this.savedConfigurations = mockConfigurations;
    this.isLoading = false;
  }

  async loadConfiguration(id: number) {
    this.isLoading = true;
    const mockConfig = { configuration: { width: 1200 }, furniture_type: 'bookshelf' };
    this.dataStore.loadConfiguration(mockConfig.configuration, mockConfig.furniture_type);
    this.isLoading = false;
  }

  async deleteConfiguration(id: number) {
    this.savedConfigurations = this.savedConfigurations.filter(c => c.id !== id);
  }
}

describe('Configurator History Store', () => {
  let historyStore: SimpleHistoryStore;

  beforeEach(() => {
    vi.clearAllMocks();
    historyStore = new SimpleHistoryStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь пустую историю', () => {
      expect(historyStore.history).toEqual([]);
    });

    it('должен иметь индекс -1', () => {
      expect(historyStore.historyIndex).toBe(-1);
    });

    it('должен не иметь canUndo', () => {
      expect(historyStore.canUndo).toBe(false);
    });

    it('должен не иметь canRedo', () => {
      expect(historyStore.canRedo).toBe(false);
    });

    it('должен быть пустым', () => {
      expect(historyStore.isEmpty).toBe(true);
    });
  });

  describe('canUndo getter', () => {
    it('должен возвращать false при пустой истории', () => {
      expect(historyStore.canUndo).toBe(false);
    });

    it('должен возвращать false при первом элементе', () => {
      historyStore.pushToHistory({ width: 800, height: 2000, depth: 350, shelves: 5 });
      expect(historyStore.canUndo).toBe(false);
    });

    it('должен возвращать true при втором элементе и более', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      expect(historyStore.canUndo).toBe(true);
    });
  });

  describe('canRedo getter', () => {
    it('должен возвращать false при пустой истории', () => {
      expect(historyStore.canRedo).toBe(false);
    });

    it('должен возвращать false при последнем элементе', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.undo();
      expect(historyStore.canRedo).toBe(true);
    });
  });

  describe('pushToHistory', () => {
    it('должен добавлять конфигурацию в историю', () => {
      historyStore.pushToHistory({ width: 1200, height: 2000, depth: 350, shelves: 5 });
      expect(historyStore.history).toHaveLength(1);
      expect(historyStore.history[0].width).toBe(1200);
    });

    it('должен устанавливать индекс в последний элемент', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.pushToHistory({ width: 1200 });
      expect(historyStore.historyIndex).toBe(2);
    });

    it('должен обрезать историю вперёд при добавлении нового элемента', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.pushToHistory({ width: 1200 });
      historyStore.undo();
      historyStore.pushToHistory({ width: 1100 });
      expect(historyStore.history).toHaveLength(3);
      expect(historyStore.history[2].width).toBe(1100);
      expect(historyStore.canRedo).toBe(false);
    });
  });

  describe('undo', () => {
    it('должен отменять последнее изменение', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.undo();
      expect(historyStore.historyIndex).toBe(0);
    });

    it('должен обновлять конфигурацию данных', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.undo();
      expect(historyStore.history[0].width).toBe(800);
    });

    it('должен не делать ничего при первом элементе', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.undo();
      expect(historyStore.historyIndex).toBe(0);
    });
  });

  describe('redo', () => {
    it('должен повторять отменённое изменение', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.pushToHistory({ width: 1200 });
      historyStore.undo();
      historyStore.redo();
      expect(historyStore.historyIndex).toBe(2);
    });

    it('должен не делать ничего при последнем элементе', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.redo();
      expect(historyStore.historyIndex).toBe(1);
    });
  });

  describe('clearHistory', () => {
    it('должен очищать историю', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.clearHistory();
      expect(historyStore.history).toEqual([]);
      expect(historyStore.historyIndex).toBe(-1);
    });

    it('должен сбрасывать canUndo и canRedo', () => {
      historyStore.pushToHistory({ width: 800 });
      historyStore.pushToHistory({ width: 1000 });
      historyStore.undo();
      historyStore.clearHistory();
      expect(historyStore.canUndo).toBe(false);
      expect(historyStore.canRedo).toBe(false);
    });
  });

  describe('save', () => {
    it('должен сохранять конфигурацию', async () => {
      const result = await historyStore.save('My Configuration');
      expect(historyStore.isSaving).toBe(false);
      expect(result.id).toBe(1);
    });

    it('должен добавлять в savedConfigurations', async () => {
      await historyStore.save('Test');
      expect(historyStore.savedConfigurations).toHaveLength(1);
    });
  });

  describe('loadSaved', () => {
    it('должен загружать сохранённые конфигурации', async () => {
      await historyStore.loadSaved();
      expect(historyStore.savedConfigurations).toHaveLength(1);
      expect(historyStore.isLoading).toBe(false);
    });
  });

  describe('loadConfiguration', () => {
    it('должен загружать конфигурацию по ID', async () => {
      await historyStore.loadConfiguration(1);
      expect(historyStore.isLoading).toBe(false);
    });
  });

  describe('deleteConfiguration', () => {
    it('должен удалять сохранённую конфигурацию', async () => {
      historyStore.savedConfigurations = [
        { id: 1, name: 'Config 1' },
        { id: 2, name: 'Config 2' },
      ];
      await historyStore.deleteConfiguration(1);
      expect(historyStore.savedConfigurations).toHaveLength(1);
      expect(historyStore.savedConfigurations[0].id).toBe(2);
    });
  });
});

