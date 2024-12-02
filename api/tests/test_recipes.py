from fastapi.testclient import TestClient
from ..controllers import recipes as controller
from ..main import app
import pytest
from ..models import recipes as model
from ..schemas.recipes import MenuItemRecipeCreate, MenuItemRecipeUpdate
from sqlalchemy.orm.exc import NoResultFound

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_recipe(db_session):
    recipe_data = {
        "name": "Spaghetti Carbonara",
        "price": 12,
        "category": "Pasta",
        "description": "Classic Italian pasta dish",
        "resource": "Pasta, eggs, cheese, pancetta",
        "instructions": "Cook pasta, mix with sauce, serve",
        "preparation_time": 30,
        "servings": 4,
        "calories": 400
    }
    recipe_create = MenuItemRecipeCreate(**recipe_data)
    created_recipe = controller.create(db_session, recipe_create)
    assert created_recipe is not None
    assert created_recipe.name == recipe_data["name"]
    assert created_recipe.price == recipe_data["price"]
    assert created_recipe.category == recipe_data["category"]
    assert created_recipe.description == recipe_data["description"]
    assert created_recipe.resource == recipe_data["resource"]
    assert created_recipe.instructions == recipe_data["instructions"]
    assert created_recipe.preparation_time == recipe_data["preparation_time"]
    assert created_recipe.servings == recipe_data["servings"]
    assert created_recipe.calories == recipe_data["calories"]

def test_update_recipe(db_session):
    update_data = {
        "description": "Updated classic Italian pasta",
        "calories": 450
    }
    existing_recipe = model.MenuItemRecipe(
        id=1,
        name="Spaghetti Carbonara",
        price=12,
        category="Pasta",
        description="Classic Italian pasta dish",
        resource="Pasta, eggs, cheese, pancetta",
        instructions="Cook pasta, mix with sauce, serve",
        preparation_time=30,
        servings=4,
        calories=400
    )
    db_session.query.return_value.get.return_value = existing_recipe
    updated_recipe = controller.update(db_session, recipe_id=1, update_data=MenuItemRecipeUpdate(**update_data))
    assert updated_recipe is not None
    assert updated_recipe.description == update_data["description"]
    assert updated_recipe.calories == update_data["calories"]

def test_get_recipe(db_session):
    existing_recipe = model.MenuItemRecipe(
        id=1,
        name="Spaghetti Carbonara",
        price=12,
        category="Pasta",
        description="Classic Italian pasta dish",
        resource="Pasta, eggs, cheese, pancetta",
        instructions="Cook pasta, mix with sauce, serve",
        preparation_time=30,
        servings=4,
        calories=400
    )
    db_session.query.return_value.get.return_value = existing_recipe
    retrieved_recipe = controller.get(db_session, recipe_id=1)
    assert retrieved_recipe is not None
    assert retrieved_recipe.id == 1
    assert retrieved_recipe.name == "Spaghetti Carbonara"
    assert retrieved_recipe.price == 12

def test_delete_recipe(db_session):
    existing_recipe = model.MenuItemRecipe(
        id=1,
        name="Spaghetti Carbonara",
        price=12,
        category="Pasta",
        description="Classic Italian pasta dish",
        resource="Pasta, eggs, cheese, pancetta",
        instructions="Cook pasta, mix with sauce, serve",
        preparation_time=30,
        servings=4,
        calories=400
    )
    db_session.query.return_value.get.return_value = existing_recipe
    result = controller.delete(db_session, recipe_id=1)
    db_session.delete.assert_called_once_with(existing_recipe)
    db_session.commit.assert_called_once()
    assert result is True

def test_get_recipe_not_found(db_session):
    db_session.query.return_value.get.side_effect = NoResultFound
    with pytest.raises(NoResultFound):
        controller.get(db_session, recipe_id=999)
