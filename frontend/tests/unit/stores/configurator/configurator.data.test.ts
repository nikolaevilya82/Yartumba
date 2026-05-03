import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

type FurnitureType = 'bookshelf' | 'nightstand' | 'dresser';

interface FurnitureConfiguration {
  width: number;
  height: number;
  depth: number;
  shelves?: number;
  drawers?: number;
  material?: any;
  edgeMaterial?: any;
  backPanel?: string;
  legs?: string;
}

interface ConfiguratorOptions {
  materials: any[];
  edgeMaterials: any[];
  slideGuides: any[];
  hinges: any[];
  supports: any[];
  wallMounts: any[];
}

const DEFAULT_CONFIG: Record<FurnitureType, FurnitureConfiguration> = {
  bookshelf: {
    width: 800,
    height: 2000,
    depth: 350,
    shelves: 5,
    material: null,
    edgeMaterial: null,
    backPanel: 'hdf',
    legs: null,
  },
  nightstand: {
    width: 500,
    height: 600,
    depth: 400,
    shelves: 1,
    material: null,
    edgeMaterial: null,
    backPanel: 'hdf',
    legs: 'wooden',
  },
  dresser: {
    width: 800,
    height: 900,
    depth: 450,
    drawers: 4,
    material: null,
    edgeMaterial: null,
    backPanel: 'hdf',
    legs: 'wooden',
  },
};

class SimpleConfiguratorDataStore {
  furnitureType: FurnitureType = 'bookshelf';
  configuration: FurnitureConfiguration = { ...DEFAULT_CONFIG.bookshelf };
  options: ConfiguratorOptions | null = null;

  get currentConfig(): FurnitureConfiguration {
    return this.configuration;
  }

  get type(): FurnitureType {
    return this.furnitureType;
  }

  setFurnitureType(type: FurnitureType) {
    this.furnitureType = type;
    this.configuration = { ...DEFAULT_CONFIG[type] };
  }

  updateConfiguration(partial: Partial<FurnitureConfiguration>) {
    this.configuration = { ...this.configuration, ...partial };
  }

  setValue<K extends keyof FurnitureConfiguration>(key: K, value: FurnitureConfiguration[K]) {
    this.configuration = { ...this.configuration, [key]: value };
  }

  setOptions(options: ConfiguratorOptions) {
    this.options = options;
  }

  reset() {
    this.configuration = { ...DEFAULT_CONFIG[this.furnitureType] };
  }

  loadConfiguration(config: FurnitureConfiguration, type: FurnitureType) {
    this.furnitureType = type;
    this.configuration = { ...config };
  }
}

describe('Configurator Data Store', () => {
  let dataStore: SimpleConfiguratorDataStore;

  beforeEach(() => {
    vi.clearAllMocks();
    dataStore = new SimpleConfiguratorDataStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь bookshelf тип мебели по умолчанию', () => {
      expect(dataStore.furnitureType).toBe('bookshelf');
    });

    it('должен иметь дефолтную конфигурацию для bookshelf', () => {
      expect(dataStore.configuration.width).toBe(800);
      expect(dataStore.configuration.height).toBe(2000);
      expect(dataStore.configuration.depth).toBe(350);
    });

    it('должен иметь null опции по умолчанию', () => {
      expect(dataStore.options).toBeNull();
    });
  });

  describe('currentConfig getter', () => {
    it('должен возвращать текущую конфигурацию', () => {
      const config = dataStore.currentConfig;
      
      expect(config.width).toBe(800);
      expect(config.height).toBe(2000);
    });
  });

  describe('type getter', () => {
    it('должен возвращать текущий тип мебели', () => {
      expect(dataStore.type).toBe('bookshelf');
    });
  });

  describe('setFurnitureType', () => {
    it('должен устанавливать тип furniture', () => {
      dataStore.setFurnitureType('nightstand');
      
      expect(dataStore.furnitureType).toBe('nightstand');
    });

    it('должен сбрасывать конфигурацию для нового типа', () => {
      dataStore.setFurnitureType('nightstand');
      
      expect(dataStore.configuration.width).toBe(500);
      expect(dataStore.configuration.height).toBe(600);
    });

    it('должен устанавливать конфигурацию dresser', () => {
      dataStore.setFurnitureType('dresser');
      
      expect(dataStore.configuration.width).toBe(800);
      expect(dataStore.configuration.height).toBe(900);
    });
  });

  describe('updateConfiguration', () => {
    it('должен обновлять частичную конфигурацию', () => {
      dataStore.updateConfiguration({ width: 1200, height: 2200 });
      
      expect(dataStore.configuration.width).toBe(1200);
      expect(dataStore.configuration.height).toBe(2200);
      expect(dataStore.configuration.depth).toBe(350);
    });

    it('должен обновлять несколько полей', () => {
      dataStore.updateConfiguration({ 
        width: 1000, 
        depth: 400,
        shelves: 10 
      });
      
      expect(dataStore.configuration.width).toBe(1000);
      expect(dataStore.configuration.depth).toBe(400);
      expect(dataStore.configuration.shelves).toBe(10);
    });

    it('должен сохранять неизменённые поля', () => {
      const originalDepth = dataStore.configuration.depth;
      
      dataStore.updateConfiguration({ width: 1000 });
      
      expect(dataStore.configuration.depth).toBe(originalDepth);
    });
  });

  describe('setValue', () => {
    it('должен устанавливать конкретное значение', () => {
      dataStore.setValue('width', 1500);
      
      expect(dataStore.configuration.width).toBe(1500);
    });

    it('должен устанавливать shelves', () => {
      dataStore.setValue('shelves', 8);
      
      expect(dataStore.configuration.shelves).toBe(8);
    });

    it('должен устанавливать backPanel', () => {
      dataStore.setValue('backPanel', 'hdf');
      
      expect(dataStore.configuration.backPanel).toBe('hdf');
    });
  });

  describe('setOptions', () => {
    it('должен загружать опции', () => {
      const mockOptions = {
        materials: [{ id: 1, name: 'Test Material' }],
        edgeMaterials: [{ id: 1, name: 'Test Edge' }],
        slideGuides: [{ id: 1, name: 'Test Guide' }],
        hinges: [{ id: 1, name: 'Test Hinge' }],
        supports: [{ id: 1, name: 'Test Support' }],
        wallMounts: [{ id: 1, name: 'Test Mount' }],
      };
      
      dataStore.setOptions(mockOptions as any);
      
      expect(dataStore.options).toEqual(mockOptions);
    });
  });

  describe('reset', () => {
    it('должен сбрасывать конфигурацию к дефолтной', () => {
      dataStore.updateConfiguration({ width: 1500, height: 2500 });
      
      dataStore.reset();
      
      expect(dataStore.configuration.width).toBe(800);
      expect(dataStore.configuration.height).toBe(2000);
    });

    it('должен сбрасывать для текущего типа мебели', () => {
      dataStore.setFurnitureType('nightstand');
      dataStore.updateConfiguration({ width: 1000 });
      
      dataStore.reset();
      
      expect(dataStore.configuration.width).toBe(500);
    });
  });

  describe('loadConfiguration', () => {
    it('должен загружать сохранённую конфигурацию', () => {
      const savedConfig: FurnitureConfiguration = {
        width: 1200,
        height: 2400,
        depth: 400,
        shelves: 6,
        material: null,
        edgeMaterial: null,
        backPanel: 'hdf',
        legs: null,
      };
      
      dataStore.loadConfiguration(savedConfig, 'bookshelf');
      
      expect(dataStore.configuration.width).toBe(1200);
      expect(dataStore.configuration.height).toBe(2400);
    });

    it('должен устанавливать тип мебели', () => {
      const savedConfig: FurnitureConfiguration = {
        width: 500,
        height: 600,
        depth: 400,
        shelves: 1,
        material: null,
        edgeMaterial: null,
        backPanel: 'hdf',
        legs: null,
      };
      
      dataStore.loadConfiguration(savedConfig, 'nightstand');
      
      expect(dataStore.furnitureType).toBe('nightstand');
    });
  });
});

