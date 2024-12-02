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
        "code": "SUMMER2024",
        "description": "Summer sale discount",
        "expiration_date": date(2024, 8, 31),
        "discount_value": 10.00,
        "discount_percentage": None
    }
    promotion_create = PromotionCreate(**promotion_data)
    created_promotion = controller.create(db_session, promotion_create)
    assert created_promotion is not None
    assert created_promotion.code == promotion_data["code"]
    assert created_promotion.description == promotion_data["description"]
    assert created_promotion.expiration_date == promotion_data["expiration_date"]
    assert created_promotion.discount_value == promotion_data["discount_value"]

def test_update_promotion(db_session):
    update_data = {
        "description": "Updated summer sale",
        "discount_value": 15.00
    }
    existing_promotion = model.Promotion(
        id=1,
        code="SUMMER2024",
        description="Summer sale discount",
        expiration_date=date(2024, 8, 31),
        discount_value=10.00,
        discount_percentage=None
    )
    db_session.query.return_value.get.return_value = existing_promotion
    updated_promotion = controller.update(db_session, promotion_id=1, update_data=PromotionUpdate(**update_data))
    assert updated_promotion is not None
    assert updated_promotion.description == update_data["description"]
    assert updated_promotion.discount_value == update_data["discount_value"]

def test_get_promotion(db_session):
    existing_promotion = model.Promotion(
        id=1,
        code="SUMMER2024",
        description="Summer sale discount",
        expiration_date=date(2024, 8, 31),
        discount_value=10.00,
        discount_percentage=None
    )
    db_session.query.return_value.get.return_value = existing_promotion
    retrieved_promotion = controller.get(db_session, promotion_id=1)
    assert retrieved_promotion is not None
    assert retrieved_promotion.id == 1
    assert retrieved_promotion.code == "SUMMER2024"
    assert retrieved_promotion.description == "Summer sale discount"
    assert retrieved_promotion.expiration_date == date(2024, 8, 31)

def test_delete_promotion(db_session):
    existing_promotion = model.Promotion(
        id=1,
        code="SUMMER2024",
        description="Summer sale discount",
        expiration_date=date(2024, 8, 31),
        discount_value=10.00,
        discount_percentage=None
    )
    db_session.query.return_value.get.return_value = existing_promotion
    result = controller.delete(db_session, promotion_id=1)
    db_session.delete.assert_called_once_with(existing_promotion)
    db_session.commit.assert_called_once()
    assert result is True

def test_get_promotion_not_found(db_session):
    db_session.query.return_value.get.side_effect = NoResultFound
    with pytest.raises(NoResultFound):
        controller.get(db_session, promotion_id=999)
