import { makeAutoObservable } from 'mobx';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
  duration?: number;
}

class NotificationStore {
  notifications: Notification[] = [];

  constructor() {
    makeAutoObservable(this);
  }

  get hasNotifications(): boolean {
    return this.notifications.length > 0;
  }

  add(notification: Omit<Notification, 'id'>) {
    const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const newNotification: Notification = {
      ...notification,
      id,
      duration: notification.duration ?? 5000,
    };

    this.notifications.push(newNotification);

    // Автоматическое удаление
    if (newNotification.duration && newNotification.duration > 0) {
      setTimeout(() => this.remove(id), newNotification.duration);
    }

    return id;
  }

  remove(id: string) {
    this.notifications = this.notifications.filter(n => n.id !== id);
  }

  success(message: string, duration?: number) {
    return this.add({ type: 'success', message, duration });
  }

  error(message: string, duration?: number) {
    return this.add({ type: 'error', message, duration: duration ?? 8000 });
  }

  warning(message: string, duration?: number) {
    return this.add({ type: 'warning', message, duration });
  }

  info(message: string, duration?: number) {
    return this.add({ type: 'info', message, duration });
  }

  clearAll() {
    this.notifications = [];
  }
}

export const notificationStore = new NotificationStore();
export default notificationStore;
