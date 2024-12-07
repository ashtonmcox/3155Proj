from fastapi.testclient import TestClient 
from ..controllers import orders as controller
from ..main import app
import pytest
from datetime import datetime 
from ..models import orders as model
from ..schemas.orders import OrderCreate, OrderUpdate
from sqlalchemy.orm.exc import NoResultFound

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_order(db_session):
    order_data = {
        "user_id": 1,
        "status": "Processing",
        "tracking_number": "TRK12345",
        "order_type": "Online",  
        "total_price": 99.99,
        "date": datetime.utcnow()  
    }
    order_create = OrderCreate(**order_data)  
    created_order = controller.create(db_session, order_create)
    
    assert created_order is not None
    assert created_order.user_id == order_data["user_id"]
    assert created_order.status == order_data["status"]
    assert created_order.tracking_number == order_data["tracking_number"]
    assert created_order.total_price == order_data["total_price"]
    assert isinstance(created_order.date, datetime)  


def test_update_order(db_session):
    update_data = {
        "status": "Shipped",
        "tracking_number": "TRK54321",
        "total_price": 109.99
    }
    existing_order = model.Order(
        id=1,
        user_id=1,
        status="Processing",
        tracking_number="TRK12345",
        total_price=99.99,
        date=datetime.utcnow()
    )
    db_session.query.return_value.get.return_value = existing_order
    updated_order = controller.update(db_session, order_id=1, request=OrderUpdate(**update_data))
    assert updated_order is not None
    assert updated_order.id == 1
    assert updated_order.status == update_data["status"]
    assert updated_order.tracking_number == update_data["tracking_number"]
    assert updated_order.total_price == update_data["total_price"]

def test_get_order(db_session):
    existing_order = model.Order(
        id=1,
        user_id=1,
        status="Processing",
        tracking_number="TRK12345",
        total_price=99.99,
        date=datetime.utcnow()
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_order
    
    retrieved_order = controller.read_one(db_session, order_id=1)
    
    assert retrieved_order is not None
    assert retrieved_order.id == 1
    assert retrieved_order.user_id == 1
    assert retrieved_order.status == "Processing"
    assert retrieved_order.tracking_number == "TRK12345"
    assert retrieved_order.total_price == 99.99
