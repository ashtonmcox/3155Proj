from . import orders, order_details, feedback, payments, promotions, recipes, resources, users, menu_item_popularity, feedback_with_low_rating, recipe_ingredients


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(feedback.router)
    app.include_router(payments.router)
    app.include_router(promotions.router)
    app.include_router(recipes.router)
    app.include_router(resources.router)
    app.include_router(users.router)
    app.include_router(menu_item_popularity.router)
    app.include_router(feedback_with_low_rating.router)
    app.include_router(recipe_ingredients.router)