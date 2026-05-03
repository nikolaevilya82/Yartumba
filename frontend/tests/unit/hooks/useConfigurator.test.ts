import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useConfigurator } from '@/hooks/useConfigurator';

describe('useConfigurator', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('должен возвращать начальную конфигурацию', () => {
    const result = useConfigurator('bookshelf');
    
    expect(result.configuration.width).toBe(800);
    expect(result.configuration.height).toBe(2000);
    expect(result.configuration.depth).toBe(350);
  });

  it('должен возвращать тип мебели', () => {
    const result = useConfigurator('nightstand');
    
    expect(result.furnitureType).toBe('nightstand');
  });

  it('должен возвращать текущий шаг', () => {
    const result = useConfigurator();
    
    expect(result.currentStep).toBe(0);
  });

  it('должен возвращать режим просмотра 2D', () => {
    const result = useConfigurator();
    
    expect(result.viewMode).toBe('2d');
  });

  it('должен иметь функции для работы с конфигурацией', () => {
    const result = useConfigurator();
    
    expect(typeof result.updateDimensions).toBe('function');
    expect(typeof result.updateMaterial).toBe('function');
    expect(typeof result.updateHardware).toBe('function');
    expect(typeof result.calculatePrice).toBe('function');
    expect(typeof result.validate).toBe('function');
    expect(typeof result.nextStep).toBe('function');
    expect(typeof result.prevStep).toBe('function');
    expect(typeof result.reset).toBe('function');
  });

  it('должен вызывать updateDimensions без ошибок', () => {
    const result = useConfigurator();
    
    expect(() => result.updateDimensions({ width: 1200 })).not.toThrow();
  });

  it('должен вызывать updateMaterial без ошибок', () => {
    const result = useConfigurator();
    
    expect(() => result.updateMaterial('mdf')).not.toThrow();
  });

  it('должен вызывать updateHardware без ошибок', () => {
    const result = useConfigurator();
    
    expect(() => result.updateHardware({ slideGuideId: 1 })).not.toThrow();
  });

  it('должен возвращать цену из calculatePrice', () => {
    const result = useConfigurator();
    
    const price = result.calculatePrice();
    
    expect(typeof price).toBe('number');
  });

  it('должен возвращать true из validate', () => {
    const result = useConfigurator();
    
    const valid = result.validate();
    
    expect(valid).toBe(true);
  });

  it('должен вызывать nextStep без ошибок', () => {
    const result = useConfigurator();
    
    expect(() => result.nextStep()).not.toThrow();
  });

  it('должен вызывать prevStep без ошибок', () => {
    const result = useConfigurator();
    
    expect(() => result.prevStep()).not.toThrow();
  });

  it('должен вызывать reset без ошибок', () => {
    const result = useConfigurator();
    
    expect(() => result.reset()).not.toThrow();
  });
});
