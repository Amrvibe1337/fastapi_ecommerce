from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, Boolean, Float, Integer, Numeric, text, DateTime, Computed, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship  
from sqlalchemy import ForeignKey, func  

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)  
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0, server_default=text('0')) # средний рейтинг
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
    tsv: Mapped[TSVECTOR] = mapped_column(
        TSVECTOR,
        Computed(
            """
            setweight(to_tsvector('english', coalesce(name, '')), 'A')
            || 
            setweight(to_tsvector('english', coalesce(description, '')), 'B')
            """,
            persisted=True,
        ),
        nullable=False,
    )

    # Отношение 1
    category: Mapped["Category"] = relationship("Category", back_populates="products")  # type: ignore

    # Отношение 2
    seller: Mapped["User"] = relationship("User", back_populates="products")  # type: ignore

    # Отношение 5
    reviews: Mapped["Review"] = relationship("Review", back_populates="product") # type: ignore
    
    # Отношение 6
    # Это позволит обращаться к product.cart_items и получать все позиции из корзин, где этот товар присутствует.
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")    # type: ignore

    __table_args__ = (
        Index("ix_products_tsv_gin", "tsv", postgresql_using="gin"),
    )
