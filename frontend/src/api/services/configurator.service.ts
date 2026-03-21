import { apiClient } from '../client';
import { commonEndpoints, configuratorEndpoints } from '../endpoints';
import type { ApiResponse } from '../../core/types/api.types';
import type { 
  FurnitureConfiguration, 
  SavedConfiguration,
  ConfigurationCalculation,
  ConfiguratorOptions 
} from '../../core/types/configurator.types';
import type { FurnitureType } from '../../core/constants/product.constants';

// Загрузка опций конфигуратора
export async function getConfiguratorOptions(): Promise<ApiResponse<ConfiguratorOptions>> {
  return apiClient.get<ApiResponse<ConfiguratorOptions>>(commonEndpoints.materials.all);
}

// Расчёт стоимости конфигурации
export async function calculateConfiguration(
  configuration: FurnitureConfiguration
): Promise<ApiResponse<ConfigurationCalculation>> {
  return apiClient.post<ApiResponse<ConfigurationCalculation>>(
    `${configuratorEndpoints.configurations}/calculate`,
    configuration
  );
}

// Валидация конфигурации
export async function validateConfiguration(
  configuration: FurnitureConfiguration
): Promise<ApiResponse<{ valid: boolean; errors: string[] }>> {
  return apiClient.post<ApiResponse<{ valid: boolean; errors: string[] }>>(
    `${configuratorEndpoints.configurations}/validate`,
    configuration
  );
}

// Сохранить конфигурацию
export async function saveConfiguration(
  name: string,
  furnitureType: FurnitureType,
  configuration: FurnitureConfiguration,
  totalPrice: number
): Promise<ApiResponse<SavedConfiguration>> {
  return apiClient.post<ApiResponse<SavedConfiguration>>(configuratorEndpoints.configurations, {
    name,
    furniture_type: furnitureType,
    configuration,
    total_price: totalPrice,
  });
}

// Получить сохранённую конфигурацию
export async function getConfiguration(id: number): Promise<ApiResponse<SavedConfiguration>> {
  return apiClient.get<ApiResponse<SavedConfiguration>>(`${configuratorEndpoints.configuration(id)}`);
}

// Получить все сохранённые конфигурации пользователя
export async function getMyConfigurations(): Promise<ApiResponse<SavedConfiguration[]>> {
  return apiClient.get<ApiResponse<SavedConfiguration[]>>(endpoints.configurations);
}

// Обновить конфигурацию
export async function updateConfiguration(
  id: number,
  data: Partial<{
    name: string;
    configuration: FurnitureConfiguration;
    total_price: number;
  }>
): Promise<ApiResponse<SavedConfiguration>> {
  return apiClient.patch<ApiResponse<SavedConfiguration>>(
    `${configuratorEndpoints.configuration(id)}`,
    data
  );
}

// Удалить конфигурацию
export async function deleteConfiguration(id: number): Promise<ApiResponse<{ success: boolean }>> {
  return apiClient.delete<ApiResponse<{ success: boolean }>>(`${configuratorEndpoints.configuration(id)}`);
}

// Создать товар из конфигурации
export async function createFromConfiguration(
  configurationId: number
): Promise<ApiResponse<{ id: number; furniture_type: FurnitureType }>> {
  return apiClient.post<ApiResponse<{ id: number; furniture_type: FurnitureType }>>(
    configuratorEndpoints.createFromConfig(configurationId),
    {}
  );
}

// Экспорт конфигурации в PDF
export async function exportConfigurationToPdf(
  configurationId: number
): Promise<Blob> {
  const response = await fetch(configuratorEndpoints.exportPdf(configurationId), {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('auth_token') || ''}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to export PDF');
  }
  
  return response.blob();
}

// Экспорт конфигурации в чертеж (DXF)
export async function exportConfigurationToDxf(
  configurationId: number
): Promise<Blob> {
  const response = await fetch(configuratorEndpoints.exportDxf(configurationId), {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('auth_token') || ''}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to export DXF');
  }
  
  return response.blob();
}

// Типы для хука useConfigurator
export interface UseConfiguratorService {
  calculate: (config: FurnitureConfiguration) => Promise<ConfigurationCalculation | null>;
  validate: (config: FurnitureConfiguration) => Promise<{ valid: boolean; errors: string[] }>;
  save: (name: string, type: FurnitureType, config: FurnitureConfiguration, price: number) => Promise<SavedConfiguration | null>;
  getSaved: () => Promise<SavedConfiguration[]>;
  remove: (id: number) => Promise<boolean>;
}

// Сервис для использования в React хуках
export function createConfiguratorService(): UseConfiguratorService {
  return {
    calculate: async (config) => {
      try {
        const response = await calculateConfiguration(config);
        return response.data;
      } catch (error) {
        console.error('Failed to calculate configuration:', error);
        return null;
      }
    },
    
    validate: async (config) => {
      try {
        const response = await validateConfiguration(config);
        return response.data;
      } catch (error) {
        console.error('Failed to validate configuration:', error);
        return { valid: false, errors: ['Ошибка валидации'] };
      }
    },
    
    save: async (name, type, config, price) => {
      try {
        const response = await saveConfiguration(name, type, config, price);
        return response.data;
      } catch (error) {
        console.error('Failed to save configuration:', error);
        return null;
      }
    },
    
    getSaved: async () => {
      try {
        const response = await getMyConfigurations();
        return response.data;
      } catch (error) {
        console.error('Failed to get configurations:', error);
        return [];
      }
    },
    
    remove: async (id) => {
      try {
        await deleteConfiguration(id);
        return true;
      } catch (error) {
        console.error('Failed to delete configuration:', error);
        return false;
      }
    },
  };
}
