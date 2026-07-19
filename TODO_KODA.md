# TODO для Koda — список задач по проекту Yartumba

> Сформирован после полного аудита проекта 2026-07-19.
> Ничего не менялось без согласия пользователя. Этот файл — памятка для следующих сессий.
> Отмечать выполненное через `[x]`. Приоритеты: 🔴 критично → 🟠 серьёзно → 🟡 средне → 🟢 мелочи.

---

## 🔴 КРИТИЧЕСКИЕ БАГИ (код сломан в рантайме)

### [ ] 1. Корзина: модель и API/сервис рассинхронизированы
**Проблема:** `CartItem` (app/models/cart.py:66) использует поле `product_type`, а весь слой API/сервис/схемы используют `furniture_type` и `configuration_id`, которых **нет в модели и в БД**. Любой запрос к API корзины → `AttributeError`.

Дополнительно в `cart_service.py:400` (merge_carts) используется `saved_configuration_snapshot`, которого нет в модели (там `materials_snapshot`).

**Рассинхрон:**
| Слой | Поле типа | Поле ID конфига |
|------|-----------|-----------------|
| Модель `CartItem` + миграция 001 + test_cart_item.py | `product_type` | ❌ нет |
| Pydantic-схемы, CartService, все роуты | `furniture_type` | `configuration_id` |

**Почему не ловится тестами:** `tests/integration/test_cart_integration.py` — все классы помечены `@pytest.mark.skip`.

**Решение (рекомендуется Вариант A):**
- [ ] Вариант A: переименовать `product_type` → `furniture_type` в модели + добавить поле `configuration_id` + новая миграция + обновить test_cart_item.py. Так API становится консистентным и соответствует `furniture_type` в Drawer/FurnitureMaterial.
- [ ] Вариант B: переименовать `furniture_type` → `product_type` во всех схемах/сервисах/роутах.
- [ ] Поправить `saved_configuration_snapshot` → `materials_snapshot` в cart_service.py:400
- [ ] Снять `@pytest.mark.skip` с интеграционных тестов корзины и реализовать их (нужны фикстуры `client`, `authenticated_user` — см. пункт 21)

### [ ] 2. Корневой `main.py` сломан
**Проблема:** README:115 инструктирует `uvicorn main:app --reload`, но корневой `main.py` содержит 9 строк мусора (обрывки определения колонок модели), а не FastAPI-приложение. Реальное приложение — `app/main.py`.

**Решение (на выбор):**
- [ ] Удалить корневой `main.py` + поправить README на `uvicorn app.main:app --reload`
- [ ] ИЛИ сделать корневой `main.py` правильной точкой входа (`from app.main import app`)

### [ ] 3. `patch.py:63` — баг с HTTP-статусом
**Проблема:**
```python
raise HTTPException(status_code=HTTPException.status_code, detail="Товар не найден в корзине")
```
`HTTPException.status_code` — атрибут экземпляра, не класса → выбросит `AttributeError` вместо 500.

**Решение:** заменить на `status.HTTP_500_INTERNAL_SERVER_ERROR` (или лучше — 404, т.к. товар не найден).

### [ ] 4. Хак с типом JSONB в модели не работает
**Проблема:** `cart.py:76,88`:
```python
configuration = Column(PG_JSONB() if hasattr(PG_JSONB, '_is_postgresql') else JSON, ...)
```
У класса `postgresql.JSONB` нет атрибута `_is_postgresql` → `hasattr` всегда `False` → колонка всегда объявляется как `JSON`, а миграция создаёт `JSONB`. Несоответствие → Alembic autogenerate постоянно предлагает «поправить» тип.

**Решение:** использовать универсальный `from sqlalchemy import JSON` (работает и в SQLite, и в PG), либо явный `JSONB` для PostgreSQL с условием по движку БД.

---

## 🟠 СЕРЬЁЗНЫЕ ПРОБЛЕМЫ

### [ ] 5. CORS небезопасен и технически некорректен
**Проблема:** `app/main.py:16` — `allow_origins=["*"]` + `allow_credentials=True`. Браузеры отклоняют эту комбинацию.

**Решение:** вынести список доменов в конфиг (env-переменная `CORS_ORIGINS`), для DEV — localhost:5173 и т.п.

### [ ] 6. `app/core/db_setup.py` — `echo=True` захардкожен
**Проблема:** SQL-логирование в продакшене засоряет логи и тормозит работу.

**Решение:** `echo=os.getenv("SQL_ECHO", "false").lower() == "true"`.

### [ ] 7. `app/core/config.py` пустой
**Проблема:** нет класса настроек. `DATABASE_URL` читается прямо в db_setup.py, CORS захардкожен, `.env.example` содержит только DATABASE_URL.

**Решение:** создать Pydantic Settings класс (`Settings`) со всеми переменными: DATABASE_URL, ENV (DEV/PROD), CORS_ORIGINS, SECRET_KEY, SQL_ECHO, SESSION_SECRET и т.д. Использовать во всём проекте через DI/синглтон.

### [ ] 8. Эндпоинты конфигуратора не используют DI
**Проблема:** `app/api/v1/configurator.py` создаёт `db = SessionLocal()` вручную в каждом обработчике вместо `Depends(get_db)` (который уже есть в `goods/dependencies.py`).

Дополнительно: дублирование if/elif по `furniture_type` (строки 74–84 и 113–119) — сервис сам умеет валидировать тип, блоки избыточны.

**Решение:**
- [ ] Заменить `db = SessionLocal()` на `db: Session = Depends(get_db)` (вынести `get_db` в общее место, например `app/core/dependencies.py`)
- [ ] Убрать дублирующие if/elif — просто вызывать `service.validate/calculate(furniture_type, config)` и ловить ValueError → HTTPException

### [ ] 9. `merge.py` — `user_id: str` как query-параметр
**Проблема:** `async def merge_carts(request: dict, user_id: str, ...)` — FastAPI воспримет `user_id` как обязательный query-параметр, а не «получить из токена».

**Решение:** реализовать зависимость `get_current_user_id` (пока заглушка-TODO), использовать `user_id: str = Depends(get_current_user_id)`. Также `request: dict` → нормальная Pydantic-схема `MergeCartsRequest`.

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
- [ ] Снять skip с тестов корзины после пункта 1

---

## 📋 Рекомендуемый порядок выполнения

1. **#1–#4** — критические баги (корзина, main.py, patch.py, JSONB-хак). Без них проект не работает.
2. **#5–#10** — безопасность и архитектура (CORS, config, DI, консистентность экспортов).
3. **#11–#16** — чистка мёртвого кода, документации, зависимостей.
4. **#17–#21** — полировка README и тестов.

---

## Заметки для следующих сессий

- **Всегда спрашивать согласие пользователя** перед изменениями (просил в первой сессии).
- **Тесты корзины skipped** — значит баг #1 не ловится. После фикса обязательно раскомментить тесты.
- **Реальное приложение в `app/main.py`**, не в корневом `main.py`.
- **`get_db` живёт в `app/api/v1/goods/dependencies.py`** — лучше вынести в `app/core/dependencies.py` для общего использования (конфигуратору тоже нужен).
- **KODA.md и README.md местами расходятся с реальностью** — сверяться с кодом, не с докой.
- **Есть дублирующие модули моделей** (`app/models/sales/cart.py` vs `app/models/cart.py`) — выяснить у пользователя, какой каноничный.
