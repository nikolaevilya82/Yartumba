import { makeAutoObservable } from 'mobx';

class CatalogLoadingStore {
  isLoading: boolean = false;
  error: string | null = null;
  loadingCount: number = 0;
  
  constructor() {
    makeAutoObservable(this);
  }
  
  startLoading() {
    this.loadingCount++;
    this.isLoading = true;
    this.error = null;
  }
  
  stopLoading(error?: string) {
    this.loadingCount = Math.max(0, this.loadingCount - 1);
    this.isLoading = this.loadingCount > 0;
    if (error) {
      this.error = error;
    }
  }
  
  get hasError(): boolean {
    return this.error !== null;
  }
}

export const catalogLoadingStore = new CatalogLoadingStore();
export default catalogLoadingStore;
