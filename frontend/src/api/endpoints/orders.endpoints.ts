// Эндпоинты заказов

export const orderEndpoints = {
  // Заказы
  orders: '/v1/orders',
  order: (id: number) => `/v1/orders/${id}`,
  orderByNumber: (number: string) => `/v1/orders/number/${number}`,
  
  // Статусы и отслеживание
  orderStatus: (id: number) => `/v1/orders/${id}/status`,
  trackOrder: (id: number) => `/v1/orders/${id}/track`,
  trackByNumber: (number: string) => `/v1/orders/track/${number}`,
  
  // Операции с заказом
  cancelOrder: (id: number) => `/v1/orders/${id}/cancel`,
  confirmOrder: (id: number) => `/v1/orders/${id}/confirm`,
  startProduction: (id: number) => `/v1/orders/${id}/start-production`,
  completeOrder: (id: number) => `/v1/orders/${id}/complete`,
  deliverOrder: (id: number) => `/v1/orders/${id}/deliver`,
} as const;

export type OrderEndpoints = typeof orderEndpoints;
