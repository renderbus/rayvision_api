"""Test rayvision_api.UserOperator.UserOperator functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.api import RayvisionAPIError
from rayvision_api.api import UserOperator


@pytest.fixture()
def fixture_UserOperator(rayvision_connect):
    """Get a UserOperator object."""
    return UserOperator(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_query_UserOperator_profile(fixture_UserOperator, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "UserOperatorId": 10001136,
             "UserOperatorName": "rayvision",
             "platform": 2,
             "phone": "15945467254",
         }})
    assert fixture_UserOperator.query_UserOperator_profile()['UserOperatorId'] == 10001136
    assert fixture_UserOperator.query_UserOperator_profile()['UserOperatorName'] == "rayvision"
    assert fixture_UserOperator.query_UserOperator_profile()['platform'] == 2
    assert fixture_UserOperator.query_UserOperator_profile()['phone'] == "15945467254"


def test_query_UserOperator_setting(fixture_UserOperator, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "taskOverTime": 1216165,
             "singleNodeRenderFrames": "1",
             "shareMainCapital": 0,
             "subDeleteTask": 0,
         }})
    assert fixture_UserOperator.query_UserOperator_setting()['taskOverTime'] == 1216165
    assert fixture_UserOperator.query_UserOperator_setting()['singleNodeRenderFrames'] == "1"
    assert fixture_UserOperator.query_UserOperator_setting()['shareMainCapital'] == 0
    assert fixture_UserOperator.query_UserOperator_setting()['subDeleteTask'] == 0


def test_update_UserOperator_settings(fixture_UserOperator, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Update UserOperator setting failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_over_time = 2582
        fixture_UserOperator.update_UserOperator_settings(task_over_time)
    assert 'Update UserOperator setting failed.' in str(str(err.value))
