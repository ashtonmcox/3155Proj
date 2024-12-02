from fastapi.testclient import TestClient
from ..controllers import order_details as controller
from ..main import app
import pytest
from ..models.order_details import OrderDetail as OrderDetailModel
from ..schemas.order_details import OrderDetailCreate
from datetime import datetime


client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    
    return mocker.Mock()


def test_create_order_detail(db_session):
    
    order_detail_data = {
        "order_id": 1,
        "menu_item_id": 101,
        "quantity": 2
    }

    
    order_detail_create = OrderDetailCreate(**order_detail_data)

    
    created_order_detail = controller.create(db_session, order_detail_create)

    
    assert created_order_detail is not None
    assert created_order_detail.order_id == order_detail_data["order_id"]
    assert created_order_detail.menu_item_id == order_detail_data["menu_item_id"]
    assert created_order_detail.quantity == order_detail_data["quantity"]


def test_update_order_detail(db_session):
    
    update_data = {
        "quantity": 3
    }

    
    existing_order_detail = OrderDetailModel(
        id=1,
        order_id=1,
        menu_item_id=101,
        quantity=2
    )

    db_session.query.return_value.get.return_value = existing_order_detail

    
    updated_order_detail = controller.update(db_session, order_detail_id=1, update_data=update_data)

    
    assert updated_order_detail is not None
    assert updated_order_detail.id == 1
    assert updated_order_detail.order_id == 1
    assert updated_order_detail.menu_item_id == 101
    assert updated_order_detail.quantity == update_data["quantity"]


def test_get_order_detail(db_session):
    
    existing_order_detail = OrderDetailModel(
        id=1,
        order_id=1,
        menu_item_id=101,
        quantity=2
    )

    db_session.query.return_value.get.return_value = existing_order_detail

    
    retrieved_order_detail = controller.get(db_session, order_detail_id=1)

    
    assert retrieved_order_detail is not None
    assert retrieved_order_detail.id == 1
    assert retrieved_order_detail.order_id == 1
    assert retrieved_order_detail.menu_item_id == 101
    assert retrieved_order_detail.quantity == 2


def test_delete_order_detail(db_session):
    
    existing_order_detail = OrderDetailModel(
        id=1,
        order_id=1,
        menu_item_id=101,
        quantity=2
    )

    db_session.query.return_value.get.return_value = existing_order_detail

    
    result = controller.delete(db_session, order_detail_id=1)

   
    db_session.delete.assert_called_once_with(existing_order_detail)
    db_session.commit.assert_called_once()
    assert result is True
