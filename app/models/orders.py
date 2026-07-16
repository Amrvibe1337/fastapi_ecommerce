from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base
from sqlalchemy import ForeignKey, String, Numeric, func, DateTime, Integer
from decimal import Decimal
from datetime import datetime


class Order(Base):
    __tablename__  = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Отношения
    user: Mapped["User"] = relationship("User", back_populates="orders")    # type: ignore
    items: Mapped[list["OrderItem"]] = relationship(    # type: ignore
            "OrderItem", back_populates="order", cascade="all, delete-orphan"
            )   
    

# 1 объект OrderItem соответствует 1 объекту класса Product
class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
            ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id: Mapped[int] = mapped_column(
            ForeignKey("products.id"), nullable=False, index=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")  # type: ignore
