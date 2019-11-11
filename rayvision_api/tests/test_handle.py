"""Test rayvision_utils.task.handle.RayvisionTask functions."""

# Import local models
from rayvision_api.task.handle import RayvisionTask


def test_task(task_info, mocker):
    """Test we can get a correct result."""
    mocker_task_id = mocker.patch.object(RayvisionTask, 'get_task_id')
    mocker_task_id.return_value = '1234567'
    mocker_user_id = mocker.patch.object(RayvisionTask, 'get_user_id')
    mocker_user_id.return_value = '10000012'
    mocker_user_id = mocker.patch.object(RayvisionTask,
                                         'check_and_add_project_name')
    mocker_user_id.return_value = '147258'
    assert RayvisionTask(**task_info).task_id == '1234567'
    assert RayvisionTask(**task_info).user_id == '10000012'
    assert RayvisionTask(**task_info).check_and_add_project_name('test'
                                                                 ) == '147258'
