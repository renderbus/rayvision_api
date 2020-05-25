"""Test rayvision_api.UserOperator.UserOperator functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import UserOperator


@pytest.fixture()
def user_operator(rayvision_connect):
    """Get a UserOperator object."""
    return UserOperator(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_query_user_profile(user_operator, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "UserID": 10001136,
             "UserName": "rayvision",
             "platform": 2,
             "phone": "15945467254",
         }})
    assert user_operator.query_user_profile()['UserID'] == 10001136
    assert user_operator.query_user_profile()['UserName'] == "rayvision"
    assert user_operator.query_user_profile()['platform'] == 2
    assert user_operator.query_user_profile()['phone'] == "15945467254"


def test_query_user_setting(user_operator, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "taskOverTime": 1216165,
             "singleNodeRenderFrames": "1",
             "shareMainCapital": 0,
             "subDeleteTask": 0,
         }})
    assert user_operator.query_user_setting()['taskOverTime'] == 1216165
    assert user_operator.query_user_setting()['singleNodeRenderFrames'] == "1"
    assert user_operator.query_user_setting()['shareMainCapital'] == 0
    assert user_operator.query_user_setting()['subDeleteTask'] == 0


def test_update_user_setting(user_operator, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Update UserOperator setting failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_over_time = 2582
        user_operator.update_user_settings(task_over_time)
    assert 'Update UserOperator setting failed.' in str(str(err.value))
