from fastapi.testclient import TestClient
from ..controllers import resources as controller
from ..main import app
import pytest
from ..models import resources as model
from ..schemas.resources import ResourceCreate, ResourceUpdate
from sqlalchemy.orm.exc import NoResultFound

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_resource(db_session):
    resource_data = {
        "name": "Flour",
        "amount": 10.5,
        "type": "Ingredient",
        "unit": "kg"
    }
    resource_create = ResourceCreate(**resource_data)
    created_resource = controller.create(db_session, resource_create)
    assert created_resource is not None
    assert created_resource.name == resource_data["name"]
    assert created_resource.amount == resource_data["amount"]
    assert created_resource.type == resource_data["type"]
    assert created_resource.unit == resource_data["unit"]

def test_update_resource(db_session):
    update_data = {
        "amount": 20.0,
        "unit": "lbs"
    }
    existing_resource = model.Resource(
        id=1,
        name="Flour",
        amount=10.5,
        type="Ingredient",
        unit="kg"
    )
    db_session.query.return_value.get.return_value = existing_resource
    updated_resource = controller.update(db_session, resource_id=1, update_data=ResourceUpdate(**update_data))
    assert updated_resource is not None
    assert updated_resource.amount == update_data["amount"]
    assert updated_resource.unit == update_data["unit"]

def test_get_resource(db_session):
    existing_resource = model.Resource(
        id=1,
        name="Flour",
        amount=10.5,
        type="Ingredient",
        unit="kg"
    )
    db_session.query.return_value.get.return_value = existing_resource
    retrieved_resource = controller.get(db_session, resource_id=1)
    assert retrieved_resource is not None
    assert retrieved_resource.id == 1
    assert retrieved_resource.name == "Flour"
    assert retrieved_resource.amount == 10.5

def test_delete_resource(db_session):
    existing_resource = model.Resource(
        id=1,
        name="Flour",
        amount=10.5,
        type="Ingredient",
        unit="kg"
    )
    db_session.query.return_value.get.return_value = existing_resource
    result = controller.delete(db_session, resource_id=1)
    db_session.delete.assert_called_once_with(existing_resource)
    db_session.commit.assert_called_once()
    assert result is True

def test_get_resource_not_found(db_session):
    db_session.query.return_value.get.side_effect = NoResultFound
    with pytest.raises(NoResultFound):
        controller.get(db_session, resource_id=999)
