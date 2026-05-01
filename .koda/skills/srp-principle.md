---
name: srp-principle
description: Всегда придерживаться принципа единой ответственности (SRP)
---

# Принцип единой ответственности (SRP)

## ⭐ Определение

**Single Responsibility Principle:** Класс, функция или модуль должен иметь **только одну причину для изменения**.

## 📐 Правила применения

### ✅ ЧТО ДЕЛАТЬ

1. **Одна функция = одна задача**
   ```typescript
   // ❌ ПЛОХО: функция делает слишком много
   function processOrder(order: Order) {
     validateOrder(order);
     calculateTotal(order);
     applyDiscount(order);
     saveToDatabase(order);
     sendEmail(order);
     updateInventory(order);
   }

   // ✅ ХОРОШО: каждая функция делает одно
   function validateOrder(order: Order): boolean { ... }
   function calculateTotal(order: Order): number { ... }
   function applyDiscount(order: Order): number { ... }
   function saveOrder(order: Order): void { ... }
   function sendOrderEmail(order: Order): void { ... }
   function updateOrderInventory(order: Order): void { ... }
   ```

2. **Один класс = одна ответственность**
   ```typescript
   // ❌ ПЛОХО: класс делает всё
   class Order {
     validate() { ... }
     calculateTotal() { ... }
     save() { ... }
     sendEmail() { ... }
   }

   // ✅ ХОРОШО: отдельные классы
   class OrderValidator { validate() { ... } }
   class OrderCalculator { calculateTotal() { ... } }
   class OrderRepository { save() { ... } }
   class OrderEmailer { sendEmail() { ... } }
   ```

3. **Один модуль = одна функциональность**
   ```
   ❌ ПЛОХО:
   utils.ts - валидация, форматирование, API, работа с localStorage

   ✅ ХОРОШО:
   validation.utils.ts
   format.utils.ts
   api.utils.ts
   storage.utils.ts
   ```

### ❌ ЧТО НЕ ДЕЛАТЬ

1. **Не создавай "Божественные объекты"** (God Objects)
   - Классы с 10+ методами
   - Файлы с 1000+ строками
   - Функции с 50+ строками

2. **Не смешивай уровни абстракции**
   ```typescript
   // ❌ ПЛОХО: бизнес-логика + UI + API
   function renderProduct() {
     const product = fetchFromAPI(); // API
     const validated = validate(product); // Бизнес
     return <div>{validated.name}</div>; // UI
   }

   // ✅ ХОРОШО: разделение по уровням
   // api/product.api.ts
   // services/product.service.ts
   // components/Product.tsx
   ```

3. **Не копируй/вставляй код**
   - Если повторяется 2+ раза — выноси в функцию
   - Если функция называется одинаково в разных местах — выноси в утилиту

## 📊 Метрики SRP

| Метрика | Хорошее значение | Тревожный сигнал |
|---------|------------------|------------------|
| Функция | < 20 строк | > 50 строк |
| Класс | < 10 методов | > 20 методов |
| Файл | < 300 строк | > 500 строк |
| Параметры функции | < 3 параметра | > 5 параметров |

## 🔧 Рефакторинг при нарушении

Если видишь нарушение SRP:

1. **Определи ответственности**
   - Что именно делает код?
   - Какие причины могут его изменить?

2. **Выдели отдельные модули**
   - Создай отдельные файлы/классы/функции
   - Каждому — свою ответственность

3. **Используй композицию**
   ```typescript
   class OrderService {
     constructor(
       private validator: OrderValidator,
       private calculator: OrderCalculator,
       private repository: OrderRepository
     ) {}

     process(order: Order) {
       this.validator.validate(order);
       const total = this.calculator.calculate(order);
       return this.repository.save({ ...order, total });
     }
   }
   ```

## 📝 Примеры из проекта

### ✅ Хорошо (в нашем проекте)

```typescript
// price.utils.ts - ТОЛЬКО форматирование цен
export function formatPrice(price: number): string { ... }
export function calculateDiscount(original: number, sale: number): number { ... }

// validation.utils.ts - ТОЛЬКО валидация
export function isValidEmail(email: string): boolean { ... }
export function required(value: unknown): boolean { ... }

// storage.utils.ts - ТОЛЬКО localStorage
export function setItem<T>(key: string, value: T): boolean { ... }
export function getItem<T>(key: string): T | null { ... }
```

### ❌ Плохо (избегай)

```typescript
// НЕЛЬЗЯ: смешивать утилиты
// bad.utils.ts
export function formatPrice() { ... }
export function isValidEmail() { ... }
export function saveToLocalStorage() { ... }
export function debounce() { ... }

// НЕЛЬЗЯ: смешивать слои
// product.component.tsx
export function Product() {
  const fetch = () => api.get(); // API
  const validate = () => {...}; // Бизнес
  return <div>...</div>; // UI
}
```

## 🚨 Нарушение SRP — это

- 🔴 Класс делает валидацию, сохранение, отправка email
- 🔴 Функция форматирует, валидирует и отправляет данные
- 🔴 Файл содержит 10 разных утилит из разных доменов
- 🔴 Метод класса управляет БД, API и UI одновременно

## ✅ Следование SRP — это

- 🟢 Каждый модуль делает одно дело и делает его хорошо
- 🟢 Легко тестировать (одна ответственность = один тест)
- 🟢 Легко менять (изменил одну часть — не сломал другие)
- 🟢 Легко переиспользовать (функциональность не завязана на контекст)

---

**Приоритет: ВЫСОКИЙ** ⚡

Этот принцип применяется ко ВСЕМ файлам и функциям проекта.
При создании нового кода — всегда сначала спроси: "Какая здесь ОДНА ответственность?"
