import type { FurnitureType } from '../constants/product.constants';
import type { FurnitureConfiguration } from './configurator.types';

// Элемент корзины
export interface CartItem {
  id: number;
  furniture_type: FurnitureType;
  furniture_id?: number;
  configuration: CartItemConfiguration;
  quantity: number;
  unit_price: number;
  total_price: number;
  created_at: string;
}

// Конфигурация товара в корзине
export interface CartItemConfiguration {
  name: string;
  width: number;
  height: number;
  depth: number;
  shelf_count?: number;
  drawer_count?: number;
  row_count?: number;
  material_name?: string;
  edge_name?: string;
  slide_guide_name?: string;
  hinge_name?: string;
  support_name?: string;
  image?: string;
}

// Корзина
export interface Cart {
  id: number;
  items: CartItem[];
  total_items: number;
  total_price: number;
  created_at: string;
  updated_at: string;
}

// Данные для добавления в корзину
export interface AddToCartPayload {
  furniture_type: FurnitureType;
  furniture_id?: number;
  configuration: FurnitureConfiguration;
  quantity: number;
}

// Обновление количества в корзине
export interface UpdateCartItemPayload {
  quantity: number;
}

// Результат операции с корзиной
export interface CartOperationResult {
  success: boolean;
  message: string;
  cart?: Cart;
  item?: CartItem;
}

// Типы для оформления заказа
export interface OrderCustomer {
  name: string;
  phone: string;
  email?: string;
  address?: string;
  comment?: string;
}

export interface Order {
  id: number;
  order_number: string;
  customer: OrderCustomer;
  items: CartItem[];
  total_price: number;
  status: OrderStatus;
  created_at: string;
  updated_at: string;
}

export type OrderStatus = 
  | 'pending' 
  | 'confirmed' 
  | 'processing' 
  | 'ready' 
  | 'delivered' 
  | 'cancelled';

export const orderStatusNames: Record<OrderStatus, string> = {
  pending: 'Ожидает подтверждения',
  confirmed: 'Подтверждён',
  processing: 'В производстве',
  ready: 'Готов к выдаче',
  delivered: 'Доставлен',
  cancelled: 'Отменён',
};
