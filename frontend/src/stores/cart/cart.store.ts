import { makeAutoObservable, runInAction } from 'mobx';
import type { Cart, CartItem } from '../../core/types/cart.types';
import * as cartService from '../../api/services/cart.service';
import { cartLoadingStore } from './cart.loading';
import { cartPromocodeStore } from './cart.promocode';

class CartStore {
  cart: Cart | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  // Геттеры - только чтение данных
  get items(): CartItem[] {
    return this.cart?.items ?? [];
  }

  get totalItems(): number {
    return this.cart?.total_items ?? 0;
  }

  get totalPrice(): number {
    return this.cart?.total_price ?? 0;
  }

  get isEmpty(): boolean {
    return this.items.length === 0;
  }

  get discountedPrice(): number {
    const discount = cartPromocodeStore.discount;
    if (discount <= 0) return this.totalPrice;
    return this.totalPrice * (1 - discount / 100);
  }

  // Загрузка корзины
  async fetch() {
    cartLoadingStore.startLoading();
    try {
      const response = await cartService.getCart();
      runInAction(() => {
        this.cart = response.data;
        cartLoadingStore.stopLoading();
      });
    } catch (error) {
      cartLoadingStore.stopLoading((error as Error).message);
    }
  }

  // Обновить корзину из ответа
  updateFromResponse(cart: Cart | null) {
    this.cart = cart;
  }

  // Очистить корзину
  clear() {
    this.cart = null;
  }
}

export const cartStore = new CartStore();
export default cartStore;
