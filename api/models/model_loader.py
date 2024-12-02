from . import orders, recipes, feedback, resources, users, order_details, payments, promotions

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    users.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    feedback.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)


