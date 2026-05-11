"""update cart item with jsonb and product fk

Revision ID: 001
Revises: 
Create Date: 2025-04-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Обновление модели CartItem:
    1. Добавление FK на products таблицу
    2. Замена product_id на furniture_id
    3. Конвертация configuration из String в JSONB
    4. Изменение unit_price и total_price с Float на Numeric
    5. Добавление материалов снепшота
    6. Добавление временных меток
    """
    # Создаем новую колонку product_id для связи с products
    op.add_column('cart_items', sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Добавляем FK constraint на products
    op.create_foreign_key(
        'fk_cart_items_product',
        'cart_items', 'products',
        ['product_id'], ['id'],
        ondelete='RESTRICT'
    )
    
    # Добавляем furniture_id для хранения ID конкретной мебели
    op.add_column('cart_items', sa.Column('furniture_id', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Добавляем configuration как JSONB
    op.add_column('cart_items', sa.Column('configuration_jsonb', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    
    # Переносим данные из старой конфигурации (JSON строка) в новую (JSONB)
    op.execute("""
        UPDATE cart_items 
        SET configuration_jsonb = configuration::jsonb 
        WHERE configuration IS NOT NULL
    """)
    
    # Удаляем старую колонку configuration
    op.drop_column('cart_items', 'configuration')
    
    # Переименовываем configuration_jsonb в configuration
    op.alter_column('cart_items', 'configuration_jsonb', new_column_name='configuration')
    
    # Устанавливаем NOT NULL для configuration
    op.alter_column('cart_items', 'configuration', nullable=False)
    
    # Заполняем furniture_id из старого product_id (для обратной совместимости)
    op.execute("""
        UPDATE cart_items 
        SET furniture_id = product_id
    """)
    
    # Делаем furniture_id NOT NULL
    op.alter_column('cart_items', 'furniture_id', nullable=False)
    
    # Делаем product_id NOT NULL (после заполнения)
    # Предполагаем, что product_id уже был заполнен
    op.alter_column('cart_items', 'product_id', nullable=False)
    
    # Добавляем индекс для furniture_id
    op.create_index('ix_cart_items_furniture_id', 'cart_items', ['furniture_id'])
    
    # Добавляем материалы снепшот
    op.add_column('cart_items', sa.Column('materials_snapshot', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    
    # Заменяем Float на Numeric для unit_price
    op.add_column('cart_items', sa.Column('unit_price_new', sa.Numeric(10, 2), nullable=True))
    op.execute("""
        UPDATE cart_items SET unit_price_new = unit_price::numeric
    """)
    op.drop_column('cart_items', 'unit_price')
    op.alter_column('cart_items', 'unit_price_new', new_column_name='unit_price')
    
    # Заменяем Float на Numeric для total_price
    op.add_column('cart_items', sa.Column('total_price_new', sa.Numeric(10, 2), nullable=True))
    op.execute("""
        UPDATE cart_items SET total_price_new = total_price::numeric
    """)
    op.drop_column('cart_items', 'total_price')
    op.alter_column('cart_items', 'total_price_new', new_column_name='total_price')
    
    # Добавляем временные метки
    op.add_column('cart_items', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('cart_items', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Устанавливаем значения по умолчанию
    op.execute("""
        UPDATE cart_items 
        SET created_at = NOW(), updated_at = NOW()
    """)
    
    op.alter_column('cart_items', 'created_at', nullable=False)
    op.alter_column('cart_items', 'updated_at', nullable=False)
    
    # Добавляем индекс для product_type (он уже мог существовать)
    op.create_index('ix_cart_items_product_type', 'cart_items', ['product_type'], unique=False)


def downgrade() -> None:
    """
    Откат изменений - возвращаем к старой структуре
    """
    # Удаляем индексы
    op.drop_index('ix_cart_items_product_type', table_name='cart_items')
    
    # Удаляем временные метки
    op.drop_column('cart_items', 'updated_at')
    op.drop_column('cart_items', 'created_at')
    
    # Возвращаем Float для total_price
    op.add_column('cart_items', sa.Column('total_price_float', sa.Float(), nullable=True))
    op.execute("""
        UPDATE cart_items SET total_price_float = total_price::float
    """)
    op.drop_column('cart_items', 'total_price')
    op.alter_column('cart_items', 'total_price_float', new_column_name='total_price')
    
    # Возвращаем Float для unit_price
    op.add_column('cart_items', sa.Column('unit_price_float', sa.Float(), nullable=True))
    op.execute("""
        UPDATE cart_items SET unit_price_float = unit_price::float
    """)
    op.drop_column('cart_items', 'unit_price')
    op.alter_column('cart_items', 'unit_price_float', new_column_name='unit_price')
    
    # Удаляем materials_snapshot
    op.drop_column('cart_items', 'materials_snapshot')
    
    # Возвращаем String для configuration
    op.add_column('cart_items', sa.Column('configuration_old', sa.String(500), nullable=True))
    op.execute("""
        UPDATE cart_items SET configuration_old = configuration::text
    """)
    op.drop_column('cart_items', 'configuration')
    op.alter_column('cart_items', 'configuration_old', new_column_name='configuration')
    
    # Удаляем индекс furniture_id
    op.drop_index('ix_cart_items_furniture_id', table_name='cart_items')
    
    # Удаляем furniture_id
    op.drop_column('cart_items', 'furniture_id')
    
    # Удаляем FK constraint
    op.drop_constraint('fk_cart_items_product', 'cart_items', type_='foreignkey')
    
    # Удаляем product_id
    op.drop_column('cart_items', 'product_id')
