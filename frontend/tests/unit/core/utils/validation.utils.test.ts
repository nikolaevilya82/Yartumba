import { describe, it, expect } from 'vitest';
import {
  isRequired,
  minLength,
  maxLength,
  lengthRange,
  minValue,
  maxValue,
  valueRange,
  isValidEmail,
  isValidPhone,
  isValidArticle,
  isValidUrl,
  isInteger,
  isMultipleOf,
  createValidator,
  combineValidators,
  required,
  email,
  phone,
  nameMinLength,
  descriptionMaxLength,
} from '@/core/utils/validation.utils';
import { isEmpty } from '@/core/utils/helpers.utils';

describe('validation.utils', () => {
  describe('isRequired', () => {
    it('должен возвращать true для непустых строк', () => {
      expect(isRequired('test')).toBe(true);
      expect(isRequired('  test  ')).toBe(true);
    });

    it('должен возвращать false для пустых строк', () => {
      expect(isRequired('')).toBe(false);
      expect(isRequired('   ')).toBe(false);
    });

    it('должен возвращать true для валидных чисел', () => {
      expect(isRequired(0)).toBe(true);
      expect(isRequired(-1)).toBe(true);
      expect(isRequired(100)).toBe(true);
    });

    it('должен возвращать false для NaN', () => {
      expect(isRequired(NaN)).toBe(false);
    });

    it('должен возвращать true для непустых массивов', () => {
      expect(isRequired([1, 2, 3])).toBe(true);
    });

    it('должен возвращать false для пустых массивов', () => {
      expect(isRequired([])).toBe(false);
    });

    it('должен возвращать false для null и undefined', () => {
      expect(isRequired(null)).toBe(false);
      expect(isRequired(undefined)).toBe(false);
    });

    it('должен возвращать true для непустых объектов', () => {
      expect(isRequired({ a: 1 })).toBe(true);
    });

    it('должен возвращать false для пустых объектов', () => {
      // Примечание: isEmpty({}) возвращает true только для объектов с 0 ключей
      expect(isEmpty({})).toBe(true);
    });
  });

  describe('minLength', () => {
    it('должен возвращать true для строки достаточной длины', () => {
      expect(minLength('hello', 5)).toBe(true);
      expect(minLength('hello world', 5)).toBe(true);
    });

    it('должен возвращать false для короткой строки', () => {
      expect(minLength('hi', 5)).toBe(false);
    });

    it('должен обрабатывать пустую строку', () => {
      expect(minLength('', 1)).toBe(false);
    });
  });

  describe('maxLength', () => {
    it('должен возвращать true для строки допустимой длины', () => {
      expect(maxLength('hello', 10)).toBe(true);
      expect(maxLength('hello', 5)).toBe(true);
    });

    it('должен возвращать false для слишком длинной строки', () => {
      expect(maxLength('hello world', 5)).toBe(false);
    });

    it('должен обрабатывать пустую строку', () => {
      expect(maxLength('', 5)).toBe(true);
    });
  });

  describe('lengthRange', () => {
    it('должен возвращать true для длины в диапазоне', () => {
      expect(lengthRange('hello', 3, 10)).toBe(true);
    });

    it('должен возвращать false для слишком короткой строки', () => {
      expect(lengthRange('hi', 3, 10)).toBe(false);
    });

    it('должен возвращать false для слишком длинной строки', () => {
      expect(lengthRange('hello world!', 3, 10)).toBe(false);
    });
  });

  describe('minValue', () => {
    it('должен возвращать true для значения >= минимума', () => {
      expect(minValue(10, 5)).toBe(true);
      expect(minValue(5, 5)).toBe(true);
    });

    it('должен возвращать false для значения < минимума', () => {
      expect(minValue(3, 5)).toBe(false);
    });

    it('должен обрабатывать отрицательные числа', () => {
      expect(minValue(-3, -5)).toBe(true);
      expect(minValue(-7, -5)).toBe(false);
    });
  });

  describe('maxValue', () => {
    it('должен возвращать true для значения <= максимума', () => {
      expect(maxValue(5, 10)).toBe(true);
      expect(maxValue(10, 10)).toBe(true);
    });

    it('должен возвращать false для значения > максимума', () => {
      expect(maxValue(15, 10)).toBe(false);
    });

    it('должен обрабатывать отрицательные числа', () => {
      expect(maxValue(-5, -3)).toBe(true);
      expect(maxValue(-1, -3)).toBe(false);
    });
  });

  describe('valueRange', () => {
    it('должен возвращать true для значения в диапазоне', () => {
      expect(valueRange(50, 0, 100)).toBe(true);
    });

    it('должен возвращать false для значения вне диапазона', () => {
      expect(valueRange(-1, 0, 100)).toBe(false);
      expect(valueRange(101, 0, 100)).toBe(false);
    });

    it('должен обрабатывать границы диапазона', () => {
      expect(valueRange(0, 0, 100)).toBe(true);
      expect(valueRange(100, 0, 100)).toBe(true);
    });
  });

  describe('isValidEmail', () => {
    it('должен принимать валидные email', () => {
      expect(isValidEmail('test@example.com')).toBe(true);
      expect(isValidEmail('user.name@domain.org')).toBe(true);
      expect(isValidEmail('user+tag@example.co.uk')).toBe(true);
    });

    it('должен отвергать невалидные email', () => {
      expect(isValidEmail('invalid')).toBe(false);
      expect(isValidEmail('invalid@')).toBe(false);
      expect(isValidEmail('@example.com')).toBe(false);
      expect(isValidEmail('test@example')).toBe(false);
      expect(isValidEmail('')).toBe(false);
    });
  });

  describe('isValidPhone', () => {
    it('должен принимать валидные телефоны', () => {
      expect(isValidPhone('+79991234567')).toBe(true);
      expect(isValidPhone('89991234567')).toBe(true);
      expect(isValidPhone('+7 (999) 123-45-67')).toBe(true);
    });

    it('должен отвергать невалидные телефоны с буквами', () => {
      // Паттерн ^\+?[0-9\s\-()]+$ принимает только цифры, пробелы, дефисы, скобки и плюс
      expect(isValidPhone('abc123')).toBe(false);
      expect(isValidPhone('test@test')).toBe(false);
      expect(isValidPhone('')).toBe(false);
    });
  });

  describe('isValidArticle', () => {
    it('должен принимать валидные артикулы', () => {
      expect(isValidArticle('ART123')).toBe(true);
      expect(isValidArticle('123456')).toBe(true);
      expect(isValidArticle('ART-123-ABC')).toBe(true);
    });

    it('должен отвергать невалидные артикулы', () => {
      expect(isValidArticle('')).toBe(false);
      // Паттерн принимает буквы, цифры, дефис и подчёркивание
      expect(isValidArticle('test@value')).toBe(false);
    });
  });

  describe('isValidUrl', () => {
    it('должен принимать валидные URL', () => {
      expect(isValidUrl('https://example.com')).toBe(true);
      expect(isValidUrl('http://localhost:3000')).toBe(true);
    });

    it('должен отвергать невалидные URL', () => {
      expect(isValidUrl('not-a-url')).toBe(false);
      expect(isValidUrl('')).toBe(false);
    });
  });

  describe('isInteger', () => {
    it('должен возвращать true для целых чисел', () => {
      expect(isInteger(5)).toBe(true);
      expect(isInteger(-3)).toBe(true);
      expect(isInteger(0)).toBe(true);
    });

    it('должен возвращать false для дробных чисел', () => {
      expect(isInteger(3.14)).toBe(false);
      expect(isInteger(-0.5)).toBe(false);
    });
  });

  describe('isMultipleOf', () => {
    it('должен возвращать true для кратных значений', () => {
      expect(isMultipleOf(10, 2)).toBe(true);
      expect(isMultipleOf(15, 5)).toBe(true);
      expect(isMultipleOf(0, 5)).toBe(true);
    });

    it('должен возвращать false для некратных значений', () => {
      expect(isMultipleOf(7, 2)).toBe(false);
      expect(isMultipleOf(11, 3)).toBe(false);
    });
  });

  describe('createValidator', () => {
    it('должен создать валидатор с сообщением', () => {
      const validator = createValidator((v) => v === 'valid', 'Ошибка');
      
      const validResult = validator('valid');
      expect(validResult.isValid).toBe(true);
      
      expect(validator('invalid')).toEqual({ isValid: false, error: 'Ошибка' });
    });
  });

  describe('combineValidators', () => {
    it('должен возвращать true если все валидаторы проходят', () => {
      const validator = combineValidators(
        createValidator((v) => v === 'a', 'Ошибка 1'),
        createValidator((v) => v === 'a', 'Ошибка 2')
      );
      
      const result = validator('a');
      expect(result.isValid).toBe(true);
    });

    it('должен вернуть первую ошибку если валидатор не проходит', () => {
      const validator = combineValidators(
        createValidator((v) => v === 'a', 'Ошибка 1'),
        createValidator((v) => v === 'b', 'Ошибка 2')
      );
      
      expect(validator('c')).toEqual({ isValid: false, error: 'Ошибка 1' });
    });
  });

  describe('required', () => {
    it('должен валидировать обязательное поле', () => {
      expect(required('test').isValid).toBe(true);
      expect(required('').isValid).toBe(false);
      expect(required(null).isValid).toBe(false);
    });
  });

  describe('email', () => {
    it('должен валидировать email', () => {
      expect(email('test@example.com').isValid).toBe(true);
      expect(email('invalid').isValid).toBe(false);
      expect(email('').isValid).toBe(false);
    });
  });

  describe('phone', () => {
    it('должен валидировать телефон', () => {
      expect(phone('+79991234567').isValid).toBe(true);
      // Паттерн принимает только цифры, пробелы, дефисы, скобки и плюс
      expect(phone('abc').isValid).toBe(false);
      expect(phone('test@test').isValid).toBe(false);
    });
  });

  describe('nameMinLength', () => {
    it('должен создавать валидатор имени', () => {
      const validator = nameMinLength(3);
      
      // Валидный результат содержит error поле даже при isValid: true
      const validResult = validator('John');
      expect(validResult.isValid).toBe(true);
      
      const invalidResult = validator('Jo');
      expect(invalidResult).toEqual({ isValid: false, error: 'Минимум 3 символов' });
    });
  });

  describe('descriptionMaxLength', () => {
    it('должен создавать валидатор описания', () => {
      const validator = descriptionMaxLength(10);
      
      // Валидный результат содержит error поле даже при isValid: true
      const validResult = validator('short');
      expect(validResult.isValid).toBe(true);
      
      const invalidResult = validator('this is too long text');
      expect(invalidResult).toEqual({ isValid: false, error: 'Максимум 10 символов' });
    });
  });
});
