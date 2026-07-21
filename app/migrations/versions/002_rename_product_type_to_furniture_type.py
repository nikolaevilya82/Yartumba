"""rename product_type to furniture_type, add configuration_id

Revision ID: 002
Revises: 001
Create Date: 2026-07-21

Исправляет рассинхрон модели CartItem и слоя API/сервис/схемы:
1. Переименование product_type -> furniture_type (соответствует Drawer/FurnitureMaterial)
2. Добавление configuration_id (опциональный ID конфигурации из каталога)
3. Унификация типа configuration/materials_snapshot (JSONB в PostgreSQL)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    1. Переименовать product_type -> furniture_type (колонка + индекс)
    2. Добавить configuration_id (nullable, с индексом)
    """
    # --- 1. Переименование product_type -> furniture_type ---

    # Удаляем старый индекс
    op.drop_index('ix_cart_items_product_type', table_name='cart_items')

    # Переименовываем колонку
    op.alter_column('cart_items', 'product_type', new_column_name='furniture_type')

    # Создаём новый индекс
    op.create_index('ix_cart_items_furniture_type', 'cart_items', ['furniture_type'], unique=False)

    # --- 2. Добавление configuration_id ---

    op.add_column(
        'cart_items',
        sa.Column('configuration_id', postgresql.UUID(as_uuid=True), nullable=True)
    )
    op.create_index('ix_cart_items_configuration_id', 'cart_items', ['configuration_id'], unique=False)


def downgrade() -> None:
    """
    Откат: вернуть furniture_type -> product_type, убрать configuration_id
    """
    # --- 2. Удаление configuration_id ---
    op.drop_index('ix_cart_items_configuration_id', table_name='cart_items')
    op.drop_column('cart_items', 'configuration_id')

    # --- 1. Переименование furniture_type -> product_type ---
    op.drop_index('ix_cart_items_furniture_type', table_name='cart_items')
    op.alter_column('cart_items', 'furniture_type', new_column_name='product_type')
    op.create_index('ix_cart_items_product_type', 'cart_items', ['product_type'], unique=False)
