export const appConfig = {
  name: 'Yartumba',
  title: 'Мебельная конфигураторная система',
  version: '1.0.0',
  description: 'Конфигуратор мебели: книжные полки, тумбы, комоды',
  author: 'NLP-Core-Team',
  defaultLanguage: 'ru',
  currency: '₽',
  currencyCode: 'RUB',
} as const;

export type AppConfig = typeof appConfig;
