import { makeAutoObservable, runInAction } from 'mobx';
import * as cartService from '../../api/services/cart.service';

class CartPromocodeStore {
  promocode: string | null = null;
  discount = 0;

  constructor() {
    makeAutoObservable(this);
  }

  get hasDiscount(): boolean {
    return this.discount > 0;
  }

  async apply(code: string) {
    try {
      const response = await cartService.applyPromocode(code);
      runInAction(() => {
        this.promocode = code;
        this.discount = response.data.discount;
      });
      return { success: true, discount: response.data.discount };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  async remove() {
    try {
      await cartService.removePromocode();
      runInAction(() => {
        this.promocode = null;
        this.discount = 0;
      });
    } catch (error) {
      // Игнорируем ошибку при удалении промокода
    }
  }

  clear() {
    this.promocode = null;
    this.discount = 0;
  }
}

export const cartPromocodeStore = new CartPromocodeStore();
export default cartPromocodeStore;
