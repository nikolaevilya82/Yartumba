// Типы товаров (furniture_type)
export const FurnitureType = {
  BOOKSHELF: 'bookshelf',
  NIGHTSTAND: 'nightstand',
  DRESSER: 'dresser',
} as const;

export type FurnitureType = (typeof FurnitureType)[keyof typeof FurnitureType];

// Названия типов товаров
export const furnitureTypeNames: Record<FurnitureType, string> = {
  [FurnitureType.BOOKSHELF]: 'Книжная полка',
  [FurnitureType.NIGHTSTAND]: 'Прикроватная тумба',
  [FurnitureType.DRESSER]: 'Комод',
};

// Категории товаров
export const CategorySlug = {
  BOOKSHELVES: 'bookshelves',
  NIGHTSTANDS: 'nightstands',
  DRESSERS: 'dressers',
} as const;

export const categoryNames: Record<string, string> = {
  [CategorySlug.BOOKSHELVES]: 'Книжные полки',
  [CategorySlug.NIGHTSTANDS]: 'Прикроватные тумбы',
  [CategorySlug.DRESSERS]: 'Комоды',
};

// Части изделий (part_type)
export const PartType = {
  BODY: 'body',
  SHELF: 'shelf',
  FACADE: 'facade',
  TOP: 'top',
  LEGS: 'legs',
  BACK: 'back',
  DRAWER: 'drawer',
} as const;

export type PartType = (typeof PartType)[keyof typeof PartType];

export const partTypeNames: Record<PartType, string> = {
  [PartType.BODY]: 'Корпус',
  [PartType.SHELF]: 'Полка',
  [PartType.FACADE]: 'Фасад',
  [PartType.TOP]: 'Столешница',
  [PartType.LEGS]: 'Ножки',
  [PartType.BACK]: 'Задняя стенка',
  [PartType.DRAWER]: 'Ящик',
};

// Статусы товара
export const ProductStatus = {
  DRAFT: 'draft',
  ACTIVE: 'active',
  ARCHIVED: 'archived',
} as const;

export type ProductStatus = (typeof ProductStatus)[keyof typeof ProductStatus];
