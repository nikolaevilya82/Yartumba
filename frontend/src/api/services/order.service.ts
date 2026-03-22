import { apiClient } from '../client';
import { orderEndpoints } from '../endpoints';
import type { ApiResponse } from '../../core/types/api.types';
import type { Order, OrderCustomer } from '../../core/types/cart.types';

// Создать заказ
export async function createOrder(
  customer: OrderCustomer
): Promise<ApiResponse<Order>> {
  return apiClient.post<ApiResponse<Order>>(orderEndpoints.orders, customer);
}

// Получить список заказов пользователя
export async function getMyOrders(): Promise<ApiResponse<Order[]>> {
  return apiClient.get<ApiResponse<Order[]>>(orderEndpoints.orders);
}

// Получить заказ по ID
export async function getOrderById(orderId: number): Promise<ApiResponse<Order>> {
  return apiClient.get<ApiResponse<Order>>(orderEndpoints.order(orderId));
}

// Получить заказ по номеру
export async function getOrderByNumber(orderNumber: string): Promise<ApiResponse<Order>> {
  return apiClient.get<ApiResponse<Order>>(`${orderEndpoints.orders}/number/${orderNumber}`);
}

// Отменить заказ
export async function cancelOrder(orderId: number): Promise<ApiResponse<Order>> {
  return apiClient.post<ApiResponse<Order>>(`${orderEndpoints.order(orderId)}/cancel`, {});
}

// Подтвердить заказ (для админа)
export async function confirmOrder(orderId: number): Promise<ApiResponse<Order>> {
  return apiClient.post<ApiResponse<Order>>(`${orderEndpoints.order(orderId)}/confirm`, {});
}

// Начать производство (для админа)
export async function startProduction(orderId: number): Promise<ApiResponse<Order>> {
  return apiClient.post<ApiResponse<Order>>(`${orderEndpoints.order(orderId)}/start-production`, {});
}

// Завершить заказ (для админа)
export async function completeOrder(orderId: number): Promise<ApiResponse<Order>> {
  return apiClient.post<ApiResponse<Order>>(`${orderEndpoints.order(orderId)}/complete`, {});
}

// Доставить заказ (для админа)
export async function deliverOrder(orderId: number): Promise<ApiResponse<Order>> {
  return apiClient.post<ApiResponse<Order>>(`${orderEndpoints.order(orderId)}/deliver`, {});
}

// Получить статус заказа
export async function getOrderStatus(orderId: number): Promise<ApiResponse<{ status: string }>> {
  return apiClient.get<ApiResponse<{ status: string }>>(`${orderEndpoints.order(orderId)}/status`);
}

// Отслеживание заказа
export interface OrderTracking {
  order_id: number;
  order_number: string;
  status: string;
  status_history: {
    status: string;
    timestamp: string;
    comment?: string;
  }[];
  estimated_delivery?: string;
}

// Получить историю отслеживания заказа
export async function trackOrder(orderId: number): Promise<ApiResponse<OrderTracking>> {
  return apiClient.get<ApiResponse<OrderTracking>>(`${orderEndpoints.order(orderId)}/track`);
}

// Получить историю отслеживания по номеру заказа
export async function trackOrderByNumber(orderNumber: string): Promise<ApiResponse<OrderTracking>> {
  return apiClient.get<ApiResponse<OrderTracking>>(`${orderEndpoints.orders}/track/${orderNumber}`);
}

// Типы статусов заказа
export type OrderStatus = Order['status'];

// Проверка возможности отмены заказа
export function canCancelOrder(order: Order): boolean {
  return ['pending', 'confirmed'].includes(order.status);
}

// Проверка возможности изменения заказа
export function canEditOrder(order: Order): boolean {
  return order.status === 'pending';
}

// Форматирование статуса заказа для отображения
export function formatOrderStatus(status: OrderStatus): string {
  const statusMap: Record<OrderStatus, string> = {
    pending: 'Ожидает подтверждения',
    confirmed: 'Подтверждён',
    processing: 'В производстве',
    ready: 'Готов к выдаче',
    delivered: 'Доставлен',
    cancelled: 'Отменён',
  };
  return statusMap[status] || status;
}

// Сервис заказов
export const orderService = {
  create: createOrder,
  getMyOrders,
  getById: getOrderById,
  getByNumber: getOrderByNumber,
  cancel: cancelOrder,
  confirm: confirmOrder,
  startProduction,
  complete: completeOrder,
  deliver: deliverOrder,
  getStatus: getOrderStatus,
  track: trackOrder,
  trackByNumber: trackOrderByNumber,
  canCancel: canCancelOrder,
  canEdit: canEditOrder,
  formatStatus: formatOrderStatus,
};

export default orderService;
