from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Recipe
from app.schemas import RecipeCreate

async def get_recipes_list(db: AsyncSession):
    stmt = select(Recipe).order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_recipe_by_id(db: AsyncSession, recipe_id: int):
    stmt = update(Recipe).where(Recipe.id == recipe_id).values(views=Recipe.views + 1).returning(Recipe)
    result = await db.execute(stmt)
    updated_recipe = result.scalar_one_or_none()
    if updated_recipe:
        await db.commit()
        await db.refresh(updated_recipe)
    return updated_recipe

async def create_recipe(db: AsyncSession, recipe: RecipeCreate):
    db_recipe = Recipe(**recipe.model_dump(), views=0)
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe
