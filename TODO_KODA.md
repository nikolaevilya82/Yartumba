# TODO для Koda — список задач по проекту Yartumba

> Сформирован после полного аудита проекта 2026-07-19.
> Ничего не менялось без согласия пользователя. Этот файл — памятка для следующих сессий.
> Отмечать выполненное через `[x]`. Приоритеты: 🔴 критично → 🟠 серьёзно → 🟡 средне → 🟢 мелочи.

---

## 🟡 ПРОБЛЕМЫ СРЕДНЕГО ПРИОРИТЕТА

### [x] 11. Мёртвый код / файлы-заглушки
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

**Сделано 2026-10-31:** все 13 файлов удалены. Перед удалением проверено grep-ом — импортов нет.

### [x] 12. Недокументированные модули моделей
Существуют целые пакеты моделей, не упомянутые ни в README, ни в KODA.md, ни в `app/models/__init__.py`:
- `app/models/inventory/` (stock, warehouse)
- `app/models/production/` (nesting, workorder)
- `app/models/sales/` (cart, customer, orders, payments) — **дублирует** `app/models/cart.py`?
- `app/models/users/` (user_auth)
- `app/models/catalog/assets.py`, `options.py`, `template.py`
- `app/models/components/handle.py`, `hardware.py`, `panel.py`

**Решение:** выяснить у пользователя статус. Если «в разработке» — описать в README как черновик. Если забытый код — убрать. Особенно проверить дубликат корзины (`app/models/sales/cart.py` vs `app/models/cart.py`).

**Сделано 2026-10-31:** все перечисленные файлы оказались пустыми (0 строк) и нигде не импортировались. Удалены по решению пользователя (вариант «А»). Дубликата корзины не существовало — `app/models/sales/cart.py` был пустым.

### [x] 13. `requirements.txt` неполон
- [x] Добавить `pydantic` (пинить явно) — `pydantic==2.10.6`
- [x] Добавить `pydantic-settings` (для `app/core/config.py`) — уже был
- [x] Добавить `coverage` (заявлен в README, но отсутствует) — `coverage==7.17.0` + `pytest-cov==7.1.0`
- [ ] Опционально: `python-multipart`, `email-validator` (для будущей авторизации)

### [x] 14. `.env.example` минимальный
Только `DATABASE_URL`. Добавить примеры:
- [x] `ENV=DEV|PROD`
- [x] `CORS_ORIGINS=http://localhost:5173,...`
- [x] `SECRET_KEY=...`
- [x] `SQL_ECHO=false`
- [x] `SESSION_SECRET=...`

**Сверено 2026-10-31:** `.env.example` содержит все шесть переменных и полностью совпадает с тем, что читает `app/core/config.py` (`DATABASE_URL`, `ENV`, `CORS_ORIGINS`, `SQL_ECHO`, `SECRET_KEY`, `SESSION_SECRET`). Дополнительно `DATABASE_URL` читается в `app/migrations/env.py`.

### [x] 15. `datetime.utcnow` устарел (deprecated с Python 3.12)
В `cart.py` и проверить другие модели.

**Решение:** заменить на `datetime.now(timezone.utc)` (или `func.now()` на уровне БД через `default=func.now()`).

**Сделано 2026-10-31:** в `app/models/cart.py` 4 места заменены на `lambda: datetime.now(timezone.utc)` (и `onupdate`). В остальных моделях `datetime` не использовался — проверено grep-ом по `app/` и `tests/`.

### [x] 16. Дублирование логики определения мебели
Одна и та же if/elif логика в трёх местах:
- `CartService._get_furniture` (cart_service.py:416)
- `CartItem.get_furniture_object` (cart.py:105)
- аналогичные проверки в конфигураторе

**Решение:** вынести в общий хелпер/реестр, например `app/core/furniture_registry.py` с маппингом `{"bookshelf": Bookshelf, "nightstand": Nightstand, "dresser": Dresser}`.

**Сделано 2026-10-31:** создан `app/core/furniture_registry.py` (`FURNITURE_MODELS`, `get_furniture_model`, `get_furniture`). `CartService._get_furniture` и `CartItem.get_furniture_object` теперь делегируют в реестр. В конфигураторе дублирования не было — там свои реестры `CALCULATORS` / `VALIDATORS` / `DIMENSION_LIMITS`.

---

## 🟢 МЕЛКИЕ УЛУЧШЕНИЯ / NICE-TO-HAVE

### [x] 19. `.gitignore` для `test.db`
- [x] Проверить наличие `.gitignore` — существует
- [x] Добавить `test.db`, `*.db`, `__pycache__/`, `.env`, `frontend/node_modules/` — `*.db`, `__pycache__/`, `.env` уже были; добавлено `frontend/node_modules/`

### [x] 20. Health-check не проверяет зависимости
`/health` возвращает просто `{"status": "ok"}`.
- [x] Добавить проверку соединения с БД (`SELECT 1`)

**Сделано 2026-10-31:** `/health` выполняет `SELECT 1` через `Depends(get_db)`, при ошибке возвращает `503` с текстом проблемы. Проверено вручную: 200 при доступной БД, 503 при подменённой сломанной сессии.

### [x] 21. Тесты: нет фикстур `client` и `authenticated_user`
`conftest.py` содержит только `engine` и `db_session`, но в skipped-тестах корзины используются `client`, `authenticated_user`, `cart_item`, `nightstand_config`, `promocode`.
- [x] Добавить фикстуру `client` (TestClient с переопределённым `get_db` на in-memory SQLite)
- [x] Добавить фикстуры `authenticated_user`, `cart_item`, `nightstand_config`, `promocode`
- [x] Снять skip с тестов корзины (нужны фикстуры `client`, `authenticated_user`)

**Сделано 2026-10-31:** в `tests/conftest.py` добавлены все пять фикстур. `engine` переведён на `StaticPool` + `check_same_thread=False`, чтобы TestClient видел ту же in-memory БД. `tests/integration/test_cart_integration.py` переписан на реальные проверки API (14 тестов), skip остался только у `test_apply_promocode` — промокодов в API нет.

### [x] 22. Баги, найденные при написании тестов корзины
- [x] `post.py`: сравнение `item.furniture_id` (UUID) с `request.furniture_id` (str) всегда давало False → 500 «Ошибка при добавлении товара». Исправлено на `str(...) == str(...)`.
- [x] `Cart.items`: у backref не было каскада, поэтому удаление корзины обнуляло `cart_items.cart_id` (NOT NULL) → IntegrityError при merge. Добавлен `cascade="all, delete-orphan"`.
- [x] UUID-колонки не принимали строковые ID (ломается на SQLite в тестах). Добавлен хелпер `app/core/identifiers.py: to_uuid()` и применён в `cart_service`, `dependencies`, `furniture_registry`.
- [x] `AddToCartRequest` не валидировал `furniture_type` (в отличие от `CartItemCreate`) → добавлен общий валидатор.

---

## 📋 Рекомендуемый порядок выполнения

1. **#11–#16** — чистка мёртвого кода, документации, зависимостей. ✅ выполнено
2. **#19–#21** — полировка README и тестов. ✅ выполнено

**Осталось (не входит в этот список):** реализация заказов (#заказы), авторизация, промокоды (см. skip в `test_cart_integration.py`), `python-multipart` / `email-validator` в `requirements.txt`.

---

## Заметки для следующих сессий

- **Всегда спрашивать согласие пользователя** перед изменениями (просил в первой сессии).
- **Критические баги #1–#4 исправлены (2026-07-21):** модель, миграция, сервис, тесты корзины синхронизированы. `product_type` → `furniture_type`, добавлен `configuration_id`, JSONB-хак убран, `main.py` — точка входа, `patch.py` — корректный статус 404.
- **#5–#9 исправлены (2026-07-21):** CORS вынесен в конфиг, `echo` читается из `SQL_ECHO`, создан `app/core/config.py` с `Settings`, создан `app/core/dependencies.py` с общим `get_db`, конфигуратор использует `Depends(get_db)`, `merge.py` получил `MergeCartsRequest` и `get_current_user_id`.
- **#11–#16, #19–#21 и #22 закрыты 2026-10-31.** Тесты: было 176 passed / 40 skipped, стало **190 passed / 32 skipped**.
- **Тесты корзины больше не skipped** — `tests/integration/test_cart_integration.py` работает через реальные HTTP-роуты. Единственный оставшийся skip — `test_apply_promocode` (промокодов нет в API).
- **Реальное приложение в `app/main.py`**, корневой `main.py` теперь корректно импортирует `from app.main import app`.
- **KODA.md и README.md местами расходятся с реальностью** — сверяться с кодом, не с докой.
- **Дубликата моделей корзины больше нет** — `app/models/sales/` удалён (был пустым).
- **UUID в тестах:** колонки объявлены как `PG_UUID(as_uuid=True)`, поэтому принимают только объекты `uuid.UUID`. Для строковых ID из HTTP используйте `app.core.identifiers.to_uuid()`. Если добавляете новые фильтры по UUID-колонкам — приводите значение, иначе на SQLite получите `AttributeError: 'str' object has no attribute 'hex'`.
