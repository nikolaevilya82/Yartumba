import { describe, it, expect } from 'vitest';
import { bookshelfEndpoints } from '@/api/endpoints/products';

describe('api/endpoints/bookshelf', () => {
  describe('list', () => {
    it('должен возвращать правильный URL для списка полок', () => {
      expect(bookshelfEndpoints.list).toBe('/v1/goods/bookshelf');
    });
  });

  describe('get(id)', () => {
    it('должен возвращать правильный URL для получения полки по ID', () => {
      expect(bookshelfEndpoints.get(1)).toBe('/v1/goods/bookshelf/1');
      expect(bookshelfEndpoints.get(123)).toBe('/v1/goods/bookshelf/123');
      expect(bookshelfEndpoints.get(9999)).toBe('/v1/goods/bookshelf/9999');
    });

    it('должен работать с ID 0', () => {
      expect(bookshelfEndpoints.get(0)).toBe('/v1/goods/bookshelf/0');
    });
  });

  describe('full(id)', () => {
    it('должен возвращать правильный URL для получения полки с деталями', () => {
      expect(bookshelfEndpoints.full(1)).toBe('/v1/goods/bookshelf/1/full');
      expect(bookshelfEndpoints.full(123)).toBe('/v1/goods/bookshelf/123/full');
    });
  });

  describe('create', () => {
    it('должен возвращать правильный URL для создания полки', () => {
      expect(bookshelfEndpoints.create).toBe('/v1/goods/bookshelf');
    });
  });

  describe('update(id)', () => {
    it('должен возвращать правильный URL для обновления полки', () => {
      expect(bookshelfEndpoints.update(1)).toBe('/v1/goods/bookshelf/1');
      expect(bookshelfEndpoints.update(123)).toBe('/v1/goods/bookshelf/123');
    });
  });

  describe('delete(id)', () => {
    it('должен возвращать правильный URL для удаления полки', () => {
      expect(bookshelfEndpoints.delete(1)).toBe('/v1/goods/bookshelf/1');
      expect(bookshelfEndpoints.delete(123)).toBe('/v1/goods/bookshelf/123');
    });
  });

  describe('parts(id)', () => {
    it('должен возвращать правильный URL для списка деталей полки', () => {
      expect(bookshelfEndpoints.parts(1)).toBe('/v1/goods/bookshelf/1/parts');
      expect(bookshelfEndpoints.parts(123)).toBe('/v1/goods/bookshelf/123/parts');
    });
  });

  describe('part(id, partId)', () => {
    it('должен возвращать правильный URL для детали полки по ID', () => {
      expect(bookshelfEndpoints.part(1, 2)).toBe('/v1/goods/bookshelf/1/parts/2');
      expect(bookshelfEndpoints.part(123, 456)).toBe('/v1/goods/bookshelf/123/parts/456');
      expect(bookshelfEndpoints.part(1, 1)).toBe('/v1/goods/bookshelf/1/parts/1');
    });
  });

  describe('все эндпоинты должны быть строками или функциями', () => {
    it('list должен быть строкой', () => {
      expect(typeof bookshelfEndpoints.list).toBe('string');
    });

    it('get должен быть функцией', () => {
      expect(typeof bookshelfEndpoints.get).toBe('function');
    });

    it('full должен быть функцией', () => {
      expect(typeof bookshelfEndpoints.full).toBe('function');
    });

    it('create должен быть строкой', () => {
      expect(typeof bookshelfEndpoints.create).toBe('string');
    });

    it('update должен быть функцией', () => {
      expect(typeof bookshelfEndpoints.update).toBe('function');
    });

    it('delete должен быть функцией', () => {
      expect(typeof bookshelfEndpoints.delete).toBe('function');
    });

    it('parts должен быть функцией', () => {
      expect(typeof bookshelfEndpoints.parts).toBe('function');
    });

    it('part должен быть функцией', () => {
      expect(typeof bookshelfEndpoints.part).toBe('function');
    });
  });
});
