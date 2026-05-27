# Промт: User Journey — Прикроватная тумба (nightstand)

## Инструкция для исполнителя

При получении этого промта:
1. Проверить актуальное состояние кода для каждого шага.
2. Для каждого шага вывести статус: ✅ готово / 🟡 частично / ❌ не реализовано.
3. Для шагов со статусом ✅ или 🟡 — привести пример работающего кода из реальных файлов проекта.
4. Для шагов со статусом ❌ — написать `// TODO: [что нужно сделать]`.
5. Если статус изменился по сравнению с предыдущим ответом — указать что именно.
6. Кратко, только факты и код.

---

## Шаги для проверки

### 1. Заходит на сайт → каталог → список тумб
Проверить:
- `frontend/src/App.jsx`
- `frontend/src/routes/AppRoutes.jsx`
- `frontend/src/pages/catalog/CatalogPage.jsx`
- `frontend/src/stores/catalog/catalog.store.ts`
- `frontend/src/components/catalog/ProductList.jsx`
- `frontend/src/components/catalog/ProductCard.jsx`

### 2. Открывает карточку товара
Проверить:
- `frontend/src/components/catalog/ProductCard.jsx`
- `frontend/src/core/config/routes.config.ts`

### 3. Переходит в конфигуратор → меняет размеры, материал, ящики
Проверить:
- `frontend/src/pages/configurator/ConfiguratorPage.jsx`
- `frontend/src/routes/AppRoutes.jsx`
- `app/api/v1/configurator.py`
- `app/services/configurator/configurator_service.py`

### 4. Добавляет в корзину
Проверить:
- `frontend/src/stores/cart/cart.actions.ts`
- `frontend/src/api/services/cart.service.ts`
- `app/api/v1/goods/cart/routes/post.py`
- `app/services/cart_service.py`

### 5. Переходит в корзину → меняет количество
Проверить:
- `frontend/src/pages/cart/CartPage.jsx`
- `frontend/src/stores/cart/cart.actions.ts`
- `frontend/src/api/services/cart.service.ts`
- `app/api/v1/goods/cart/routes/patch.py`
- `app/services/cart_service.py`

### 6. Оформляет заказ → заполняет форму
Проверить:
- `frontend/src/pages/cart/CartPage.jsx`
- `app/api/v1/orders.py`

### 7. Регистрируется (прямо при оформлении)
Проверить:
- `frontend/src/pages/auth/RegisterPage.jsx`
- `frontend/src/routes/AppRoutes.jsx`

### 8. Выбирает оплату → подтверждает заказ
Проверить наличие:
- компонента выбора способа оплаты
- API подтверждения заказа

### 9. Оплачивает
Проверить наличие:
- платёжного виджета / интеграции
- API обработки платежа

### 10. Получает email с подтверждением
Проверить наличие:
- сервиса отправки email
- шаблона письма
- экрана успеха после оплаты

