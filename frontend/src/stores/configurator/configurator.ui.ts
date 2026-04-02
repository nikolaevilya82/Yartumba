import { makeAutoObservable, runInAction } from 'mobx';
import type { FurnitureType } from '../../core/constants/product.constants';
import * as configuratorService from '../../api/services/configurator.service';
import { configuratorDataStore } from './configurator.data';

type ViewMode = '2d' | '3d';

class ConfiguratorUIStore {
  currentStep = 0;
  totalSteps = 4;
  viewMode: ViewMode = '2d';
  isLoading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  // Геттеры
  get step(): number {
    return this.currentStep;
  }

  get is3D(): boolean {
    return this.viewMode === '3d';
  }

  get isFirstStep(): boolean {
    return this.currentStep === 0;
  }

  get isLastStep(): boolean {
    return this.currentStep === this.totalSteps - 1;
  }

  // Переход к шагу
  goToStep(step: number) {
    if (step >= 0 && step < this.totalSteps) {
      this.currentStep = step;
    }
  }

  // Следующий шаг
  nextStep() {
    if (this.currentStep < this.totalSteps - 1) {
      this.currentStep++;
    }
  }

  // Предыдущий шаг
  prevStep() {
    if (this.currentStep > 0) {
      this.currentStep--;
    }
  }

  // Переключить вид (2D/3D)
  toggleViewMode() {
    this.viewMode = this.viewMode === '2d' ? '3d' : '2d';
  }

  // Установить режим просмотра
  setViewMode(mode: ViewMode) {
    this.viewMode = mode;
  }

  // Загрузить опции конфигуратора
  async loadOptions(furnitureType: FurnitureType) {
    this.isLoading = true;
    this.error = null;

    try {
      const response = await configuratorService.getConfiguratorOptions();
      runInAction(() => {
        configuratorDataStore.setFurnitureType(furnitureType);
        configuratorDataStore.setOptions(response.data);
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = (error as Error).message;
        this.isLoading = false;
      });
    }
  }

  // Сброс UI
  reset() {
    this.currentStep = 0;
    this.viewMode = '2d';
    this.error = null;
  }

  // Установить ошибку
  setError(error: string | null) {
    this.error = error;
  }
}

export const configuratorUIStore = new ConfiguratorUIStore();
export default configuratorUIStore;
