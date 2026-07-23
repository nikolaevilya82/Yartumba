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

  get isLoading(): boolean {
    return cartLoadingStore.isLoading;
  }

  get discountedPrice(): number {
    const discount = cartPromocodeStore.discount;
    if (discount <= 0) return this.totalPrice;
    return this.totalPrice * (1 - discount / 100);
  }

  // Моковые данные для разработки (без бэкенда)
  private _mockCart: Cart = {
    id: '1',
    items: [
      {
        id: 'mock-item-1',
        furniture_type: 'nightstand',
        furniture_id: '223e4567-e89b-12d3-a456-426614174000',
        configuration: {
          name: 'Тумба "Уют"',
          width: 500,
          height: 500,
          depth: 400,
          drawer_count: 1,
          material_name: 'ЛДСП Дуб сонома',
        },
        quantity: 2,
        unit_price: 5200,
        total_price: 10400,
        created_at: new Date().toISOString(),
      },
      {
        id: 'mock-item-2',
        furniture_type: 'bookshelf',
        furniture_id: '123e4567-e89b-12d3-a456-426614174000',
        configuration: {
          name: 'Стеллаж "Лес"',
          width: 800,
          height: 200,
          depth: 300,
          shelf_count: 4,
          material_name: 'ДСП Белый',
        },
        quantity: 1,
        unit_price: 8500,
        total_price: 8500,
        created_at: new Date().toISOString(),
      },
    ],
    total_items: 3,
    total_price: 18900,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

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
      // Если бэкенд недоступен, используем моковые данные для разработки
      console.warn('Бэкенд недоступен, использую моковые данные корзины');
      runInAction(() => {
        this.cart = this._mockCart;
        cartLoadingStore.stopLoading();
      });
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
