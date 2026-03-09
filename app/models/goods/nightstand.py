"""
Прикроватная тумба
"""
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Nightstand(Base):
    """
    Прикроватная тумба.
    """
    __tablename__ = "nightstands"

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
    
    drawer_count = Column(Integer, nullable=False, default=1)
    has_open_shelf = Column(Boolean, default=False)
    leg_type = Column(String(50), nullable=False, default="standard")
    
    product = relationship("Product", backref="nightstand")

    def __repr__(self):
        return f"<Nightstand {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящика>"

