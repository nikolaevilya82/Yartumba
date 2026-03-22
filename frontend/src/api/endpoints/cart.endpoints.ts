// Эндпоинты корзины

export const cartEndpoints = {
  // Корзина
  cart: '/v1/cart',
  cartItem: (id: number) => `/v1/cart/items/${id}`,
  
  // Промокоды
  applyPromocode: '/v1/cart/promocode',
  removePromocode: '/v1/cart/promocode',
} as const;

export type CartEndpoints = typeof cartEndpoints;
