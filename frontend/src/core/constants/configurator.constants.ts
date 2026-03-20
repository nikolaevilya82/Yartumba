// Типы материалов (material_type из БД)
export const MaterialType = {
  CHIPBOARD: 'chipboard',   // ДСП
  LDSP: 'ldsp',             // ЛДСП
  MDF: 'mdf',               // МДФ
  HDF: 'hdf',               // ХДФ
  PLYWOOD: 'plywood',       // Фанера
  SOLID_WOOD: 'solid_wood', // Массив
} as const;

export type MaterialType = (typeof MaterialType)[keyof typeof MaterialType];

export const materialTypeNames: Record<MaterialType, string> = {
  [MaterialType.CHIPBOARD]: 'ДСП',
  [MaterialType.LDSP]: 'ЛДСП',
  [MaterialType.MDF]: 'МДФ',
  [MaterialType.HDF]: 'ХДФ',
  [MaterialType.PLYWOOD]: 'Фанера',
  [MaterialType.SOLID_WOOD]: 'Массив',
};

// Типы кромки
export const EdgeType = {
  ABS: 'abs',
  PVC: 'pvc',
  ACRYLIC: 'acrylic',
  VENEER: 'veneer',
} as const;

export type EdgeType = (typeof EdgeType)[keyof typeof EdgeType];

// Типы направляющих
export const SlideGuideType = {
  ROLL: 'roll',
  TELESCOPIC: 'telescopic',
  BALL_BEARING: 'ball_bearing',
} as const;

export type SlideGuideType = (typeof SlideGuideType)[keyof typeof SlideGuideType];

// Типы петель
export const HingeType = {
  FOUR_HUNDRED: '400',
  FOUR_HUNDRED_A: '400A',
  SIXTEEN_HUNDRED: '1600',
  INTERNAL: 'internal',
} as const;

export type HingeType = (typeof HingeType)[keyof typeof HingeType];

// Типы опор
export const SupportType = {
  LEGS: 'legs',
  PLINTH: 'plinth',
  WALL_MOUNTED: 'wall_mounted',
} as const;

export type SupportType = (typeof SupportType)[keyof typeof SupportType];

// Конфигурация конфигуратора по типам товаров
export const configuratorDefaults = {
  bookshelf: {
    defaultShelfCount: 3,
    minShelfCount: 1,
    maxShelfCount: 10,
    defaultWidth: 800,
    minWidth: 400,
    maxWidth: 2000,
    defaultHeight: 1200,
    minHeight: 400,
    maxHeight: 2400,
    defaultDepth: 300,
    minDepth: 200,
    maxDepth: 600,
  },
  nightstand: {
    defaultWidth: 500,
    minWidth: 300,
    maxWidth: 800,
    defaultHeight: 500,
    minHeight: 300,
    maxHeight: 800,
    defaultDepth: 400,
    minDepth: 300,
    maxDepth: 600,
    hasDrawer: true,
    maxDrawers: 3,
  },
  dresser: {
    defaultWidth: 800,
    minWidth: 600,
    maxWidth: 1600,
    defaultHeight: 800,
    minHeight: 600,
    maxHeight: 1200,
    defaultDepth: 500,
    minDepth: 400,
    maxDepth: 700,
    hasDrawer: true,
    maxDrawers: 6,
    defaultDrawerRows: 4,
  },
} as const;

// Шаг изменения размеров (мм)
export const sizeStep = 50;

// Доступные цвета для визуализации (hex)
export const materialColors = {
  white: '#FFFFFF',
  beige: '#F5F5DC',
  oak: '#C19A6B',
  walnut: '#5D432C',
  black: '#1A1A1A',
  grey: '#808080',
  wenge: '#3D2B1F',
} as const;
