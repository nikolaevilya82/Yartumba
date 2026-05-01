import { describe, it, expect } from 'vitest';
import { nightstandEndpoints } from '@/api/endpoints/products';

describe('api/endpoints/nightstand', () => {
  describe('list', () => {
    it('должен возвращать правильный URL для списка тумб', () => {
      expect(nightstandEndpoints.list).toBe('/v1/goods/nightstand');
    });
  });

  describe('get(id)', () => {
    it('должен возвращать правильный URL для получения тумбы по ID', () => {
      expect(nightstandEndpoints.get(1)).toBe('/v1/goods/nightstand/1');
      expect(nightstandEndpoints.get(123)).toBe('/v1/goods/nightstand/123');
      expect(nightstandEndpoints.get(9999)).toBe('/v1/goods/nightstand/9999');
    });

    it('должен работать с ID 0', () => {
      expect(nightstandEndpoints.get(0)).toBe('/v1/goods/nightstand/0');
    });
  });

  describe('full(id)', () => {
    it('должен возвращать правильный URL для получения тумбы с деталями', () => {
      expect(nightstandEndpoints.full(1)).toBe('/v1/goods/nightstand/1/full');
      expect(nightstandEndpoints.full(123)).toBe('/v1/goods/nightstand/123/full');
    });
  });

  describe('create', () => {
    it('должен возвращать правильный URL для создания тумбы', () => {
      expect(nightstandEndpoints.create).toBe('/v1/goods/nightstand');
    });
  });

  describe('update(id)', () => {
    it('должен возвращать правильный URL для обновления тумбы', () => {
      expect(nightstandEndpoints.update(1)).toBe('/v1/goods/nightstand/1');
      expect(nightstandEndpoints.update(123)).toBe('/v1/goods/nightstand/123');
    });
  });

  describe('delete(id)', () => {
    it('должен возвращать правильный URL для удаления тумбы', () => {
      expect(nightstandEndpoints.delete(1)).toBe('/v1/goods/nightstand/1');
      expect(nightstandEndpoints.delete(123)).toBe('/v1/goods/nightstand/123');
    });
  });

  describe('parts(id)', () => {
    it('должен возвращать правильный URL для списка деталей тумбы', () => {
      expect(nightstandEndpoints.parts(1)).toBe('/v1/goods/nightstand/1/parts');
      expect(nightstandEndpoints.parts(123)).toBe('/v1/goods/nightstand/123/parts');
    });
  });

  describe('part(id, partId)', () => {
    it('должен возвращать правильный URL для детали тумбы по ID', () => {
      expect(nightstandEndpoints.part(1, 2)).toBe('/v1/goods/nightstand/1/parts/2');
      expect(nightstandEndpoints.part(123, 456)).toBe('/v1/goods/nightstand/123/parts/456');
      expect(nightstandEndpoints.part(1, 1)).toBe('/v1/goods/nightstand/1/parts/1');
    });
  });

  describe('все эндпоинты должны быть строками или функциями', () => {
    it('list должен быть строкой', () => {
      expect(typeof nightstandEndpoints.list).toBe('string');
    });

    it('get должен быть функцией', () => {
      expect(typeof nightstandEndpoints.get).toBe('function');
    });

    it('full должен быть функцией', () => {
      expect(typeof nightstandEndpoints.full).toBe('function');
    });

    it('create должен быть строкой', () => {
      expect(typeof nightstandEndpoints.create).toBe('string');
    });

    it('update должен быть функцией', () => {
      expect(typeof nightstandEndpoints.update).toBe('function');
    });

    it('delete должен быть функцией', () => {
      expect(typeof nightstandEndpoints.delete).toBe('function');
    });

    it('parts должен быть функцией', () => {
      expect(typeof nightstandEndpoints.parts).toBe('function');
    });

    it('part должен быть функцией', () => {
      expect(typeof nightstandEndpoints.part).toBe('function');
    });
  });
});
