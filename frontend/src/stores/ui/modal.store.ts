import { makeAutoObservable } from 'mobx';

// Типы модалок
export type ModalType = 
  | 'none'
  | 'login'
  | 'register'
  | 'confirm'
  | 'delete'
  | 'promocode'
  | 'configurator'
  | 'orderSuccess'
  | 'imagePreview';

export interface ModalConfig {
  type: ModalType;
  data?: Record<string, unknown>;
  onConfirm?: () => void;
  onCancel?: () => void;
}

class ModalStore {
  activeModal: ModalConfig = { type: 'none' };

  constructor() {
    makeAutoObservable(this);
  }

  get isOpen(): boolean {
    return this.activeModal.type !== 'none';
  }

  get type(): ModalType {
    return this.activeModal.type;
  }

  open(config: ModalConfig) {
    this.activeModal = config;
  }

  close() {
    this.activeModal = { type: 'none' };
  }

  openLogin() {
    this.open({ type: 'login' });
  }

  openRegister() {
    this.open({ type: 'register' });
  }

  openConfirm(message: string, onConfirm: () => void, onCancel?: () => void) {
    this.open({ type: 'confirm', data: { message }, onConfirm, onCancel });
  }

  openDelete(itemName: string, onConfirm: () => void) {
    this.open({ type: 'delete', data: { itemName }, onConfirm });
  }

  openPromocode() {
    this.open({ type: 'promocode' });
  }

  openOrderSuccess(orderId: number) {
    this.open({ type: 'orderSuccess', data: { orderId } });
  }

  openImagePreview(imageUrl: string) {
    this.open({ type: 'imagePreview', data: { imageUrl } });
  }
}

export const modalStore = new ModalStore();
export default modalStore;
