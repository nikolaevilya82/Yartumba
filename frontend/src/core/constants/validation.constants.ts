// Ограничения для валидации размеров (в мм)
export const sizeLimits = {
  bookshelf: {
    width: { min: 400, max: 2000 },
    height: { min: 400, max: 2400 },
    depth: { min: 200, max: 600 },
  },
  nightstand: {
    width: { min: 300, max: 800 },
    height: { min: 300, max: 800 },
    depth: { min: 300, max: 600 },
  },
  dresser: {
    width: { min: 600, max: 1600 },
    height: { min: 600, max: 1200 },
    depth: { min: 400, max: 700 },
  },
} as const;

// Ограничения для количества полок/ящиков
export const countLimits = {
  shelf: { min: 1, max: 10 },
  drawer: { min: 1, max: 6 },
} as const;

// Ограничения для текстовых полей
export const textLimits = {
  name: { min: 1, max: 100 },
  description: { min: 0, max: 1000 },
  article: { min: 1, max: 50 },
} as const;

// Ограничения для цен
export const priceLimits = {
  min: 0,
  max: 1_000_000,
  decimals: 2,
} as const;

// Регулярные выражения для валидации
export const validationPatterns = {
  article: /^[A-Za-z0-9\-_]+$/,
  phone: /^\+?[0-9\s\-()]+$/,
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  url: /^https?:\/\/.+/,
} as const;

// Сообщения об ошибках валидации
export const validationMessages = {
  required: 'Это поле обязательно',
  minLength: (min: number) => `Минимум ${min} символов`,
  maxLength: (max: number) => `Максимум ${max} символов`,
  minValue: (min: number) => `Минимальное значение: ${min}`,
  maxValue: (max: number) => `Максимальное значение: ${max}`,
  invalidFormat: 'Неверный формат',
  invalidArticle: 'Артикул может содержать только латинские буквы, цифры, дефис и подчёркивание',
  invalidPhone: 'Введите корректный номер телефона',
  invalidEmail: 'Введите корректный email',
  invalidUrl: 'Введите корректный URL',
  notInteger: 'Введите целое число',
  notMultipleOf: (step: number) => `Значение должно быть кратно ${step}`,
} as const;

// Шаг размеров
export const sizeStep = 50;
