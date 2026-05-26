import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import engine, Base

@pytest.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_and_list_recipes(client: AsyncClient):
    new_recipe = {
        "name": "Борщ",
        "cooking_time": 90,
        "ingredients": ["свекла", "капуста", "картофель"],
        "description": "Сварить бульон, добавить овощи."
    }
    resp = await client.post("/recipes", json=new_recipe)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Борщ"
    assert data["views"] == 0
    recipe_id = data["id"]

    resp = await client.get("/recipes")
    assert resp.status_code == 200
    recipes = resp.json()
    assert len(recipes) == 1
    assert recipes[0]["name"] == "Борщ"
    assert recipes[0]["views"] == 0
    assert recipes[0]["cooking_time"] == 90

@pytest.mark.asyncio
async def test_recipe_views_increment(client: AsyncClient):
    new_recipe = {
        "name": "Салат",
        "cooking_time": 20,
        "ingredients": ["огурцы", "помидоры"],
        "description": "Нарезать и смешать."
    }
    resp = await client.post("/recipes", json=new_recipe)
    recipe_id = resp.json()["id"]

    resp1 = await client.get(f"/recipes/{recipe_id}")
    assert resp1.status_code == 200
    assert resp1.json()["views"] == 1

    resp2 = await client.get(f"/recipes/{recipe_id}")
    assert resp2.status_code == 200
    assert resp2.json()["views"] == 2

    resp_list = await client.get("/recipes")
    assert resp_list.json()[0]["views"] == 2

@pytest.mark.asyncio
async def test_not_found(client: AsyncClient):
    resp = await client.get("/recipes/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Recipe not found"

@pytest.mark.asyncio
async def test_sorting_by_views_and_time(client: AsyncClient):
    r1 = {"name": "Популярный", "cooking_time": 10, "ingredients": [], "description": ""}
    r2 = {"name": "Очень популярный", "cooking_time": 5, "ingredients": [], "description": ""}
    r3 = {"name": "Непопулярный", "cooking_time": 20, "ingredients": [], "description": ""}

    resp = await client.post("/recipes", json=r1)
    id1 = resp.json()["id"]
    resp = await client.post("/recipes", json=r2)
    id2 = resp.json()["id"]
    resp = await client.post("/recipes", json=r3)
    id3 = resp.json()["id"]

    await client.get(f"/recipes/{id2}")
    await client.get(f"/recipes/{id2}")
    await client.get(f"/recipes/{id1}")

    resp = await client.get("/recipes")
    recipes = resp.json()
    assert [r["id"] for r in recipes] == [id2, id1, id3]

    r4 = {"name": "Быстрый", "cooking_time": 2, "ingredients": [], "description": ""}
    r5 = {"name": "Медленный", "cooking_time": 15, "ingredients": [], "description": ""}
    resp = await client.post("/recipes", json=r4)
    id4 = resp.json()["id"]
    resp = await client.post("/recipes", json=r5)
    id5 = resp.json()["id"]
    resp = await client.get("/recipes")
    recipes = resp.json()
    zero_views = [r for r in recipes if r["views"] == 0]
    assert [r["id"] for r in zero_views] == [id4, id5, id3]
