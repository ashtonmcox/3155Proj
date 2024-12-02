from fastapi.testclient import TestClient
from ..controllers import payments as controller
from ..main import app
import pytest
from datetime import datetime
from ..models import payments as model
from ..schemas.payments import PaymentCreate, PaymentUpdate
from sqlalchemy.orm.exc import NoResultFound

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_payment(db_session):
    payment_data = {
        "order_id": 1,
        "card_information": "1234-5678-9876-5432",
        "transaction_status": "Completed",
        "payment_type": "Credit Card"
    }
    payment_create = PaymentCreate(**payment_data)
    created_payment = controller.create(db_session, payment_create)
    assert created_payment is not None
    assert created_payment.order_id == payment_data["order_id"]
    assert created_payment.card_information == payment_data["card_information"]
    assert created_payment.transaction_status == payment_data["transaction_status"]
    assert created_payment.payment_type == payment_data["payment_type"]

def test_update_payment(db_session):
    update_data = {
        "transaction_status": "Failed",
        "payment_type": "Debit Card"
    }
    existing_payment = model.Payment(
        id=1,
        order_id=1,
        card_information="1234-5678-9876-5432",
        transaction_status="Completed",
        payment_type="Credit Card"
    )
    db_session.query.return_value.get.return_value = existing_payment
    updated_payment = controller.update(db_session, payment_id=1, update_data=PaymentUpdate(**update_data))
    assert updated_payment is not None
    assert updated_payment.id == 1
    assert updated_payment.transaction_status == update_data["transaction_status"]
    assert updated_payment.payment_type == update_data["payment_type"]

def test_get_payment(db_session):
    existing_payment = model.Payment(
        id=1,
        order_id=1,
        card_information="1234-5678-9876-5432",
        transaction_status="Completed",
        payment_type="Credit Card"
    )
    db_session.query.return_value.get.return_value = existing_payment
    retrieved_payment = controller.get(db_session, payment_id=1)
    assert retrieved_payment is not None
    assert retrieved_payment.id == 1
    assert retrieved_payment.order_id == 1
    assert retrieved_payment.card_information == "1234-5678-9876-5432"
    assert retrieved_payment.transaction_status == "Completed"
    assert retrieved_payment.payment_type == "Credit Card"

def test_delete_payment(db_session):
    existing_payment = model.Payment(
        id=1,
        order_id=1,
        card_information="1234-5678-9876-5432",
        transaction_status="Completed",
        payment_type="Credit Card"
    )
    db_session.query.return_value.get.return_value = existing_payment
    result = controller.delete(db_session, payment_id=1)
    db_session.delete.assert_called_once_with(existing_payment)
    db_session.commit.assert_called_once()
    assert result is True

def test_get_payment_not_found(db_session):
    db_session.query.return_value.get.side_effect = NoResultFound
    with pytest.raises(NoResultFound):
        controller.get(db_session, payment_id=999)
