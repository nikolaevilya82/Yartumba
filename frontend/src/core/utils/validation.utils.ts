import { validationPatterns, validationMessages, textLimits } from '../constants/validation.constants';

/**
 * Проверка на пустоту
 */
export function isRequired(value: unknown): boolean {
  if (typeof value === 'string') return value.trim().length > 0;
  if (typeof value === 'number') return !isNaN(value);
  if (Array.isArray(value)) return value.length > 0;
  return value !== null && value !== undefined;
}

/**
 * Валидация минимальной длины строки
 */
export function minLength(value: string, min: number): boolean {
  return value.length >= min;
}

/**
 * Валидация максимальной длины строки
 */
export function maxLength(value: string, max: number): boolean {
  return value.length <= max;
}

/**
 * Валидация длины строки
 */
export function lengthRange(value: string, min: number, max: number): boolean {
  return minLength(value, min) && maxLength(value, max);
}

/**
 * Валидация минимального значения
 */
export function minValue(value: number, min: number): boolean {
  return value >= min;
}

/**
 * Валидация максимального значения
 */
export function maxValue(value: number, max: number): boolean {
  return value <= max;
}

/**
 * Валидация диапазона
 */
export function valueRange(value: number, min: number, max: number): boolean {
  return minValue(value, min) && maxValue(value, max);
}

/**
 * Валидация email
 */
export function isValidEmail(email: string): boolean {
  return validationPatterns.email.test(email);
}

/**
 * Валидация телефона
 */
export function isValidPhone(phone: string): boolean {
  return validationPatterns.phone.test(phone);
}

/**
 * Валидация артикула
 */
export function isValidArticle(article: string): boolean {
  return validationPatterns.article.test(article);
}

/**
 * Валидация URL
 */
export function isValidUrl(url: string): boolean {
  return validationPatterns.url.test(url);
}

/**
 * Проверка на целое число
 */
export function isInteger(value: number): boolean {
  return Number.isInteger(value);
}

/**
 * Проверка на кратность
 */
export function isMultipleOf(value: number, step: number): boolean {
  return value % step === 0;
}

/**
 * Результат валидации поля
 */
export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * Валидация поля с универсальным типом
 */
export type Validator = (value: unknown) => ValidationResult;

/**
 * Создание валидатора с кастомным сообщением
 */
export function createValidator(validate: (value: unknown) => boolean, message: string): Validator {
  return (value: unknown) => ({
    isValid: validate(value),
    error: message,
  });
}

/**
 * Комбинирование нескольких валидаторов
 */
export function combineValidators(...validators: Validator[]): Validator {
  return (value: unknown) => {
    for (const validator of validators) {
      const result = validator(value);
      if (!result.isValid) {
        return result;
      }
    }
    return { isValid: true };
  };
}

/**
 * Валидация обязательного поля
 */
export const required = createValidator(isRequired, validationMessages.required);

/**
 * Валидация email
 */
export const email = createValidator(
  (v) => typeof v === 'string' && isValidEmail(v),
  validationMessages.invalidEmail
);

/**
 * Валидация телефона
 */
export const phone = createValidator(
  (v) => typeof v === 'string' && isValidPhone(v),
  validationMessages.invalidPhone
);

/**
 * Валидация имени (мин. длина)
 */
export const nameMinLength = (min: number = textLimits.name.min) =>
  createValidator(
    (v) => typeof v === 'string' && minLength(v, min),
    validationMessages.minLength(min)
  );

/**
 * Валидация описания (макс. длина)
 */
export const descriptionMaxLength = (max: number = textLimits.description.max) =>
  createValidator(
    (v) => typeof v === 'string' && maxLength(v, max),
    validationMessages.maxLength(max)
  );
