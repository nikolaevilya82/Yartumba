// Эндпоинты конфигуратора

export const configuratorEndpoints = {
  // Конфигурации
  configurations: '/v1/configurations',
  configuration: (id: number) => `/v1/configurations/${id}`,
  
  // Операции с конфигурациями
  calculate: '/v1/configurations/calculate',
  validate: '/v1/configurations/validate',
  createFromConfig: (id: number) => `/v1/configurations/${id}/create`,
  
  // Экспорт
  exportPdf: (id: number) => `/v1/configurations/${id}/export/pdf`,
  exportDxf: (id: number) => `/v1/configurations/${id}/export/dxf`,
} as const;

export type ConfiguratorEndpoints = typeof configuratorEndpoints;
