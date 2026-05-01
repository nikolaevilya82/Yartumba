import { describe, it, expect } from 'vitest';
import { orderEndpoints } from '@/api/endpoints';

describe('api/endpoints/orders', () => {
  describe('orders', () => {
    it('должен возвращать правильный URL для списка заказов', () => {
      expect(orderEndpoints.orders).toBe('/v1/orders');
    });
  });

  describe('order(id)', () => {
    it('должен возвращать правильный URL для заказа по ID', () => {
      expect(orderEndpoints.order(1)).toBe('/v1/orders/1');
      expect(orderEndpoints.order(123)).toBe('/v1/orders/123');
    });
  });

  describe('orderByNumber(number)', () => {
    it('должен возвращать правильный URL для заказа по номеру', () => {
      expect(orderEndpoints.orderByNumber('ORD-001')).toBe('/v1/orders/number/ORD-001');
      expect(orderEndpoints.orderByNumber('2024-12345')).toBe('/v1/orders/number/2024-12345');
    });
  });

  describe('orderStatus(id)', () => {
    it('должен возвращать правильный URL для статуса заказа', () => {
      expect(orderEndpoints.orderStatus(1)).toBe('/v1/orders/1/status');
      expect(orderEndpoints.orderStatus(123)).toBe('/v1/orders/123/status');
    });
  });

  describe('trackOrder(id)', () => {
    it('должен возвращать правильный URL для отслеживания заказа по ID', () => {
      expect(orderEndpoints.trackOrder(1)).toBe('/v1/orders/1/track');
      expect(orderEndpoints.trackOrder(123)).toBe('/v1/orders/123/track');
    });
  });

  describe('trackByNumber(number)', () => {
    it('должен возвращать правильный URL для отслеживания заказа по номеру', () => {
      expect(orderEndpoints.trackByNumber('ORD-001')).toBe('/v1/orders/track/ORD-001');
    });
  });

  describe('cancelOrder(id)', () => {
    it('должен возвращать правильный URL для отмены заказа', () => {
      expect(orderEndpoints.cancelOrder(1)).toBe('/v1/orders/1/cancel');
      expect(orderEndpoints.cancelOrder(123)).toBe('/v1/orders/123/cancel');
    });
  });

  describe('confirmOrder(id)', () => {
    it('должен возвращать правильный URL для подтверждения заказа', () => {
      expect(orderEndpoints.confirmOrder(1)).toBe('/v1/orders/1/confirm');
      expect(orderEndpoints.confirmOrder(123)).toBe('/v1/orders/123/confirm');
    });
  });

  describe('startProduction(id)', () => {
    it('должен возвращать правильный URL для запуска производства', () => {
      expect(orderEndpoints.startProduction(1)).toBe('/v1/orders/1/start-production');
      expect(orderEndpoints.startProduction(123)).toBe('/v1/orders/123/start-production');
    });
  });

  describe('completeOrder(id)', () => {
    it('должен возвращать правильный URL для завершения заказа', () => {
      expect(orderEndpoints.completeOrder(1)).toBe('/v1/orders/1/complete');
      expect(orderEndpoints.completeOrder(123)).toBe('/v1/orders/123/complete');
    });
  });

  describe('deliverOrder(id)', () => {
    it('должен возвращать правильный URL для доставки заказа', () => {
      expect(orderEndpoints.deliverOrder(1)).toBe('/v1/orders/1/deliver');
      expect(orderEndpoints.deliverOrder(123)).toBe('/v1/orders/123/deliver');
    });
  });

  describe('все эндпоинты должны быть строками или функциями', () => {
    it('orders должен быть строкой', () => {
      expect(typeof orderEndpoints.orders).toBe('string');
    });

    it('order должен быть функцией', () => {
      expect(typeof orderEndpoints.order).toBe('function');
    });

    it('orderByNumber должен быть функцией', () => {
      expect(typeof orderEndpoints.orderByNumber).toBe('function');
    });

    it('orderStatus должен быть функцией', () => {
      expect(typeof orderEndpoints.orderStatus).toBe('function');
    });

    it('trackOrder должен быть функцией', () => {
      expect(typeof orderEndpoints.trackOrder).toBe('function');
    });

    it('trackByNumber должен быть функцией', () => {
      expect(typeof orderEndpoints.trackByNumber).toBe('function');
    });

    it('cancelOrder должен быть функцией', () => {
      expect(typeof orderEndpoints.cancelOrder).toBe('function');
    });

    it('confirmOrder должен быть функцией', () => {
      expect(typeof orderEndpoints.confirmOrder).toBe('function');
    });

    it('startProduction должен быть функцией', () => {
      expect(typeof orderEndpoints.startProduction).toBe('function');
    });

    it('completeOrder должен быть функцией', () => {
      expect(typeof orderEndpoints.completeOrder).toBe('function');
    });

    it('deliverOrder должен быть функцией', () => {
      expect(typeof orderEndpoints.deliverOrder).toBe('function');
    });
  });
});
