import { runInAction } from 'mobx';
import type { FurnitureConfiguration } from '../../core/types/configurator.types';
import type { FurnitureType } from '../../core/constants/product.constants';
import * as cartService from '../../api/services/cart.service';
import { cartStore } from './cart.store';
import { cartLoadingStore } from './cart.loading';
import { cartPromocodeStore } from './cart.promocode';

class CartActions {
  // Добавить товар
  async addItem(
    furnitureType: FurnitureType,
    configuration: FurnitureConfiguration,
    quantity: number = 1
  ) {
    cartLoadingStore.startLoading();
    try {
      const response = await cartService.addItemToCart(furnitureType, configuration, quantity);
      runInAction(() => {
        if (response.data.cart) {
          cartStore.updateFromResponse(response.data.cart);
        }
        cartLoadingStore.stopLoading();
      });
      return { success: true };
    } catch (error) {
      cartLoadingStore.stopLoading((error as Error).message);
      return { success: false, error: (error as Error).message };
    }
  }

  // Обновить количество
  async updateQuantity(itemId: number, quantity: number) {
    try {
      const response = await cartService.updateCartItem(itemId, { quantity });
      runInAction(() => {
        if (response.data.cart) {
          cartStore.updateFromResponse(response.data.cart);
        }
      });
    } catch (error) {
      cartLoadingStore.setError((error as Error).message);
    }
  }

  // Увеличить количество
  async increment(itemId: number) {
    try {
      const response = await cartService.incrementCartItem(itemId);
      runInAction(() => {
        if (response.data.cart) {
          cartStore.updateFromResponse(response.data.cart);
        }
      });
    } catch (error) {
      cartLoadingStore.setError((error as Error).message);
    }
  }

  // Уменьшить количество
  async decrement(itemId: number) {
    try {
      const response = await cartService.decrementCartItem(itemId);
      runInAction(() => {
        if (response.data.cart) {
          cartStore.updateFromResponse(response.data.cart);
        }
      });
    } catch (error) {
      cartLoadingStore.setError((error as Error).message);
    }
  }

  // Удалить товар
  async removeItem(itemId: number) {
    try {
      const response = await cartService.removeFromCart(itemId);
      runInAction(() => {
        if (response.data.cart) {
          cartStore.updateFromResponse(response.data.cart);
        }
      });
    } catch (error) {
      cartLoadingStore.setError((error as Error).message);
    }
  }

  // Очистить корзину
  async clear() {
    cartLoadingStore.startLoading();
    try {
      await cartService.clearCart();
      runInAction(() => {
        cartStore.clear();
        cartPromocodeStore.clear();
        cartLoadingStore.stopLoading();
      });
    } catch (error) {
      cartLoadingStore.stopLoading((error as Error).message);
    }
  }

  // Применить промокод
  async applyPromocode(code: string) {
    return cartPromocodeStore.apply(code);
  }

  // Удалить промокод
  async removePromocode() {
    await cartPromocodeStore.remove();
  }
}

export const cartActions = new CartActions();
export default cartActions;
