"""Test rayvision_api.user.User functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import User


@pytest.fixture()
def fixture_user(rayvision_connect):
    """Get a User object."""
    return User(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_query_user_profile(fixture_user, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "userId": 10001136,
             "userName": "rayvision",
             "platform": 2,
             "phone": "15945467254",
         }})
    assert fixture_user.query_user_profile()['userId'] == 10001136
    assert fixture_user.query_user_profile()['userName'] == "rayvision"
    assert fixture_user.query_user_profile()['platform'] == 2
    assert fixture_user.query_user_profile()['phone'] == "15945467254"


def test_query_user_setting(fixture_user, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "taskOverTime": 1216165,
             "singleNodeRenderFrames": "1",
             "shareMainCapital": 0,
             "subDeleteTask": 0,
         }})
    assert fixture_user.query_user_setting()['taskOverTime'] == 1216165
    assert fixture_user.query_user_setting()['singleNodeRenderFrames'] == "1"
    assert fixture_user.query_user_setting()['shareMainCapital'] == 0
    assert fixture_user.query_user_setting()['subDeleteTask'] == 0


def test_update_user_settings(fixture_user, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Update user setting failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_over_time = 2582
        fixture_user.update_user_settings(task_over_time)
    assert 'Update user setting failed.' in str(str(err.value))
