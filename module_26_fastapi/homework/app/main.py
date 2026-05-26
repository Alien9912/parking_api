from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine, Base
from app import crud, schemas
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Cookbook API",
    description="API для кулинарной книги с сортировкой по популярности",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/recipes", response_model=List[schemas.RecipeListItem])
async def list_recipes(db: AsyncSession = Depends(get_db)):
    recipes = await crud.get_recipes_list(db)
    return [schemas.RecipeListItem.model_validate(r) for r in recipes]

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    recipe = await crud.get_recipe_by_id(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.post("/recipes", response_model=schemas.Recipe, status_code=201)
async def create_recipe(recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_recipe(db, recipe)
