import { appConfig } from '../config/app.config';

/**
 * Форматирование цены в рублях
 */
export function formatPrice(price: number): string {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(price);
}

/**
 * Форматирование цены без символа валюты
 */
export function formatPriceOnly(price: number): string {
  return new Intl.NumberFormat('ru-RU').format(price);
}

/**
 * Форматирование цены с валютой (кастомный символ)
 */
export function formatPriceWithSymbol(price: number, symbol: string = appConfig.currency): string {
  const formatted = formatPriceOnly(price);
  return `${formatted} ${symbol}`;
}

/**
 * Расчёт скидки в процентах
 */
export function calculateDiscount(originalPrice: number, salePrice: number): number {
  if (originalPrice <= 0 || salePrice < 0) return 0;
  if (salePrice >= originalPrice) return 0;
  return Math.round(((originalPrice - salePrice) / originalPrice) * 100);
}

/**
 * Расчёт скидки для отображения
 */
export function calculateSalePrice(price: number, discountPercent: number): number {
  if (discountPercent < 0 || discountPercent > 100) return price;
  return Math.round(price * (1 - discountPercent / 100) * 100) / 100;
}

/**
 * Форматирование диапазона цен
 */
export function formatPriceRange(min: number, max: number): string {
  return `${formatPrice(min)} – ${formatPrice(max)}`;
}

/**
 * Форматирование большой цены (с пробелами)
 */
export function formatLargePrice(price: number): string {
  return formatPriceOnly(price).replace(/\s/g, ' ');
}

/**
 * Округление цены
 */
export function roundPrice(price: number, decimals: number = 0): number {
  const factor = Math.pow(10, decimals);
  return Math.round(price * factor) / factor;
}

/**
 * Проверка, является ли цена акционной
 */
export function isSalePrice(originalPrice: number, salePrice: number): boolean {
  return salePrice < originalPrice && salePrice > 0;
}
