from . import orders, recipes, feedback, resources, users, order_details, payments, promotions, recipe_ingredients, menu_items_recipes_resources
from sqlalchemy import Table
from ..dependencies.database import engine, Base


def index():
    orders.Base.metadata.create_all(engine)
    users.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    feedback.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    recipe_ingredients.Base.metadata.create_all(engine)


    Base.metadata.create_all(engine)


