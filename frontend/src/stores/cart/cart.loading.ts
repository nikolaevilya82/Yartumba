import { makeAutoObservable } from 'mobx';

class CartLoadingStore {
  isLoading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  startLoading() {
    this.isLoading = true;
    this.error = null;
  }

  stopLoading(error: string | null = null) {
    this.isLoading = false;
    this.error = error;
  }

  setError(error: string) {
    this.error = error;
  }

  clearError() {
    this.error = null;
  }
}

export const cartLoadingStore = new CartLoadingStore();
export default cartLoadingStore;
