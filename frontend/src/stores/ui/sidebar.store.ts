import React from 'react';
import { makeAutoObservable } from 'mobx';

export interface SidebarConfig {
  isOpen: boolean;
  content?: React.ReactNode;
  position: 'left' | 'right';
  width?: number;
}

class SidebarStore {
  config: SidebarConfig = {
    isOpen: false,
    position: 'right',
    width: 400,
  };

  constructor() {
    makeAutoObservable(this);
  }

  get isOpen(): boolean {
    return this.config.isOpen;
  }

  open(content: React.ReactNode, position: 'left' | 'right' = 'right', width = 400) {
    this.config = { isOpen: true, content, position, width };
  }

  close() {
    this.config.isOpen = false;
  }

  toggle() {
    this.config.isOpen = !this.config.isOpen;
  }
}

export const sidebarStore = new SidebarStore();
export default sidebarStore;
