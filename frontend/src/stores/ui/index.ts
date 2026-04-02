// UI Сторы (SRP - каждый отвечает за свою область)
export { modalStore } from './modal.store';
export type { ModalType, ModalConfig } from './modal.store';

export { notificationStore } from './notification.store';
export type { NotificationType, Notification } from './notification.store';

export { loadingStore } from './loading.store';

export { themeStore } from './theme.store';

export { languageStore } from './language.store';

export { sidebarStore } from './sidebar.store';
export type { SidebarConfig } from './sidebar.store';
