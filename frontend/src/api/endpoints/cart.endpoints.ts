// Эндпоинты корзины

export const cartEndpoints = {
  // Корзина
  cart: '/v1/goods/cart',
  cartItem: (id: string) => `/v1/goods/cart/items/${id}`,
  
  // Промокоды
  applyPromocode: '/v1/goods/cart/promocode',
  removePromocode: '/v1/goods/cart/promocode',
} as const;

export type CartEndpoints = typeof cartEndpoints;
