import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

type ViewMode = '2d' | '3d';

class SimpleUIStore {
  currentStep = 0;
  totalSteps = 4;
  viewMode: ViewMode = '2d';
  isLoading = false;
  error: string | null = null;

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

  goToStep(step: number) {
    if (step >= 0 && step < this.totalSteps) {
      this.currentStep = step;
    }
  }

  nextStep() {
    if (this.currentStep < this.totalSteps - 1) {
      this.currentStep++;
    }
  }

  prevStep() {
    if (this.currentStep > 0) {
      this.currentStep--;
    }
  }

  toggleViewMode() {
    this.viewMode = this.viewMode === '2d' ? '3d' : '2d';
  }

  setViewMode(mode: ViewMode) {
    this.viewMode = mode;
  }

  reset() {
    this.currentStep = 0;
    this.viewMode = '2d';
    this.error = null;
  }

  setError(error: string | null) {
    this.error = error;
  }
}

describe('Configurator UI Store', () => {
  let uiStore: SimpleUIStore;

  beforeEach(() => {
    vi.clearAllMocks();
    uiStore = new SimpleUIStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен иметь шаг 0 по умолчанию', () => {
      expect(uiStore.currentStep).toBe(0);
    });

    it('должен иметь totalSteps = 4', () => {
      expect(uiStore.totalSteps).toBe(4);
    });

    it('должен иметь режим просмотра 2D', () => {
      expect(uiStore.viewMode).toBe('2d');
    });

    it('должен не быть в загрузке', () => {
      expect(uiStore.isLoading).toBe(false);
    });

    it('должен не иметь ошибки', () => {
      expect(uiStore.error).toBeNull();
    });
  });

  describe('step getter', () => {
    it('должен возвращать currentStep', () => {
      expect(uiStore.step).toBe(0);
    });

    it('должен обновляться при изменении currentStep', () => {
      uiStore.goToStep(2);
      expect(uiStore.step).toBe(2);
    });
  });

  describe('is3D getter', () => {
    it('должен возвращать false при 2D', () => {
      expect(uiStore.is3D).toBe(false);
    });

    it('должен возвращать true при 3D', () => {
      uiStore.setViewMode('3d');
      expect(uiStore.is3D).toBe(true);
    });
  });

  describe('isFirstStep getter', () => {
    it('должен возвращать true на первом шаге', () => {
      expect(uiStore.isFirstStep).toBe(true);
    });

    it('должен возвращать false на других шагах', () => {
      uiStore.goToStep(1);
      expect(uiStore.isFirstStep).toBe(false);
    });
  });

  describe('isLastStep getter', () => {
    it('должен возвращать false на первом шаге', () => {
      expect(uiStore.isLastStep).toBe(false);
    });

    it('должен возвращать true на последнем шаге', () => {
      uiStore.goToStep(3);
      expect(uiStore.isLastStep).toBe(true);
    });
  });

  describe('goToStep', () => {
    it('должен переходить к указанному шагу', () => {
      uiStore.goToStep(2);
      expect(uiStore.currentStep).toBe(2);
    });

    it('должен не выходить за пределы [0, totalSteps-1]', () => {
      uiStore.goToStep(-1);
      expect(uiStore.currentStep).toBe(0);
    });

    it('должен не выходить за верхнюю границу', () => {
      uiStore.goToStep(10);
      expect(uiStore.currentStep).toBe(0);
    });

    it('должен переходить к шагу 3', () => {
      uiStore.goToStep(3);
      expect(uiStore.currentStep).toBe(3);
    });
  });

  describe('nextStep', () => {
    it('должен увеличивать шаг', () => {
      uiStore.nextStep();
      expect(uiStore.currentStep).toBe(1);
    });

    it('должен не выходить за последний шаг', () => {
      uiStore.goToStep(3);
      uiStore.nextStep();
      expect(uiStore.currentStep).toBe(3);
    });

    it('должен позволять несколько переходов вперёд', () => {
      uiStore.nextStep();
      uiStore.nextStep();
      expect(uiStore.currentStep).toBe(2);
    });
  });

  describe('prevStep', () => {
    it('должен уменьшать шаг', () => {
      uiStore.goToStep(2);
      uiStore.prevStep();
      expect(uiStore.currentStep).toBe(1);
    });

    it('должен не выходить за первый шаг', () => {
      uiStore.prevStep();
      expect(uiStore.currentStep).toBe(0);
    });

    it('должен позволять несколько переходов назад', () => {
      uiStore.goToStep(3);
      uiStore.prevStep();
      uiStore.prevStep();
      expect(uiStore.currentStep).toBe(1);
    });
  });

  describe('toggleViewMode', () => {
    it('должен переключать 2D → 3D', () => {
      uiStore.toggleViewMode();
      expect(uiStore.viewMode).toBe('3d');
    });

    it('должен переключать 3D → 2D', () => {
      uiStore.setViewMode('3d');
      uiStore.toggleViewMode();
      expect(uiStore.viewMode).toBe('2d');
    });

    it('должен переключать несколько раз', () => {
      uiStore.toggleViewMode();
      uiStore.toggleViewMode();
      uiStore.toggleViewMode();
      expect(uiStore.viewMode).toBe('3d');
    });
  });

  describe('setViewMode', () => {
    it('должен устанавливать 2D', () => {
      uiStore.setViewMode('2d');
      expect(uiStore.viewMode).toBe('2d');
    });

    it('должен устанавливать 3D', () => {
      uiStore.setViewMode('3d');
      expect(uiStore.viewMode).toBe('3d');
    });
  });

  describe('reset', () => {
    it('должен сбрасывать currentStep в 0', () => {
      uiStore.goToStep(2);
      uiStore.reset();
      expect(uiStore.currentStep).toBe(0);
    });

    it('должен сбрасывать viewMode в 2D', () => {
      uiStore.setViewMode('3d');
      uiStore.reset();
      expect(uiStore.viewMode).toBe('2d');
    });

    it('должен сбрасывать ошибку', () => {
      uiStore.error = 'Test error';
      uiStore.reset();
      expect(uiStore.error).toBeNull();
    });
  });

  describe('setError', () => {
    it('должен устанавливать ошибку', () => {
      uiStore.setError('Connection failed');
      expect(uiStore.error).toBe('Connection failed');
    });

    it('должен устанавливать null для очистки', () => {
      uiStore.error = 'Some error';
      uiStore.setError(null);
      expect(uiStore.error).toBeNull();
    });
  });

  describe('navigation', () => {
    it('должен позволять навигацию вперёд и назад', () => {
      uiStore.nextStep();
      uiStore.nextStep();
      uiStore.prevStep();
      uiStore.goToStep(3);
      expect(uiStore.currentStep).toBe(3);
    });

    it('должен обновлять isFirstStep и isLastStep', () => {
      expect(uiStore.isFirstStep).toBe(true);
      expect(uiStore.isLastStep).toBe(false);
      uiStore.nextStep();
      expect(uiStore.isFirstStep).toBe(false);
      expect(uiStore.isLastStep).toBe(false);
      uiStore.goToStep(3);
      expect(uiStore.isFirstStep).toBe(false);
      expect(uiStore.isLastStep).toBe(true);
    });
  });
});
