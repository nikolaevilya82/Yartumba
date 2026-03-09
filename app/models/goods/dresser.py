"""
Комод
"""
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Dresser(Base):
    """
    Комод.
    """
    __tablename__ = "dressers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    
    drawer_count = Column(Integer, nullable=False, default=4)
    drawer_rows = Column(Integer, nullable=False, default=2)
    dresser_type = Column(String(50), nullable=False, default="standard")
    has_legs = Column(Boolean, default=True)
    
    product = relationship("Product", backref="dresser")

    def __repr__(self):
        return f"<Dresser {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящиков>"

