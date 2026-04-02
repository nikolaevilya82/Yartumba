import { makeAutoObservable } from 'mobx';
import type { FurnitureType } from '../../core/constants/product.constants';
import type { FurnitureConfiguration, ConfiguratorOptions } from '../../core/types/configurator.types';

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
    legs: 'wooden',
  },
  dresser: {
    width: 800,
    height: 900,
    depth: 450,
    drawers: 4,
    material: null,
    edgeMaterial: null,
    legs: 'wooden',
  },
};

class ConfiguratorDataStore {
  furnitureType: FurnitureType = 'bookshelf';
  configuration: FurnitureConfiguration = DEFAULT_CONFIG.bookshelf;
  options: ConfiguratorOptions | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  // Геттеры
  get currentConfig(): FurnitureConfiguration {
    return this.configuration;
  }

  get type(): FurnitureType {
    return this.furnitureType;
  }

  // Установить тип мебели
  setFurnitureType(type: FurnitureType) {
    this.furnitureType = type;
    this.configuration = { ...DEFAULT_CONFIG[type] };
  }

  // Обновить конфигурацию
  updateConfiguration(partial: Partial<FurnitureConfiguration>) {
    this.configuration = { ...this.configuration, ...partial };
  }

  // Установить конкретное значение
  setValue<K extends keyof FurnitureConfiguration>(key: K, value: FurnitureConfiguration[K]) {
    this.configuration = { ...this.configuration, [key]: value };
  }

  // Загрузить опции
  setOptions(options: ConfiguratorOptions) {
    this.options = options;
  }

  // Сбросить конфигурацию
  reset() {
    this.configuration = { ...DEFAULT_CONFIG[this.furnitureType] };
  }

  // Загрузить сохранённую конфигурацию
  loadConfiguration(config: FurnitureConfiguration, type: FurnitureType) {
    this.furnitureType = type;
    this.configuration = { ...config };
  }
}

export const configuratorDataStore = new ConfiguratorDataStore();
export default configuratorDataStore;
