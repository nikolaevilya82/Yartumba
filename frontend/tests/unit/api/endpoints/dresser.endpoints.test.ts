import { describe, it, expect } from 'vitest';
import { dresserEndpoints } from '@/api/endpoints/products';

describe('api/endpoints/dresser', () => {
  describe('list', () => {
    it('должен возвращать правильный URL для списка комодов', () => {
      expect(dresserEndpoints.list).toBe('/v1/goods/dresser');
    });
  });

  describe('get(id)', () => {
    it('должен возвращать правильный URL для получения комода по ID', () => {
      expect(dresserEndpoints.get(1)).toBe('/v1/goods/dresser/1');
      expect(dresserEndpoints.get(123)).toBe('/v1/goods/dresser/123');
      expect(dresserEndpoints.get(9999)).toBe('/v1/goods/dresser/9999');
    });

    it('должен работать с ID 0', () => {
      expect(dresserEndpoints.get(0)).toBe('/v1/goods/dresser/0');
    });
  });

  describe('full(id)', () => {
    it('должен возвращать правильный URL для получения комода с деталями', () => {
      expect(dresserEndpoints.full(1)).toBe('/v1/goods/dresser/1/full');
      expect(dresserEndpoints.full(123)).toBe('/v1/goods/dresser/123/full');
    });
  });

  describe('create', () => {
    it('должен возвращать правильный URL для создания комода', () => {
      expect(dresserEndpoints.create).toBe('/v1/goods/dresser');
    });
  });

  describe('update(id)', () => {
    it('должен возвращать правильный URL для обновления комода', () => {
      expect(dresserEndpoints.update(1)).toBe('/v1/goods/dresser/1');
      expect(dresserEndpoints.update(123)).toBe('/v1/goods/dresser/123');
    });
  });

  describe('delete(id)', () => {
    it('должен возвращать правильный URL для удаления комода', () => {
      expect(dresserEndpoints.delete(1)).toBe('/v1/goods/dresser/1');
      expect(dresserEndpoints.delete(123)).toBe('/v1/goods/dresser/123');
    });
  });

  describe('parts(id)', () => {
    it('должен возвращать правильный URL для списка деталей комода', () => {
      expect(dresserEndpoints.parts(1)).toBe('/v1/goods/dresser/1/parts');
      expect(dresserEndpoints.parts(123)).toBe('/v1/goods/dresser/123/parts');
    });
  });

  describe('part(id, partId)', () => {
    it('должен возвращать правильный URL для детали комода по ID', () => {
      expect(dresserEndpoints.part(1, 2)).toBe('/v1/goods/dresser/1/parts/2');
      expect(dresserEndpoints.part(123, 456)).toBe('/v1/goods/dresser/123/parts/456');
      expect(dresserEndpoints.part(1, 1)).toBe('/v1/goods/dresser/1/parts/1');
    });
  });

  describe('все эндпоинты должны быть строками или функциями', () => {
    it('list должен быть строкой', () => {
      expect(typeof dresserEndpoints.list).toBe('string');
    });

    it('get должен быть функцией', () => {
      expect(typeof dresserEndpoints.get).toBe('function');
    });

    it('full должен быть функцией', () => {
      expect(typeof dresserEndpoints.full).toBe('function');
    });

    it('create должен быть строкой', () => {
      expect(typeof dresserEndpoints.create).toBe('string');
    });

    it('update должен быть функцией', () => {
      expect(typeof dresserEndpoints.update).toBe('function');
    });

    it('delete должен быть функцией', () => {
      expect(typeof dresserEndpoints.delete).toBe('function');
    });

    it('parts должен быть функцией', () => {
      expect(typeof dresserEndpoints.parts).toBe('function');
    });

    it('part должен быть функцией', () => {
      expect(typeof dresserEndpoints.part).toBe('function');
    });
  });
});
