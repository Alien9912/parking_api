from pydantic import BaseModel, Field
from typing import List

class RecipeBase(BaseModel):
    name: str = Field(..., description="Название блюда", example="Оливье")
    cooking_time: int = Field(..., description="Время приготовления в минутах", example=60)
    ingredients: List[str] = Field(..., description="Список ингредиентов", example=["картофель", "морковь", "горошек"])
    description: str = Field(..., description="Текстовое описание рецепта", example="Отварить овощи, нарезать, смешать.")

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    views: int = Field(..., description="Количество просмотров")

    class Config:
        from_attributes = True

class RecipeListItem(BaseModel):
    id: int
    name: str
    views: int
    cooking_time: int

    class Config:
        from_attributes = True
