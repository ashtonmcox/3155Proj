from fastapi.testclient import TestClient
from ..controllers import recipes as controller
from ..main import app
import pytest
from ..models import recipes as model
from ..schemas.recipes import MenuItemRecipeCreate, MenuItemRecipeUpdate

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_recipe(db_session):
    recipe_data = {
        "name": "Spaghetti Carbonara",
        "price": 12.0, 
        "category": "Pasta",
        "dietary_category": "Vegan",
        "description": "Classic Italian pasta dish",
        "instructions": "Cook pasta, mix with sauce, serve",
        "preparation_time": "30 min",
        "servings": 4,
        "calories": 400
    }

    recipe_create = MenuItemRecipeCreate(**recipe_data)

    created_recipe = controller.create(db_session, recipe_create)

    assert created_recipe is not None
    assert created_recipe.name == recipe_data["name"]
    assert created_recipe.price == recipe_data["price"]
    assert created_recipe.category == recipe_data["category"]
    assert created_recipe.dietary_category == recipe_data["dietary_category"]
    assert created_recipe.description == recipe_data["description"]
    assert created_recipe.instructions == recipe_data["instructions"]
    assert created_recipe.preparation_time == recipe_data["preparation_time"]
    assert created_recipe.servings == recipe_data["servings"]
    assert created_recipe.calories == recipe_data["calories"]

def test_update_recipe(db_session):
    update_data = {
        "description": "Updated classic Italian pasta",
        "calories": 450
    }

    # Mock existing recipe object
    existing_recipe = model.MenuItemRecipe(
        id=1,
        name="Spaghetti Carbonara",
        price=12,
        category="Pasta",
        dietary_category="Vegan",
        description="Classic Italian pasta dish",
        instructions="Cook pasta, mix with sauce, serve",
        preparation_time="30 min",
        servings=4,
        calories=400
    )

    # Mock query and update behavior
    db_session.query.return_value.filter.return_value.first.return_value = existing_recipe

    def mock_update(data, synchronize_session):
        for key, value in data.items():
            setattr(existing_recipe, key, value)

    db_session.query.return_value.filter.return_value.update.side_effect = mock_update

    # Simulate refresh behavior
    db_session.refresh.side_effect = lambda obj: None  # No-op, as the object is already updated

    # Call the controller update function
    updated_recipe = controller.update(db_session, item_id=1, request=MenuItemRecipeUpdate(**update_data))

    # Assertions
    assert updated_recipe is not None
    assert updated_recipe.description == update_data["description"]
    assert updated_recipe.calories == update_data["calories"]

def test_get_recipe(db_session):
    existing_recipe = model.MenuItemRecipe(
        id=1,
        name="Spaghetti Carbonara",
        price=12,
        category="Pasta",
        dietary_category="Vegan",
        description="Classic Italian pasta dish",
        instructions="Cook pasta, mix with sauce, serve",
        preparation_time= "30 min",
        servings=4,
        calories=400
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_recipe
    retrieved_recipe = controller.read_one(db_session, item_id=1)
    assert retrieved_recipe is not None
    assert retrieved_recipe.id == 1
