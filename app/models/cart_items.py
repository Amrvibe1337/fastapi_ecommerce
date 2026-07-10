from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    __table_args__ = (
            UniqueConstraint("user_id", "product_id", name="uq_cart_items_user_product"),
            )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Отношение 7
    user: Mapped["User"] = relationship("User", back_populates="cart_items")    # type: ignore

    # Отношение 6
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")   # type: ignore
