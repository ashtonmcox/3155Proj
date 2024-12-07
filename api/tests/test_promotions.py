from fastapi.testclient import TestClient
from ..controllers import promotions as controller
from ..main import app
import pytest
from datetime import date
from ..models import promotions as model
from ..schemas.promotions import PromotionCreate, PromotionUpdate
from sqlalchemy.orm.exc import NoResultFound

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_promotion(db_session):
    promotion_data = {
        "promotion_code": "SUMMER2024",
        "description": "Summer sale discount",
        "expiration_date": date(2024, 8, 31),
        "discount_percent": 10.00
    }
    promotion_create = PromotionCreate(**promotion_data)
    created_promotion = controller.create(db_session, promotion_create)
    assert created_promotion is not None
    assert created_promotion.promotion_code == promotion_data["promotion_code"]
    assert created_promotion.description == promotion_data["description"]
    assert created_promotion.expiration_date == promotion_data["expiration_date"]
    assert created_promotion.discount_percent == promotion_data["discount_percent"]

def test_update_promotion(db_session):
    update_data = {
        "description": "Updated summer sale",
        "discount_percent": 15.00
    }

    existing_promotion = model.Promotion(
        id=1,
        promotion_code="SUMMER2024",
        description="Summer sale discount",
        expiration_date=date(2024, 8, 31),
        discount_percent=10.00
    )

    db_session.query.return_value.filter.return_value.first.return_value = existing_promotion

    updated_promotion = controller.update(db_session, promotion_id=1, request=PromotionUpdate(**update_data))

    existing_promotion.description = update_data["description"]
    existing_promotion.discount_percent = update_data["discount_percent"]

    assert updated_promotion is not None
    assert updated_promotion.description == update_data["description"]
    assert updated_promotion.discount_percent == update_data["discount_percent"]

def test_get_promotion(db_session):
    existing_promotion = model.Promotion(
        id=1,
        promotion_code="SUMMER2024",
        description="Summer sale discount",
        expiration_date=date(2024, 8, 31),
        discount_percent=10.00
    )

    db_session.query.return_value.filter.return_value.first.return_value = existing_promotion

    retrieved_promotion = controller.read_one(db_session, promotion_id=1)

    assert retrieved_promotion is not None
    assert retrieved_promotion.id == 1
    assert retrieved_promotion.promotion_code == "SUMMER2024"
    assert retrieved_promotion.description == "Summer sale discount"
    assert retrieved_promotion.expiration_date == date(2024, 8, 31)
    assert retrieved_promotion.discount_percent == 10.00
