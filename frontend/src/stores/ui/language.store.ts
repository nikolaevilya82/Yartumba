import { makeAutoObservable } from 'mobx';

type Language = 'ru' | 'en';

class LanguageStore {
  language: Language = 'ru';

  constructor() {
    makeAutoObservable(this);
    this.init();
  }

  private init() {
    const saved = localStorage.getItem('language') as Language | null;
    if (saved) {
      this.language = saved;
    }
  }

  setLanguage(lang: Language) {
    this.language = lang;
    localStorage.setItem('language', lang);
  }

  toggle() {
    this.language = this.language === 'ru' ? 'en' : 'ru';
    localStorage.setItem('language', this.language);
  }
}

export const languageStore = new LanguageStore();
export default languageStore;
