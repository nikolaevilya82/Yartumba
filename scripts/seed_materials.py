"""
Сидер для заполнения БД базовыми материалами и фурнитурой.

Запуск:
    python scripts/seed_materials.py

Требует DATABASE_URL в .env (по умолчанию sqlite:///./test.db)
"""
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.db_setup import SessionLocal, engine, Base
from app.models.materials import SheetMaterial, EdgeMaterial, SlideGuide, Hinge, Support, WallMount


# === ЛДСП материалы ===
SHEET_MATERIALS = [
    {
        "name": "ЛДСП 16мм Дуб ватан",
        "material_type": "ldsp",
        "thickness": 16,
        "standard_width": 2800,
        "standard_height": 2070,
        "decor_name": "Дуб ватан",
        "hex_code": "#C4A882",
        "texture_url": None,
        "image_url": "/images/materials/sheet/дуб_ватан.jpg",
        "unit": "sheet",
        "price": 250000,  # 2500 руб в копейках
        "description": "ЛДСП 16мм, декор Дуб ватан, Kronospan",
        "is_active": "active",
    },
    {
        "name": "ЛДСП 16мм Белый гладкий",
        "material_type": "ldsp",
        "thickness": 16,
        "standard_width": 2800,
        "standard_height": 2070,
        "decor_name": "Белый гладкий",
        "hex_code": "#F5F5F5",
        "texture_url": None,
        "image_url": "/images/materials/sheet/белый_гладкий.jpg",
        "unit": "sheet",
        "price": 230000,  # 2300 руб
        "description": "ЛДСП 16мм, Белый гладкий, Kronospan",
        "is_active": "active",
    },
    {
        "name": "ЛДСП 16мм Кашемир",
        "material_type": "ldsp",
        "thickness": 16,
        "standard_width": 2800,
        "standard_height": 2070,
        "decor_name": "Кашемир",
        "hex_code": "#D4C5B5",
        "texture_url": None,
        "image_url": "/images/materials/sheet/кашемир.jpg",
        "unit": "sheet",
        "price": 270000,  # 2700 руб
        "description": "ЛДСП 16мм, декор Кашемир, Egger",
        "is_active": "active",
    },
]


# === Кромка (1:1 к ЛДСП) ===
EDGE_MATERIALS = [
    {
        "edge_type": "pvc",
        "thickness": 1,
        "width": 19,
        "decor_name": "Дуб ватан",
        "vendor_code": "PVC-19-DV",
        "price_per_meter": 1500,
        "image_url": "/images/materials/edge/дуб_ватан.jpg",
    },
    {
        "edge_type": "pvc",
        "thickness": 1,
        "width": 19,
        "decor_name": "Белый гладкий",
        "vendor_code": "PVC-19-BG",
        "price_per_meter": 1200,
        "image_url": "/images/materials/edge/белый_гладкий.jpg",
    },
    {
        "edge_type": "pvc",
        "thickness": 1,
        "width": 19,
        "decor_name": "Кашемир",
        "vendor_code": "PVC-19-KSH",
        "price_per_meter": 1600,
        "image_url": "/images/materials/edge/кашемир.jpg",
    },
]


# === Направляющие ===
SLIDE_GUIDES = [
    {
        "name": "Шариковые 300 мм",
        "guide_type": "ball",
        "extension_type": "partial",
        "length": 300,
        "load_capacity": 25,
        "has_soft_close": False,
        "manufacturer": "Hettich",
        "vendor_code": "KT-300-25",
        "price": 45000,  # 450 руб
        "image_url": "/images/hardware/slide_guides/шариковые_300.jpg",
    },
    {
        "name": "Шариковые 400 мм с доводчиком",
        "guide_type": "ball",
        "extension_type": "full",
        "length": 400,
        "load_capacity": 30,
        "has_soft_close": True,
        "manufacturer": "Blum",
        "vendor_code": "TANDEM-400",
        "price": 89000,  # 890 руб
        "image_url": "/images/hardware/slide_guides/шариковые_400_доводчик.jpg",
    },
    {
        "name": "Тандем 500 мм полновыкатные",
        "guide_type": "tandem",
        "extension_type": "full",
        "length": 500,
        "load_capacity": 30,
        "has_soft_close": True,
        "manufacturer": "Blum",
        "vendor_code": "TANDEM-500",
        "price": 120000,  # 1200 руб
        "image_url": "/images/hardware/slide_guides/тандем_500.jpg",
    },
]


# === Петли ===
HINGES = [
    {
        "name": "Петля Clip 110° с доводчиком",
        "hinge_type": "clip",
        "mounting_type": "overlay",
        "opening_angle": 110,
        "cup_diameter": 35,
        "has_soft_close": True,
        "has_integrated_soft_close": True,
        "manufacturer": "Blum",
        "vendor_code": "CLIP-110-SC",
        "price": 18000,  # 180 руб
        "image_url": "/images/hardware/hinges/clip_110_доводчик.jpg",
    },
    {
        "name": "Петля Slide-on 95°",
        "hinge_type": "slide_on",
        "mounting_type": "half_overlay",
        "opening_angle": 95,
        "cup_diameter": 35,
        "has_soft_close": False,
        "has_integrated_soft_close": False,
        "manufacturer": "Hettich",
        "vendor_code": "SO-95",
        "price": 12000,  # 120 руб
        "image_url": "/images/hardware/hinges/slide_on_95.jpg",
    },
]


# === Опоры / ножки ===
SUPPORTS = [
    {
        "name": "Ножка регулируемая 100 мм",
        "support_type": "adjustable",
        "material": "metal",
        "height": 100,
        "diameter": 30,
        "is_adjustable": True,
        "color": "Хром",
        "manufacturer": "Hettich",
        "vendor_code": "LEG-100-CH",
        "price": 8500,  # 85 руб
        "image_url": "/images/hardware/supports/ножка_100_хром.jpg",
    },
    {
        "name": "Ножка деревянная 150 мм",
        "support_type": "leg",
        "material": "solid_wood",
        "height": 150,
        "diameter": 40,
        "is_adjustable": False,
        "color": "Дуб",
        "manufacturer": "Мебельщик",
        "vendor_code": "LEG-150-OAK",
        "price": 15000,  # 150 руб
        "image_url": "/images/hardware/supports/ножка_150_дуб.jpg",
    },
    {
        "name": "Цоколь алюминиевый 100 мм",
        "support_type": "plinth",
        "material": "metal",
        "height": 100,
        "width": 16,
        "is_adjustable": True,
        "color": "Алюминий",
        "manufacturer": "Rehau",
        "vendor_code": "PLINTH-100-AL",
        "price": 45000,  # 450 руб/метр
        "image_url": "/images/hardware/supports/цоколь_100.jpg",
    },
]


# === Настенные крепления ===
WALL_MOUNTS = [
    {
        "name": "Навеска скрытая 40 кг",
        "mount_type": "hanger",
        "wall_type": "concrete",
        "max_load": 40,
        "adjustment": "3d",
        "is_hidden": True,
        "manufacturer": "Hettich",
        "vendor_code": "HANG-40-3D",
        "price": 12000,  # 120 руб
        "image_url": "/images/hardware/wall_mounts/навеска_40.jpg",
    },
    {
        "name": "Рейка навесная 1.5 м",
        "mount_type": "rail",
        "wall_type": "drywall",
        "max_load": 60,
        "adjustment": "horizontal",
        "is_hidden": True,
        "manufacturer": "Blum",
        "vendor_code": "RAIL-150",
        "price": 35000,  # 350 руб
        "image_url": "/images/hardware/wall_mounts/рейка_150.jpg",
    },
]


def seed_sheet_materials(db):
    """Создать листовые материалы и связанную кромку."""
    existing = db.query(SheetMaterial).count()
    if existing > 0:
        print(f"⚠️  SheetMaterial: уже есть {existing} записей, пропускаем")
        return

    for i, data in enumerate(SHEET_MATERIALS):
        sheet = SheetMaterial(**data)
        db.add(sheet)
        db.flush()  # чтобы получить sheet.id

        # Создаём кромку 1:1
        edge_data = EDGE_MATERIALS[i]
        edge = EdgeMaterial(
            sheet_material_id=sheet.id,
            **edge_data,
        )
        db.add(edge)
        print(f"  ✅ {sheet.name} + кромка {edge.decor_name}")

    db.commit()
    print(f"✅ Создано {len(SHEET_MATERIALS)} материалов + кромка")


def seed_slide_guides(db):
    """Создать направляющие."""
    existing = db.query(SlideGuide).count()
    if existing > 0:
        print(f"⚠️  SlideGuide: уже есть {existing} записей, пропускаем")
        return

    for data in SLIDE_GUIDES:
        db.add(SlideGuide(**data))
        print(f"  ✅ {data['name']}")

    db.commit()
    print(f"✅ Создано {len(SLIDE_GUIDES)} направляющих")


def seed_hinges(db):
    """Создать петли."""
    existing = db.query(Hinge).count()
    if existing > 0:
        print(f"⚠️  Hinge: уже есть {existing} записей, пропускаем")
        return

    for data in HINGES:
        db.add(Hinge(**data))
        print(f"  ✅ {data['name']}")

    db.commit()
    print(f"✅ Создано {len(HINGES)} петель")


def seed_supports(db):
    """Создать опоры."""
    existing = db.query(Support).count()
    if existing > 0:
        print(f"⚠️  Support: уже есть {existing} записей, пропускаем")
        return

    for data in SUPPORTS:
        db.add(Support(**data))
        print(f"  ✅ {data['name']}")

    db.commit()
    print(f"✅ Создано {len(SUPPORTS)} опор")


def seed_wall_mounts(db):
    """Создать настенные крепления."""
    existing = db.query(WallMount).count()
    if existing > 0:
        print(f"⚠️  WallMount: уже есть {existing} записей, пропускаем")
        return

    for data in WALL_MOUNTS:
        db.add(WallMount(**data))
        print(f"  ✅ {data['name']}")

    db.commit()
    print(f"✅ Создано {len(WALL_MOUNTS)} креплений")


def main():
    print("🌱 Запуск сидера материалов...")
    print(f"   БД: {engine.url}")

    # Создаём таблицы если их нет
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы (или уже существуют)\n")

    db = SessionLocal()
    try:
        seed_sheet_materials(db)
        seed_slide_guides(db)
        seed_hinges(db)
        seed_supports(db)
        seed_wall_mounts(db)
        print("\n🎉 Готово! БД заполнена.")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
