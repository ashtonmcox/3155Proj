from fastapi.testclient import TestClient
from ..controllers import users as controller
from ..main import app
import pytest
from ..models import users as model
from ..schemas.users import UserCreate, UserUpdate
from sqlalchemy.orm.exc import NoResultFound

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_user(db_session):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "address": "123 Main St"
    }
    user_create = UserCreate(**user_data)
    created_user = controller.create(db_session, user_create)
    assert created_user is not None
    assert created_user.name == user_data["name"]
    assert created_user.email == user_data["email"]
    assert created_user.phone_number == user_data["phone_number"]
    assert created_user.address == user_data["address"]

from unittest.mock import MagicMock

def test_update_user(db_session):
    # Define the data to update
    update_data = {
        "email": "newemail@example.com",
        "phone_number": "0987654321"
    }

    # Mock existing user
    existing_user = model.User(
        id=1,
        name="John Doe",
        email="johndoe@example.com",
        phone_number="1234567890",
        address="123 Main St"
    )

    # Mock the query behavior to return the existing user
    db_session.query.return_value.filter.return_value.first.return_value = existing_user

    # Mock the update method to simulate applying updates
    def mock_update(update_data, synchronize_session):
        for key, value in update_data.items():
            setattr(existing_user, key, value)  # Apply updates to the in-memory object

    db_session.query.return_value.filter.return_value.update.side_effect = mock_update

    # Simulate commit behavior
    db_session.commit.return_value = None  # No-op

    # Call the update method in the controller
    user_update = UserUpdate(**update_data)
    updated_user = controller.update(db_session, user_id=1, request=user_update)

    # Assertions to verify the updated user
    assert updated_user is not None
    assert updated_user.id == 1
    assert updated_user.email == update_data["email"]
    assert updated_user.phone_number == update_data["phone_number"]


def test_get_user(db_session):
    existing_user = model.User(
        id=1,
        name="John Doe",
        email="johndoe@example.com",
        phone_number="1234567890",
        address="123 Main St"
    )
    
    db_session.query.return_value.filter.return_value.first.return_value = existing_user
    
    retrieved_user = controller.read_one(db_session, user_id=1)
    
    assert retrieved_user is not None
    assert retrieved_user.id == 1
    assert retrieved_user.name == "John Doe"
    assert retrieved_user.email == "johndoe@example.com"
