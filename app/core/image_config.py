"""
Конфигурация путей к изображениям проекта.

Все пути относительно frontend/public/images/.
На продакшене nginx раздаёт статику из этого каталога.
"""

from typing import Dict

# Базовый URL-префикс для изображений (nginx раздаёт /images/ из frontend/public/images/)
IMAGES_BASE_URL = "/images"

# === Материалы ===
MATERIALS_PATH = f"{IMAGES_BASE_URL}/materials"
SHEET_MATERIALS_PATH = f"{MATERIALS_PATH}/sheet"
EDGE_MATERIALS_PATH = f"{MATERIALS_PATH}/edge"
DECOR_MATERIALS_PATH = f"{MATERIALS_PATH}/decor"

# === Фурнитура ===
HARDWARE_PATH = f"{IMAGES_BASE_URL}/hardware"
SLIDE_GUIDES_PATH = f"{HARDWARE_PATH}/slide_guides"
HINGES_PATH = f"{HARDWARE_PATH}/hinges"
SUPPORTS_PATH = f"{HARDWARE_PATH}/supports"
WALL_MOUNTS_PATH = f"{HARDWARE_PATH}/wall_mounts"

# === Товары ===
PRODUCTS_PATH = f"{IMAGES_BASE_URL}/products"
BOOKSHELF_PRODUCTS_PATH = f"{PRODUCTS_PATH}/bookshelf"
NIGHTSTAND_PRODUCTS_PATH = f"{PRODUCTS_PATH}/nightstand"
DRESSER_PRODUCTS_PATH = f"{PRODUCTS_PATH}/dresser"

# === Конфигуратор ===
CONFIGURATOR_PATH = f"{IMAGES_BASE_URL}/configurator"
CONFIGURATOR_TEXTURES_PATH = f"{CONFIGURATOR_PATH}/textures"
CONFIGURATOR_ICONS_PATH = f"{CONFIGURATOR_PATH}/icons"
CONFIGURATOR_PRESETS_PATH = f"{CONFIGURATOR_PATH}/presets"

# === UI ===
UI_PATH = f"{IMAGES_BASE_URL}/ui"
UI_BACKGROUNDS_PATH = f"{UI_PATH}/backgrounds"
UI_ICONS_PATH = f"{UI_PATH}/icons"
UI_LOGOS_PATH = f"{UI_PATH}/logos"

# === Загрузки ===
UPLOADS_PATH = f"{IMAGES_BASE_URL}/uploads"
UPLOADS_CONFIGURATIONS_PATH = f"{UPLOADS_PATH}/configurations"
UPLOADS_TEMP_PATH = f"{UPLOADS_PATH}/temp"

# Маппинг типов мебели на папки товаров
FURNITURE_IMAGE_PATHS: Dict[str, str] = {
    "bookshelf": BOOKSHELF_PRODUCTS_PATH,
    "nightstand": NIGHTSTAND_PRODUCTS_PATH,
    "dresser": DRESSER_PRODUCTS_PATH,
}

# Маппинг типов материалов на папки
MATERIAL_TYPE_PATHS: Dict[str, str] = {
    "sheet": SHEET_MATERIALS_PATH,
    "edge": EDGE_MATERIALS_PATH,
    "decor": DECOR_MATERIALS_PATH,
}

# Маппинг типов фурнитуры на папки
HARDWARE_TYPE_PATHS: Dict[str, str] = {
    "slide_guide": SLIDE_GUIDES_PATH,
    "hinge": HINGES_PATH,
    "support": SUPPORTS_PATH,
    "wall_mount": WALL_MOUNTS_PATH,
}
