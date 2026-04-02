import { makeAutoObservable } from 'mobx';

type Theme = 'light' | 'dark' | 'system';

class ThemeStore {
  theme: Theme = 'system';

  constructor() {
    makeAutoObservable(this);
    this.init();
  }

  private init() {
    const saved = localStorage.getItem('theme') as Theme | null;
    if (saved) {
      this.theme = saved;
    }
    this.applyTheme();
  }

  get currentTheme(): string {
    if (this.theme === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return this.theme;
  }

  setTheme(theme: Theme) {
    this.theme = theme;
    localStorage.setItem('theme', theme);
    this.applyTheme();
  }

  toggle() {
    const themes: Theme[] = ['light', 'dark', 'system'];
    const currentIndex = themes.indexOf(this.theme);
    const nextIndex = (currentIndex + 1) % themes.length;
    this.setTheme(themes[nextIndex]);
  }

  private applyTheme() {
    const isDark = this.currentTheme === 'dark';
    document.documentElement.classList.toggle('dark', isDark);
  }
}

export const themeStore = new ThemeStore();
export default themeStore;
