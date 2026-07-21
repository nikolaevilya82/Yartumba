# TODO для Koda — список задач по проекту Yartumba

> Сформирован после полного аудита проекта 2026-07-19.
> Ничего не менялось без согласия пользователя. Этот файл — памятка для следующих сессий.
> Отмечать выполненное через `[x]`. Приоритеты: 🔴 критично → 🟠 серьёзно → 🟡 средне → 🟢 мелочи.

---

## 🟠 СЕРЬЁЗНЫЕ ПРОБЛЕМЫ

### [ ] 10. `app/__init__.py` и `app/models/__init__.py` расходятся
**Проблемы:**
- `app/__init__.py` не экспортирует `Cart`, `CartItem` (нет в `__all__`), хотя импортирует `FurnitureMaterial` отдельной строкой.
- `app/models/__init__.py` экспортирует `Cart, CartItem`, но **не импортирует** `NightstandPart`, `DresserPart` (есть в goods, но не в `__all__`). При этом `BookshelfPart` экспортируется — непоследовательно.

**Решение:**
- [ ] Добавить `Cart, CartItem` в `app/__init__.py`
- [ ] Добавить `NightstandPart, DresserPart` в `app/models/__init__.py` и `app/__init__.py`
- [ ] Унифицировать импорт `FurnitureMaterial` (через `app.models.catalog`, а не отдельной строкой)

---

## 🟡 ПРОБЛЕМЫ СРЕДНЕГО ПРИОРИТЕТА

### [ ] 11. Мёртвый код / файлы-заглушки
Засоряют структуру и вводят в заблуждение. Не подключены к роутеру, не используются.

| Файл | Содержимое |
|------|-----------|
| `app/services/configuratorservice.py` | 13 строк комментариев |
| `app/services/catalogservice.py` | 3 строки комментариев |
| `app/services/fulfilment_service.py` | 6 строк комментариев |
| `app/services/inventoryservice.py` | 3 строки комментариев |
| `app/services/pricingservice.py` | 3 строки комментариев |
| `app/api/v1/goods_cart.py` | 1 строка комментария |
| `app/api/v1/goods_catalog.py` | заглушка |
| `app/api/v1/inventory_admin.py` | заглушка |
| `app/api/v1/orders.py` | 1 строка комментария |
| `app/core/DI.py` | пустой |
| `app/core/exceptions.py` | пустой |
| `app/core/logging.py` | пустой |
| `app/core/base_model.py` | проверить использование (везде `from app.core.db_setup import Base`) |

**Решение:** удалить заглушки или реализовать. Спросить пользователя — это задумка на будущее или забытый код.

### [ ] 12. Недокументированные модули моделей
Существуют целые пакеты моделей, не упомянутые ни в README, ни в KODA.md, ни в `app/models/__init__.py`:
- `app/models/inventory/` (stock, warehouse)
- `app/models/production/` (nesting, workorder)
- `app/models/sales/` (cart, customer, orders, payments) — **дублирует** `app/models/cart.py`?
- `app/models/users/` (user_auth)
- `app/models/catalog/assets.py`, `options.py`, `template.py`
- `app/models/components/handle.py`, `hardware.py`, `panel.py`

**Решение:** выяснить у пользователя статус. Если «в разработке» — описать в README как черновик. Если забытый код — убрать. Особенно проверить дубликат корзины (`app/models/sales/cart.py` vs `app/models/cart.py`).

### [ ] 13. `requirements.txt` неполон
- [ ] Добавить `pydantic` (пинить явно)
- [ ] Добавить `pydantic-settings` (для `app/core/config.py`)
- [ ] Добавить `coverage` (заявлен в README, но отсутствует)
- [ ] Опционально: `python-multipart`, `email-validator` (для будущей авторизации)

### [ ] 14. `.env.example` минимальный
Только `DATABASE_URL`. Добавить примеры:
- [ ] `ENV=DEV|PROD`
- [ ] `CORS_ORIGINS=http://localhost:5173,...`
- [ ] `SECRET_KEY=...`
- [ ] `SQL_ECHO=false`
- [ ] `SESSION_SECRET=...`

### [ ] 15. `datetime.utcnow` устарел (deprecated с Python 3.12)
В `cart.py` и проверить другие модели.

**Решение:** заменить на `datetime.now(timezone.utc)` (или `func.now()` на уровне БД через `default=func.now()`).

### [ ] 16. Дублирование логики определения мебели
Одна и та же if/elif логика в трёх местах:
- `CartService._get_furniture` (cart_service.py:416)
- `CartItem.get_furniture_object` (cart.py:105)
- аналогичные проверки в конфигураторе

**Решение:** вынести в общий хелпер/реестр, например `app/core/furniture_registry.py` с маппингом `{"bookshelf": Bookshelf, "nightstand": Nightstand, "dresser": Dresser}`.

---

## 🟢 МЕЛКИЕ УЛУЧШЕНИЯ / NICE-TO-HAVE

### [ ] 17. README не соответствует фактическому API
- [ ] В секциях «Прикроватные тумбы» и «Комоды» не перечислены эндпоинты `/parts` (POST/GET/PATCH/DELETE), хотя они есть в роутах и KODA.md
- [ ] Нет эндпоинтов корзины (`/v1/goods/cart/...`), хотя они реализованы
- [ ] В секциях «Каталог» и «Материалы» указаны эндпоинты (`/v1/categories`, `/v1/materials/sheet` и т.д.), но **роутеры не подключены** в `router.py` (только `goods` и `configurator`). Либо реализовать, либо убрать из README.

### [ ] 18. KODA.md содержит дубли и неточности
- [ ] Блок `app/services/` описан дважды (копипаст)
- [ ] Упоминается `calculators/base_calculator.py`, которого нет (реальный файл — `furniture_calculator.py`)
- [ ] Проверить остальные расхождения с реальной структурой

### [ ] 19. `.gitignore` для `test.db`
`db_setup.py` дефолтит на `sqlite:///./test.db` — файл может попасть в git.
- [ ] Проверить наличие `.gitignore`
- [ ] Добавить `test.db`, `*.db`, `__pycache__/`, `.env`, `frontend/node_modules/`

### [ ] 20. Health-check не проверяет зависимости
`/health` возвращает просто `{"status": "ok"}`.
- [ ] Добавить проверку соединения с БД (`SELECT 1`)

### [ ] 21. Тесты: нет фикстур `client` и `authenticated_user`
`conftest.py` содержит только `engine` и `db_session`, но в skipped-тестах корзины используются `client`, `authenticated_user`, `cart_item`, `nightstand_config`, `promocode`.
- [ ] Добавить фикстуру `client` (TestClient с переопределённым `get_db` на in-memory SQLite)
- [ ] Добавить фикстуры `authenticated_user`, `cart_item`, `nightstand_config`, `promocode`
- [ ] Снять skip с тестов корзины (нужны фикстуры `client`, `authenticated_user`)

---

## 📋 Рекомендуемый порядок выполнения

1. **#10** — консистентность экспортов.
2. **#11–#16** — чистка мёртвого кода, документации, зависимостей.
3. **#17–#21** — полировка README и тестов.

---

## Заметки для следующих сессий

- **Всегда спрашивать согласие пользователя** перед изменениями (просил в первой сессии).
- **Критические баги #1–#4 исправлены (2026-07-21):** модель, миграция, сервис, тесты корзины синхронизированы. `product_type` → `furniture_type`, добавлен `configuration_id`, JSONB-хак убран, `main.py` — точка входа, `patch.py` — корректный статус 404.
- **#5–#9 исправлены (2026-07-21):** CORS вынесен в конфиг, `echo` читается из `SQL_ECHO`, создан `app/core/config.py` с `Settings`, создан `app/core/dependencies.py` с общим `get_db`, конфигуратор использует `Depends(get_db)`, `merge.py` получил `MergeCartsRequest` и `get_current_user_id`.
- **Тесты корзины skipped** — интеграционные тесты (`tests/integration/test_cart_integration.py`) по-прежнему пропущены. Для их разблокировки нужны фикстуры `client` и `authenticated_user` (см. пункт 21).
- **Реальное приложение в `app/main.py`**, корневой `main.py` теперь корректно импортирует `from app.main import app`.
- **KODA.md и README.md местами расходятся с реальностью** — сверяться с кодом, не с докой.
- **Есть дублирующие модули моделей** (`app/models/sales/cart.py` vs `app/models/cart.py`) — выяснить у пользователя, какой каноничный.
