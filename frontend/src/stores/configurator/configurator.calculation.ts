import { makeAutoObservable, runInAction } from 'mobx';
import type { FurnitureConfiguration, CalculationResult } from '../../core/types/configurator.types';
import * as configuratorService from '../../api/services/configurator.service';
import { configuratorDataStore } from './configurator.data';

class ConfiguratorCalculationStore {
  calculation: CalculationResult | null = null;
  isCalculating = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  // Геттеры
  get price(): number {
    return this.calculation?.price ?? 0;
  }

  get materials(): CalculationResult['materials'] {
    return this.calculation?.materials ?? [];
  }

  get parts(): CalculationResult['parts'] {
    return this.calculation?.parts ?? [];
  }

  get isEmpty(): boolean {
    return this.calculation === null;
  }

  // Рассчитать конфигурацию
  async calculate(config?: FurnitureConfiguration) {
    const configuration = config ?? configuratorDataStore.configuration;
    this.isCalculating = true;
    this.error = null;

    try {
      const response = await configuratorService.calculateConfiguration(configuration);
      runInAction(() => {
        this.calculation = response.data;
        this.isCalculating = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = (error as Error).message;
        this.isCalculating = false;
      });
    }
  }

  // Очистить расчёт
  clear() {
    this.calculation = null;
    this.error = null;
  }
}

export const configuratorCalculationStore = new ConfiguratorCalculationStore();
export default configuratorCalculationStore;
