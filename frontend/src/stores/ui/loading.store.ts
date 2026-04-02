import { makeAutoObservable } from 'mobx';

class LoadingStore {
  isPageLoading = false;
  isGlobalLoading = false;
  loadingMessage = '';

  constructor() {
    makeAutoObservable(this);
  }

  setPageLoading(loading: boolean, message = '') {
    this.isPageLoading = loading;
    this.loadingMessage = message;
  }

  setGlobalLoading(loading: boolean, message = '') {
    this.isGlobalLoading = loading;
    this.loadingMessage = message;
  }

  show(message = 'Загрузка...') {
    this.isGlobalLoading = true;
    this.loadingMessage = message;
  }

  hide() {
    this.isGlobalLoading = false;
    this.loadingMessage = '';
  }

  showPage(message = '') {
    this.isPageLoading = true;
    this.loadingMessage = message;
  }

  hidePage() {
    this.isPageLoading = false;
    this.loadingMessage = '';
  }
}

export const loadingStore = new LoadingStore();
export default loadingStore;
