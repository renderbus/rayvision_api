"""Interface to operate on the task."""

from rayvision_api import constants


class Task(object):
    """API task related operations."""

    TASK_PARAM = 'taskIds'

    def __init__(self, connect):
        """Initialize instance."""
        self._connect = connect

    def create_task(self, count=1, out_user_id=None):
        """Create task ID.

        Args:
            count (int, optional): The quantity of task ID.
            out_user_id (int, optional): Non-required, external user ID, used
                to distinguish users accessing third parties.

        Returns:
            dict: Task info.
                e.g.:
                    {
                        "taskIdList": [1658434],
                        "aliasTaskIdList": [2W1658434],
                        "userId": 100093088
                    }

        """
        data = {
            'count': count
        }
        if out_user_id:
            data['outUserId'] = out_user_id
        return self._connect.post(constants.CREATE_TASK, data)

    def submit_task(self, task_id):
        """Submit task.

        Args:
            task_id (int): Submit task ID.

        """
        self._connect.post(constants.SUBMIT_TASK, {'taskId': task_id})

    def stop_task(self, task_param_list):
        """Stop the task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.STOP_TASK,
                           {self.TASK_PARAM: task_param_list})

    def start_task(self, task_param_list):
        """Start task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.START_TASK,
                           {self.TASK_PARAM: task_param_list})

    def abort_task(self, task_param_list):
        """Give up the task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.ABORT_TASK,
                           {self.TASK_PARAM: task_param_list})

    def delete_task(self, task_param_list):
        """Delete task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.DELETE_TASK,
                           {self.TASK_PARAM: task_param_list})

    def update_task_level(self, task_id, task_level):
        """Update the level of the task in the render.

        Args:
            task_id (int): Task id.
            task_level (int): Task level.

        """
        data = {
            'taskId': task_id,
            'taskUserLevel': task_level,
        }
        self._connect.post(constants.UPDATE_TASK_USER_LEVEL, data)
