import { useObserver } from 'mobx-react-lite';
import { cartStore } from '../stores/cart/cart.store';
import { cartActions } from '../stores/cart/cart.actions';
import type { FurnitureConfiguration } from '../core/types/configurator.types';
import type { FurnitureType } from '../core/constants/product.constants';

export function useCart() {
  return useObserver(() => ({
    items: cartStore.items,
    totalItems: cartStore.totalItems,
    totalPrice: cartStore.totalPrice,
    discountedPrice: cartStore.discountedPrice,
    isEmpty: cartStore.isEmpty,
    isLoading: cartStore.isLoading,
    addToCart: (type: FurnitureType, config: FurnitureConfiguration, qty: number = 1) =>
      cartActions.addItem(type, config, qty),
    removeFromCart: (id: string) => cartActions.removeItem(id),
    updateItemQuantity: (id: string, qty: number) => cartActions.updateQuantity(id, qty),
    incrementItem: (id: string) => cartActions.increment(id),
    decrementItem: (id: string) => cartActions.decrement(id),
    clearCart: () => cartActions.clear(),
  }));
}
