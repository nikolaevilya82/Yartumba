import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

type ModalType = 'none' | 'login' | 'register' | 'confirm' | 'delete' | 'promocode' | 'configurator' | 'orderSuccess' | 'imagePreview';

interface ModalConfig {
  type: ModalType;
  data?: Record<string, unknown>;
  onConfirm?: () => void;
  onCancel?: () => void;
}

class SimpleModalStore {
  activeModal: ModalConfig = { type: 'none' };

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

describe('Modal Store', () => {
  let modalStore: SimpleModalStore;

  beforeEach(() => {
    vi.clearAllMocks();
    modalStore = new SimpleModalStore();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('initialState', () => {
    it('должен быть закрыт по умолчанию', () => {
      expect(modalStore.isOpen).toBe(false);
    });

    it('должен иметь тип none по умолчанию', () => {
      expect(modalStore.type).toBe('none');
    });
  });

  describe('open', () => {
    it('должен открывать модалку с типом login', () => {
      modalStore.open({ type: 'login' });
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('login');
    });

    it('должен открывать модалку с типом confirm', () => {
      const onConfirm = vi.fn();
      modalStore.open({ type: 'confirm', data: { message: 'Test' }, onConfirm });
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('confirm');
      expect(modalStore.activeModal.data?.message).toBe('Test');
    });

    it('должен передавать данные в модалку', () => {
      modalStore.open({ 
        type: 'delete', 
        data: { itemName: 'Test Item' },
        onConfirm: vi.fn()
      });
      
      expect(modalStore.activeModal.data?.itemName).toBe('Test Item');
    });

    it('должен передавать onConfirm callback', () => {
      const onConfirm = vi.fn();
      modalStore.open({ type: 'confirm', onConfirm });
      
      modalStore.activeModal.onConfirm?.();
      expect(onConfirm).toHaveBeenCalled();
    });
  });

  describe('close', () => {
    it('должен закрывать открытую модалку', () => {
      modalStore.open({ type: 'login' });
      expect(modalStore.isOpen).toBe(true);
      
      modalStore.close();
      expect(modalStore.isOpen).toBe(false);
      expect(modalStore.type).toBe('none');
    });

    it('должен сбрасывать тип в none', () => {
      modalStore.open({ type: 'register' });
      modalStore.close();
      
      expect(modalStore.type).toBe('none');
    });
  });

  describe('openLogin', () => {
    it('должен открывать модалку входа', () => {
      modalStore.openLogin();
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('login');
    });
  });

  describe('openRegister', () => {
    it('должен открывать модалку регистрации', () => {
      modalStore.openRegister();
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('register');
    });
  });

  describe('openConfirm', () => {
    it('должен открывать confirm модалку с сообщением', () => {
      const onConfirm = vi.fn();
      modalStore.openConfirm('Are you sure?', onConfirm);
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('confirm');
      expect(modalStore.activeModal.data?.message).toBe('Are you sure?');
    });

    it('должен передавать onCancel callback', () => {
      const onConfirm = vi.fn();
      const onCancel = vi.fn();
      modalStore.openConfirm('Test', onConfirm, onCancel);
      
      modalStore.activeModal.onCancel?.();
      expect(onCancel).toHaveBeenCalled();
    });
  });

  describe('openDelete', () => {
    it('должен открывать delete модалку с названием элемента', () => {
      const onConfirm = vi.fn();
      modalStore.openDelete('Item Name', onConfirm);
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('delete');
      expect(modalStore.activeModal.data?.itemName).toBe('Item Name');
    });
  });

  describe('openPromocode', () => {
    it('должен открывать промокод модалку', () => {
      modalStore.openPromocode();
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('promocode');
    });
  });

  describe('openOrderSuccess', () => {
    it('должен открывать модалку успеха заказа с ID', () => {
      modalStore.openOrderSuccess(123);
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('orderSuccess');
      expect(modalStore.activeModal.data?.orderId).toBe(123);
    });
  });

  describe('openImagePreview', () => {
    it('должен открывать модалку предпросмотра изображения', () => {
      const imageUrl = 'https://example.com/image.jpg';
      modalStore.openImagePreview(imageUrl);
      
      expect(modalStore.isOpen).toBe(true);
      expect(modalStore.type).toBe('imagePreview');
      expect(modalStore.activeModal.data?.imageUrl).toBe(imageUrl);
    });
  });
});

