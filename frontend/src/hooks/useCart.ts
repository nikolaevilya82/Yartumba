// Заглушка для useCart - будет реализована после установки MobX
export function useCart() {
  return {
    items: [],
    totalItems: 0,
    totalPrice: 0,
    isEmpty: true,
    addToCart: async (_type: string, _config: any, _qty: number = 1) => {},
    removeFromCart: (_id: number) => {},
    updateItemQuantity: (_id: number, _qty: number) => {},
    incrementItem: (_id: number) => {},
    decrementItem: (_id: number) => {},
    clearCart: () => {},
  };
}
