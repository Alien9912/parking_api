from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cooking_time: Mapped[int] = mapped_column(Integer, nullable=False)
    ingredients: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0)
