import { makeAutoObservable, runInAction } from 'mobx';
import type { FurnitureType } from '../../core/constants/product.constants';
import type { SavedConfiguration, FurnitureConfiguration } from '../../core/types/configurator.types';
import * as configuratorService from '../../api/services/configurator.service';
import { configuratorDataStore } from './configurator.data';

class ConfiguratorHistoryStore {
  history: FurnitureConfiguration[] = [];
  historyIndex = -1;
  savedConfigurations: SavedConfiguration[] = [];
  isSaving = false;
  isLoading = false;

  constructor() {
    makeAutoObservable(this);
  }

  // Геттеры
  get canUndo(): boolean {
    return this.historyIndex > 0;
  }

  get canRedo(): boolean {
    return this.historyIndex < this.history.length - 1;
  }

  get isEmpty(): boolean {
    return this.history.length === 0;
  }

  // Добавить в историю
  pushToHistory(config: FurnitureConfiguration) {
    // Обрезать историю вперёд если мы не на последнем элементе
    if (this.historyIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.historyIndex + 1);
    }
    this.history.push({ ...config });
    this.historyIndex = this.history.length - 1;
  }

  // Отменить
  undo() {
    if (this.canUndo) {
      this.historyIndex--;
      configuratorDataStore.updateConfiguration(this.history[this.historyIndex]);
    }
  }

  // Повторить
  redo() {
    if (this.canRedo) {
      this.historyIndex++;
      configuratorDataStore.updateConfiguration(this.history[this.historyIndex]);
    }
  }

  // Очистить историю
  clearHistory() {
    this.history = [];
    this.historyIndex = -1;
  }

  // Сохранить конфигурацию
  async save(name: string) {
    this.isSaving = true;
    try {
      const config = configuratorDataStore.configuration;
      const type = configuratorDataStore.furnitureType;
      const response = await configuratorService.saveConfiguration(name, type, config);
      runInAction(() => {
        this.savedConfigurations.push(response.data);
        this.isSaving = false;
      });
      return response.data;
    } catch (error) {
      runInAction(() => {
        this.isSaving = false;
      });
      throw error;
    }
  }

  // Загрузить сохранённые конфигурации
  async loadSaved() {
    this.isLoading = true;
    try {
      const response = await configuratorService.getMyConfigurations();
      runInAction(() => {
        this.savedConfigurations = response.data;
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.isLoading = false;
      });
    }
  }

  // Загрузить конкретную конфигурацию
  async loadConfiguration(id: number) {
    this.isLoading = true;
    try {
      const response = await configuratorService.getConfiguration(id);
      runInAction(() => {
        configuratorDataStore.loadConfiguration(
          response.data.configuration,
          response.data.furniture_type
        );
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.isLoading = false;
      });
    }
  }

  // Удалить сохранённую конфигурацию
  async deleteConfiguration(id: number) {
    try {
      await configuratorService.deleteConfiguration(id);
      runInAction(() => {
        this.savedConfigurations = this.savedConfigurations.filter(c => c.id !== id);
      });
    } catch (error) {
      throw error;
    }
  }
}

export const configuratorHistoryStore = new ConfiguratorHistoryStore();
export default configuratorHistoryStore;
