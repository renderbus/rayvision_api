"""Test rayvision_api.task.Task functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import TaskOperator


@pytest.fixture()
def fixture_task(rayvision_connect):
    """Get a Task object."""
    return TaskOperator(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_create_task(fixture_task, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "taskIdList": [1658434],
             "aliasTaskIdList": ['2W1658434'],
             "userId": 100093066
         }})
    assert fixture_task.create_task()['taskIdList'] == [1658434]
    assert fixture_task.create_task()['aliasTaskIdList'] == ['2W1658434']
    assert fixture_task.create_task()['userId'] == 100093066


def test_submit_task(fixture_task, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Submit task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_id = 564642
        fixture_task.submit_task(task_id)
    assert 'Submit task failed.' in str(err.value)


def test_stop_task(fixture_task, mock_requests):
    """Test if code ``604`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 604, 'data': {},
            'message': 'Stop task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_param_list = [336463, 469733]
        fixture_task.stop_task(task_param_list)
    assert 'Stop task failed.' in str(err.value)


def test_start_task(fixture_task, mock_requests):
    """Test if code ``604`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 604, 'data': {},
            'message': 'Start task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_param_list = [456463, 469633]
        fixture_task.start_task(task_param_list)
    assert 'Start task failed.' in str(err.value)


def test_abort_task(fixture_task, mock_requests):
    """Test if code ``604`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 604, 'data': {},
            'message': 'Abort task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_param_list = [456463, 462582]
        fixture_task.abort_task(task_param_list)
    assert 'Abort task failed.' in str(err.value)


def test_delete_task(fixture_task, mock_requests):
    """Test if code ``601`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 601, 'data': {},
            'message': 'Delete task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_param_list = [996463, 462582]
        fixture_task.delete_task(task_param_list)
    assert 'Delete task failed.' in str(err.value)


@pytest.mark.parametrize('task_id, task_level', [
    (661616, 20),
    (661216, -20),
    (6616, 120),
    (6616, 500),
])
def test_update_task_level(fixture_task, mock_requests, task_id, task_level):
    """Test if code ``601`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 601, 'data': {},
            'message': 'Update task level failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        fixture_task.update_priority(task_id, task_level)
    assert 'Update task level failed.' in str(err.value)
