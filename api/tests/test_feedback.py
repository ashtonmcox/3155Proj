from fastapi.testclient import TestClient
from ..controllers import feedback as controller
from ..main import app
import pytest
from ..models.feedback import Feedback as FeedbackModel
from ..schemas.feedback import FeedbackCreate
from sqlalchemy.orm.exc import NoResultFound

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_feedback(db_session):
    feedback_data = {
        "user_id": 1,
        "content": "Great service!",
        "order_details_orders_id": 101,
        "score": 5
    }
    feedback_create = FeedbackCreate(**feedback_data)
    created_feedback = controller.create(db_session, feedback_create)
    assert created_feedback is not None
    assert created_feedback.user_id == feedback_data["user_id"]
    assert created_feedback.content == feedback_data["content"]
    assert created_feedback.order_details_orders_id == feedback_data["order_details_orders_id"]
    assert created_feedback.score == feedback_data["score"]

def test_update_feedback(db_session):
    update_data = {
        "content": "Amazing experience!",
        "score": 4
    }
    existing_feedback = FeedbackModel(
        id=1,
        user_id=1,
        content="Good service",
        order_details_orders_id=101,
        score=5
    )
    db_session.query.return_value.get.return_value = existing_feedback
    updated_feedback = controller.update(db_session, feedback_id=1, update_data=update_data)
    assert updated_feedback is not None
    assert updated_feedback.id == 1
    assert updated_feedback.content == update_data["content"]
    assert updated_feedback.score == update_data["score"]

def test_get_feedback(db_session):
    existing_feedback = FeedbackModel(
        id=1,
        user_id=1,
        content="Great service!",
        order_details_orders_id=101,
        score=5
    )
    db_session.query.return_value.get.return_value = existing_feedback
    retrieved_feedback = controller.get(db_session, feedback_id=1)
    assert retrieved_feedback is not None
    assert retrieved_feedback.id == 1
    assert retrieved_feedback.user_id == 1
    assert retrieved_feedback.content == "Great service!"
    assert retrieved_feedback.order_details_orders_id == 101
    assert retrieved_feedback.score == 5

def test_delete_feedback(db_session):
    existing_feedback = FeedbackModel(
        id=1,
        user_id=1,
        content="Great service!",
        order_details_orders_id=101,
        score=5
    )
    db_session.query.return_value.get.return_value = existing_feedback
    result = controller.delete(db_session, feedback_id=1)
    db_session.delete.assert_called_once_with(existing_feedback)
    db_session.commit.assert_called_once()
    assert result is True

def test_get_feedback_not_found(db_session):
    db_session.query.return_value.get.side_effect = NoResultFound
    with pytest.raises(NoResultFound):
        controller.get(db_session, feedback_id=999)
