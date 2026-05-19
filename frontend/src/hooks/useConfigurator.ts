// Заглушка для useConfigurator - будет реализована после установки MobX
export function useConfigurator(furnitureType: string = 'bookshelf') {
  return {
    configuration: { width: 800, height: 2000, depth: 350 },
    materialType: 'ldsp',
    currentStep: 0,
    viewMode: '2d' as const,
    totalPrice: 0,
    isValid: true,
    errors: [],
    furnitureType,
    updateDimensions: (_dims: any) => {},
    updateMaterial: (_type: string) => {},
    updateHardware: (_hardware: any) => {},
    calculatePrice: () => 0,
    validate: () => true,
    nextStep: () => {},
    prevStep: () => {},
    reset: () => {},
  };
}
