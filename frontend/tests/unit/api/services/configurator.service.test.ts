import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import * as configuratorService from '@/api/services/configurator.service';
import * as apiClient from '@/api/client';

vi.mock('@/api/client', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/api/client')>();
  return {
    ...actual,
    apiClient: {
      get: vi.fn(),
      post: vi.fn(),
      patch: vi.fn(),
      delete: vi.fn(),
    },
  };
});

vi.mock('@/api/endpoints', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/api/endpoints')>();
  return {
    ...actual,
    configuratorEndpoints: {
      configurations: '/v1/configurator/configurations',
      configuration: (id: number) => `/v1/configurator/configurations/${id}`,
      createFromConfig: (id: number) => `/v1/configurator/configurations/${id}/create`,
      exportPdf: (id: number) => `/v1/configurator/configurations/${id}/export/pdf`,
      exportDxf: (id: number) => `/v1/configurator/configurations/${id}/export/dxf`,
    },
  };
});

describe('api/services/configurator', () => {
  const mockApiClient = apiClient.apiClient as {
    get: ReturnType<typeof vi.fn>;
    post: ReturnType<typeof vi.fn>;
    patch: ReturnType<typeof vi.fn>;
    delete: ReturnType<typeof vi.fn>;
  };

  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getConfiguratorOptions', () => {
    it('должен вызывать GET запрос для получения опций', async () => {
      const mockResponse = {
        data: {
          sheet_materials: [],
          edge_materials: [],
          slide_guides: [],
        },
      };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await configuratorService.getConfiguratorOptions();

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('/materials')
      );
    });

    it('должен возвращать опции конфигуратора', async () => {
      const mockOptions = {
        data: {
          sheet_materials: [{ id: 1, name: 'ДСП' }],
        },
      };
      mockApiClient.get.mockResolvedValueOnce(mockOptions);

      const result = await configuratorService.getConfiguratorOptions();

      expect(result.data.sheet_materials).toHaveLength(1);
    });
  });

  describe('calculateConfiguration', () => {
    it('должен вызывать POST запрос для расчёта стоимости', async () => {
      const mockResponse = { data: { total_price: 15000 } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      const config = {
        furniture_type: 'nightstand' as const,
        parts: [{ type: 'body', material_id: 1 }],
      };

      await configuratorService.calculateConfiguration(config);

      expect(mockApiClient.post).toHaveBeenCalledWith(
        expect.stringContaining('/calculate'),
        config
      );
    });

    it('должен возвращать расчёт стоимости', async () => {
      const mockResponse = {
        data: {
          total_price: 15000,
          breakdown: [],
        },
      };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      const result = await configuratorService.calculateConfiguration({
        furniture_type: 'nightstand',
        parts: [],
      });

      expect(result.data.total_price).toBe(15000);
    });
  });

  describe('validateConfiguration', () => {
    it('должен вызывать POST запрос для валидации', async () => {
      const mockResponse = { data: { valid: true, errors: [] } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      await configuratorService.validateConfiguration({
        furniture_type: 'bookshelf',
        parts: [],
      });

      expect(mockApiClient.post).toHaveBeenCalledWith(
        expect.stringContaining('/validate'),
        expect.any(Object)
      );
    });

    it('должен возвращать результат валидации', async () => {
      const mockResponse = {
        data: { valid: false, errors: ['Не выбран материал'] },
      };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      const result = await configuratorService.validateConfiguration({
        furniture_type: 'bookshelf',
        parts: [],
      });

      expect(result.data.valid).toBe(false);
      expect(result.data.errors).toHaveLength(1);
    });
  });

  describe('saveConfiguration', () => {
    it('должен вызывать POST запрос для сохранения конфигурации', async () => {
      const mockResponse = { data: { id: 1 } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      await configuratorService.saveConfiguration(
        'Моя полка',
        'bookshelf',
        { width: 1000 },
        10000
      );

      expect(mockApiClient.post).toHaveBeenCalledWith(
        expect.stringContaining('/configurations'),
        expect.objectContaining({
          name: 'Моя полка',
          furniture_type: 'bookshelf',
          total_price: 10000,
        })
      );
    });

    it('должен возвращать сохранённую конфигурацию', async () => {
      const mockResponse = {
        data: { id: 1, name: 'Test', total_price: 10000 },
      };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      const result = await configuratorService.saveConfiguration(
        'Test',
        'nightstand',
        {},
        5000
      );

      expect(result.data.id).toBe(1);
    });
  });

  describe('getConfiguration', () => {
    it('должен вызывать GET запрос для получения конфигурации по ID', async () => {
      const mockResponse = { data: { id: 123 } };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await configuratorService.getConfiguration(123);

      expect(mockApiClient.get).toHaveBeenCalledWith(
        expect.stringContaining('/configurations/123')
      );
    });
  });

  describe('getMyConfigurations', () => {
    it('должен вызывать GET запрос для получения списка конфигураций', async () => {
      const mockResponse = { data: [] };
      mockApiClient.get.mockResolvedValueOnce(mockResponse);

      await configuratorService.getMyConfigurations();

      expect(mockApiClient.get).toHaveBeenCalled();
    });
  });

  describe('updateConfiguration', () => {
    it('должен вызывать PATCH запрос для обновления конфигурации', async () => {
      const mockResponse = { data: { id: 1 } };
      mockApiClient.patch.mockResolvedValueOnce(mockResponse);

      await configuratorService.updateConfiguration(123, {
        name: 'Обновлённое имя',
      });

      expect(mockApiClient.patch).toHaveBeenCalledWith(
        expect.stringContaining('/configurations/123'),
        { name: 'Обновлённое имя' }
      );
    });
  });

  describe('deleteConfiguration', () => {
    it('должен вызывать DELETE запрос для удаления конфигурации', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.delete.mockResolvedValueOnce(mockResponse);

      await configuratorService.deleteConfiguration(123);

      expect(mockApiClient.delete).toHaveBeenCalledWith(
        expect.stringContaining('/configurations/123')
      );
    });

    it('должен возвращать результат удаления', async () => {
      const mockResponse = { data: { success: true } };
      mockApiClient.delete.mockResolvedValueOnce(mockResponse);

      const result = await configuratorService.deleteConfiguration(1);

      expect(result.data.success).toBe(true);
    });
  });

  describe('createFromConfiguration', () => {
    it('должен вызывать POST запрос для создания товара из конфигурации', async () => {
      const mockResponse = { data: { id: 1, furniture_type: 'bookshelf' } };
      mockApiClient.post.mockResolvedValueOnce(mockResponse);

      await configuratorService.createFromConfiguration(123);

      expect(mockApiClient.post).toHaveBeenCalledWith(
        expect.stringContaining('/configurations/123/create'),
        {}
      );
    });
  });

  describe('createConfiguratorService', () => {
    it('должен возвращать сервис с методами для React хуков', () => {
      const service = configuratorService.createConfiguratorService();

      expect(service.calculate).toBeDefined();
      expect(service.validate).toBeDefined();
      expect(service.save).toBeDefined();
      expect(service.getSaved).toBeDefined();
      expect(service.remove).toBeDefined();
    });

    it('должен возвращать null при ошибке в calculate', async () => {
      mockApiClient.post.mockRejectedValueOnce(new Error('API error'));

      const service = configuratorService.createConfiguratorService();
      const result = await service.calculate({ furniture_type: 'nightstand', parts: [] });

      expect(result).toBeNull();
    });

    it('должен возвращать { valid: false, errors: [...] } при ошибке в validate', async () => {
      mockApiClient.post.mockRejectedValueOnce(new Error('API error'));

      const service = configuratorService.createConfiguratorService();
      const result = await service.validate({ furniture_type: 'nightstand', parts: [] });

      expect(result).toEqual({ valid: false, errors: ['Ошибка валидации'] });
    });

    it('должен возвращать null при ошибке в save', async () => {
      mockApiClient.post.mockRejectedValueOnce(new Error('API error'));

      const service = configuratorService.createConfiguratorService();
      const result = await service.save('Test', 'bookshelf', {}, 1000);

      expect(result).toBeNull();
    });

    it('должен возвращать пустой массив при ошибке в getSaved', async () => {
      mockApiClient.get.mockRejectedValueOnce(new Error('API error'));

      const service = configuratorService.createConfiguratorService();
      const result = await service.getSaved();

      expect(result).toEqual([]);
    });

    it('должен возвращать false при ошибке в remove', async () => {
      mockApiClient.delete.mockRejectedValueOnce(new Error('API error'));

      const service = configuratorService.createConfiguratorService();
      const result = await service.remove(1);

      expect(result).toBe(false);
    });
  });

  describe('обработка ошибок', () => {
    it('должен пробрасывать ошибки от apiClient', async () => {
      const apiError = {
        code: 'CONFIG_ERROR',
        message: 'Configuration error',
        status_code: 400,
      };
      mockApiClient.post.mockRejectedValueOnce(apiError);

      await expect(
        configuratorService.calculateConfiguration({ furniture_type: 'nightstand', parts: [] })
      ).rejects.toEqual(apiError);
    });
  });
});
