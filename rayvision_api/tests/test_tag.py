"""Test rayvision_api.tag.Tag functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import TagOperator


@pytest.fixture()
def fixture_tag(rayvision_connect):
    """Get a Tag object."""
    return TagOperator(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_add_label(fixture_tag, mock_requests):
    """Test if code ``504`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 504, 'data': {},
            'message': 'Add lable failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        new_name = "afas"
        status = 0
        fixture_tag.add_label(new_name, status)
    assert 'Add lable failed.' in str(err.value)


def test_delete_label(fixture_tag, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Delete lable failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        del_name = "dsfdfa"
        fixture_tag.delete_label(del_name)
    assert 'Delete lable failed.' in str(err.value)


def test_get_project_list(fixture_tag, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {"projectNameList": [
             {"projectId": 3671,
              "projectName": "myLabel"
              }
         ]}}
    )
    assert fixture_tag.get_project_list()[0]['projectId'] == 3671
    assert fixture_tag.get_project_list()[0]['projectName'] == 'myLabel'
