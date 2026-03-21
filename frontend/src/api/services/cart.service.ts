import { apiClient } from '../client';
import { cartEndpoints } from '../endpoints';
import type { ApiResponse } from '../../core/types/api.types';
import type { 
  Cart, 
  CartItem, 
  AddToCartPayload,
  UpdateCartItemPayload,
  CartOperationResult 
} from '../../core/types/cart.types';
import type { FurnitureConfiguration } from '../../core/types/configurator.types';
import type { FurnitureType } from '../../core/constants/product.constants';

// Получить текущую корзину
export async function getCart(): Promise<ApiResponse<Cart>> {
  return apiClient.get<ApiResponse<Cart>>(cartEndpoints.cart);
}

// Добавить товар в корзину
export async function addToCart(
  payload: AddToCartPayload
): Promise<ApiResponse<CartOperationResult>> {
  return apiClient.post<ApiResponse<CartOperationResult>>(cartEndpoints.cart, payload);
}

// Добавить товар в корзину (упрощённый вариант)
export async function addItemToCart(
  furnitureType: FurnitureType,
  configuration: FurnitureConfiguration,
  quantity: number = 1
): Promise<ApiResponse<CartOperationResult>> {
  return addToCart({
    furniture_type: furnitureType,
    configuration,
    quantity,
  });
}

// Обновить количество товара в корзине
export async function updateCartItem(
  itemId: number,
  payload: UpdateCartItemPayload
): Promise<ApiResponse<CartOperationResult>> {
  return apiClient.patch<ApiResponse<CartOperationResult>>(
    cartEndpoints.cartItem(itemId),
    payload
  );
}

// Увеличить количество товара
export async function incrementCartItem(itemId: number): Promise<ApiResponse<CartOperationResult>> {
  const cart = await getCart();
  const item = cart.data.items.find(i => i.id === itemId);
  if (!item) {
    throw new Error('Item not found');
  }
  return updateCartItem(itemId, { quantity: item.quantity + 1 });
}

// Уменьшить количество товара
export async function decrementCartItem(itemId: number): Promise<ApiResponse<CartOperationResult>> {
  const cart = await getCart();
  const item = cart.data.items.find(i => i.id === itemId);
  if (!item) {
    throw new Error('Item not found');
  }
  if (item.quantity <= 1) {
    return removeFromCart(itemId);
  }
  return updateCartItem(itemId, { quantity: item.quantity - 1 });
}

// Удалить товар из корзины
export async function removeFromCart(itemId: number): Promise<ApiResponse<CartOperationResult>> {
  return apiClient.delete<ApiResponse<CartOperationResult>>(cartEndpoints.cartItem(itemId));
}

// Очистить корзину
export async function clearCart(): Promise<ApiResponse<CartOperationResult>> {
  return apiClient.delete<ApiResponse<CartOperationResult>>(cartEndpoints.cart);
}

// Применить промокод
export async function applyPromocode(
  code: string
): Promise<ApiResponse<{ discount: number; new_total: number }>> {
  return apiClient.post<ApiResponse<{ discount: number; new_total: number }>>(
    `${cartEndpoints.cart}/promocode`,
    { code }
  );
}

// Удалить промокод
export async function removePromocode(): Promise<ApiResponse<Cart>> {
  return apiClient.delete<ApiResponse<Cart>>(`${cartEndpoints.cart}/promocode`);
}

// Получить количество товаров в корзине
export async function getCartItemsCount(): Promise<number> {
  try {
    const response = await getCart();
    return response.data.total_items;
  } catch {
    return 0;
  }
}

// Получить общую стоимость корзины
export async function getCartTotal(): Promise<number> {
  try {
    const response = await getCart();
    return response.data.total_price;
  } catch {
    return 0;
  }
}

// Хелпер: проверить, есть ли товар в корзине
export async function isItemInCart(
  furnitureType: FurnitureType,
  furnitureId: number
): Promise<boolean> {
  try {
    const response = await getCart();
    return response.data.items.some(
      item => item.furniture_type === furnitureType && item.furniture_id === furnitureId
    );
  } catch {
    return false;
  }
}

// Сервис для работы с корзиной (удобная обёртка)
export const cartService = {
  getCart,
  addItem: addItemToCart,
  updateQuantity: updateCartItem,
  increment: incrementCartItem,
  decrement: decrementCartItem,
  remove: removeFromCart,
  clear: clearCart,
  applyPromocode,
  removePromocode,
  getCount: getCartItemsCount,
  getTotal: getCartTotal,
  isInCart: isItemInCart,
};

export default cartService;
